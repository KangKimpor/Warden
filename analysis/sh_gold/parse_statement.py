"""Reconcile all closed gold positions in the supplied statement, in USC."""
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from collections import Counter, defaultdict
from itertools import groupby
import csv, hashlib, json, statistics, re, sqlite3

ROOT=Path(__file__).parent
PDF=Path(r'C:\Users\jpkim\Downloads\Telegram Desktop\statement-184102461-2026-10-14.pdf')
text=(ROOT/'statement_review'/'statement_text.txt').read_text(encoding='utf-8')
trades=[]
for line in text.splitlines():
    p=line.split()
    if len(p)>=5 and p[1] in {'buy','sell'} and p[4]=='XAUUSDc':
        assert len(p)==17, p
        stamp=lambda i:datetime.strptime(p[i]+' '+p[i+1],'%Y-%m-%d %H:%M:%S')
        trade=dict(sequence=len(trades)+1,position_id=p[0],side=p[1],opened=stamp(2).isoformat(),closed=stamp(7).isoformat(),
            open_price=float(p[5]),volume_cent_lots=float(p[6]),close_price=float(p[9]),close_volume=float(p[10]),
            recorded_sl=float(p[11]),recorded_tp=float(p[12]),commission_usc=float(p[13]),tax_usc=float(p[14]),swap_usc=float(p[15]),profit_usc=float(p[16]),profit_usd=float(Decimal(p[16])/100),holding_seconds=(stamp(7)-stamp(2)).total_seconds())
        assert trade['holding_seconds']>=0 and trade['volume_cent_lots']==trade['close_volume']
        signed_move=Decimal(p[9])-Decimal(p[5]) if p[1]=='buy' else Decimal(p[5])-Decimal(p[9])
        predicted_usc=signed_move*Decimal(p[6])*100
        # Printed prices and P/L are rounded; this checks gold cent exposure without assuming initial SL.
        assert abs(predicted_usc-Decimal(p[16]))<=Decimal('0.15'), (p[0],predicted_usc,p[16])
        trades.append(trade)
assert len(trades)==len(re.findall(r'^\s*\d+\s+(?:buy|sell)\s+\d{4}-\d{2}-\d{2}.*XAUUSDc',text,re.M))
assert len({t['position_id'] for t in trades})==len(trades)
net=sum(Decimal(str(t['profit_usc'])) for t in trades)
assert net==Decimal('233.9')
assert Decimal('1500')-Decimal('1733')+net==Decimal('0.9')
winners=[t for t in trades if t['profit_usc']>0];losers=[t for t in trades if t['profit_usc']<0]
daily=[]
for day in sorted({t['closed'][:10] for t in trades}):
    ts=[t for t in trades if t['closed'].startswith(day)]
    daily.append(dict(day=day,trades=len(ts),wins=sum(t['profit_usc']>0 for t in ts),losses=sum(t['profit_usc']<0 for t in ts),net_usd=round(sum(t['profit_usd'] for t in ts),3),no_recorded_sl=sum(t['recorded_sl']==0 for t in ts)))
balance=Decimal('1500');peak=balance;dd=Decimal(0);dd_rate=Decimal(0);curve=[]
# Aggregate simultaneous closes so printed row ordering does not create fictional intermediate balances.
for stamp,items in groupby(sorted(trades,key=lambda t:t['closed']),key=lambda t:t['closed']):
    ts=list(items);balance+=sum(Decimal(str(t['profit_usc'])) for t in ts);peak=max(peak,balance)
    dd=max(dd,peak-balance);dd_rate=max(dd_rate,(peak-balance)/peak)
    curve.append(dict(closed=stamp,balance_usd=float(balance/100),net_usd=float((balance-1500)/100),closed_trades=sum(t['closed']<=stamp for t in trades)))
events=defaultdict(lambda: {'open':[],'close':[]})
for t in trades:events[t['opened']]['open'].append(t);events[t['closed']]['close'].append(t)
active={};max_n=0;max_volume=0;max_exposure_at='';max_exposure=[]
for stamp,event in sorted(events.items()):
    for t in event['close']:active.pop(t['position_id'],None)
    for t in event['open']:active[t['position_id']]=t
    max_n=max(max_n,len(active));gross=sum(t['volume_cent_lots'] for t in active.values())
    if gross>max_volume:max_volume=gross;max_exposure_at=stamp;max_exposure=list(active.values())
last_two=sorted(trades,key=lambda t:t['opened'])[-2:]
gross_win=sum(t['profit_usd'] for t in winners);gross_loss=-sum(t['profit_usd'] for t in losers)
small_window=[t for t in trades if '2026-08-11T14:06:00'<=t['opened']<'2026-08-11T14:27:00']
aug19=[t for t in trades if t['closed']=='2026-08-19T07:05:57']
summary=dict(pdf_pages=3,pdf_sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),statement_period='2026-08-06 through 2026-10-14',actual_trading_dates=[min(t['opened'][:10] for t in trades),max(t['closed'][:10] for t in trades)],timezone='not specified in statement',
    closed_trades=len(trades),wins=len(winners),losses=len(losers),win_rate=len(winners)/len(trades),net_usc=float(net),net_usd=float(net/100),deposit_usd=15,withdrawal_usd=17.33,closing_balance_usd=0.009,
    cancelled_pending_orders=sum('cancelled' in l and 'XAUUSDc' in l for l in text.splitlines()),gross_profit_usd=round(gross_win,3),gross_loss_usd=round(gross_loss,3),profit_factor=gross_win/gross_loss,
    mean_win_usd=statistics.mean(t['profit_usd'] for t in winners),mean_loss_usd=statistics.mean(-t['profit_usd'] for t in losers),median_win_usd=statistics.median(t['profit_usd'] for t in winners),median_loss_usd=statistics.median(-t['profit_usd'] for t in losers),
    no_recorded_sl=sum(t['recorded_sl']==0 for t in trades),no_recorded_sl_tp=sum(t['recorded_sl']==t['recorded_tp']==0 for t in trades),holding_seconds_median=statistics.median(t['holding_seconds'] for t in trades),under_60_seconds=sum(t['holding_seconds']<60 for t in trades),
    volume_distribution=dict(Counter(t['volume_cent_lots'] for t in trades)),max_simultaneous_positions=max_n,max_gross_cent_lots=max_volume,max_exposure_at=max_exposure_at,
    last_two_profit_usd=round(sum(t['profit_usd'] for t in last_two),3),net_without_last_two_usd=round(float(net/100)-sum(t['profit_usd'] for t in last_two),3),gross_profit_share_last_two=sum(t['profit_usd'] for t in last_two)/gross_win,
    last_two=last_two,maximum_closed_balance_drawdown_usd=float(dd/100),maximum_closed_balance_drawdown_rate=float(dd_rate),minimum_closed_balance_usd=min(r['balance_usd'] for r in curve),
    august11_21minute_entries=len(small_window),august19_same_close_loss_usd=round(sum(t['profit_usd'] for t in aug19),3),august19_same_close_positions=len(aug19),daily=daily,
    all_explicit_charges_zero=all(t['commission_usc']==t['tax_usc']==t['swap_usc']==0 for t in trades),cent_gold_ounce_exposure_confirmed_by_all_printed_trade_price_pnl_pairs=True)
with (ROOT/'statement_trades.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(trades[0]));w.writeheader();w.writerows(trades)
(ROOT/'statement_metrics.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
(ROOT/'closed_balance_curve.json').write_text(json.dumps(curve,indent=2),encoding='utf-8')
with sqlite3.connect(ROOT/'audit.sqlite') as db:
    db.executescript('DROP TABLE IF EXISTS closed_balance; CREATE TABLE closed_balance(closed TEXT PRIMARY KEY, balance_usd REAL, net_usd REAL, closed_trades INTEGER);')
    db.execute('INSERT INTO closed_balance VALUES (?,?,?,?)',('2026-08-10T02:10:57',15,0,0))
    db.executemany('INSERT INTO closed_balance VALUES (?,?,?,?)',[(r['closed'],r['balance_usd'],r['net_usd'],r['closed_trades']) for r in curve])
    assert abs(db.execute('SELECT balance_usd FROM closed_balance ORDER BY closed DESC LIMIT 1').fetchone()[0]-17.339)<1e-12
print(json.dumps(summary,indent=2))
