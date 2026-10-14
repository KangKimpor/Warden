"""Verify the attached log and fetched daily context without copying account IDs."""
from pathlib import Path
from datetime import date
import hashlib, json, math, re

OUT=Path(__file__).parent
log=Path(r'C:\Users\jpkim\Downloads\Telegram Desktop\log_184102461_2026.10.14.txt')
raw=log.read_bytes()
text=raw.decode('utf-8-sig')
balances=re.findall(r'account info balance:\s*([\d.]+)\s+(\w+)',text)
history=re.findall(r'success get orders history, orders retrieved:\s*(\d+)',text)
assert balances and all(float(value)==0 and currency=='USC' for value,currency in balances)
assert history==['0','0']
audit={'source_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'lines':len(text.splitlines()),'currency':'USC','reported_balance':0,'history_response_counts':[int(n) for n in history],'completed_trade_records_present':False,'timestamp_timezone':'not specified','notes':'Application activity log, not a completed-deal trading statement. Zero records in this short log do not establish lifetime trade history.'}
(OUT/'log_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
daily=json.loads((OUT/'alpha_vantage_gold_daily.json').read_text(encoding='utf-8'))
rows=daily['data']
assert len(rows)==166 and len({r['date'] for r in rows})==166
assert all(math.isfinite(float(r['price'])) and float(r['price'])>0 for r in rows)
assert max(r['date'] for r in rows)=='2026-10-13'
audit_daily={'row_count':len(rows),'fields':['date','price'],'unique_dates':len({r['date'] for r in rows}),'weekend_rows':sum(date.fromisoformat(r['date']).weekday()>=5 for r in rows),'suitable_for_M15_replay':False,'intraday_attempt':'Alpha Vantage FX_INTRADAY XAU/USD 15min returned a premium-access error; symbol support not established.'}
(OUT/'data_availability.json').write_text(json.dumps(audit_daily,indent=2),encoding='utf-8')
# Verify unit arithmetic independently of signal extraction.
assert 10*100==1000
assert abs(12*100*0.01*0.01-0.12)<1e-12
assert abs((0.12/10)*100-1.2)<1e-12
print(json.dumps({'log':audit,'daily':audit_daily}))
