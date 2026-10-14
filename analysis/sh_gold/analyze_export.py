"""Read-only Telegram export audit. Outputs go beside this script."""
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime
from collections import Counter
import csv, hashlib, json, re, statistics, sqlite3, sys

SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / 'Downloads' / 'Telegram Desktop' / 'SH Data'
OUT = Path(__file__).parent

class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []
    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()
    def has(self, cls):
        return cls in self.attrs.get('class', '').split()
    def text(self):
        if self.tag == 'br': return '\n'
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)
    def find(self, cls):
        return next((n for n in self.walk() if n.has(cls)), None)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {'br','img','meta','link','input','hr','source'}: self.stack.append(node)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break
    def handle_data(self, data): self.stack[-1].children.append(data)

def numbers(label, text):
    # shortcut: only explicit English price labels are parsed; manually review image/Khmer-only signals before expanding.
    match = re.search('(?:' + label + r')\s*[:=\-]?\s*((?:\d[\d,.]*)(?:\s*[-–/]\s*\d[\d,.]*)*)', text, re.I)
    return [float(x.replace(',', '')) for x in re.findall(r'\d[\d,.]*', match[1])] if match else []

def signal(text):
    sides = set(re.findall(r'\b(buy|sell|long|short)\b', text.lower()))
    direction = set('buy' if x in {'buy','long'} else 'sell' for x in sides)
    entry = numbers(r'\bentry', text)
    if not entry:
        entry = numbers(r'\b(?:buy|sell|long|short)\s*(?:now\s*)?', text)
    sl = numbers(r'\b(?:SL|stop\s*loss)', text)
    tp = numbers(r'(?:^|\n)[^\w\n]*TP(?:\s*1)?|(?:^|\n)[^\w\n]*take\s*profit', text)
    gold = bool(re.search(r'\b(?:gold|xauusd|xau)\b', text, re.I))
    crypto = bool(re.search(r'\b(?:btc|eth|bitcoin|ethereum|sol|bnb)\b', text.split('\n\n')[0], re.I))
    candidate = len(direction) == 1 and bool(entry) and not crypto and (gold or (sl and tp))
    side = next(iter(direction)) if len(direction)==1 else ''
    complete = bool(candidate and entry and len(sl)==1 and tp)
    valid = complete and (sl[0]<min(entry) and max(entry)<min(tp) if side=='buy' else max(tp)<min(entry) and max(entry)<sl[0])
    # User confirmed the unnamed SH price signals are gold; preserve explicit crypto exclusions.
    instrument = 'explicit_crypto' if crypto else 'explicit_gold' if gold else 'user_confirmed_gold' if candidate else 'unclassified'
    return dict(candidate=bool(candidate), instrument=instrument, side=side, entry=entry, sl=sl, tp=tp,
                complete=bool(complete), valid=bool(valid),
                risk=abs(entry[0]-sl[0]) if valid else None,
                reward=abs(tp[0]-entry[0]) if valid else None,
                rr=abs(tp[0]-entry[0])/abs(entry[0]-sl[0]) if valid else None,
                rr_final=abs(tp[-1]-entry[0])/abs(entry[0]-sl[0]) if valid else None)

def self_check():
    p=Parser(); p.feed('<div class="message default" id="message1"><div class="text">Short Gold<br>Entry: 4580<br>SL: 4595<br>TP: 4565</div></div>')
    s=signal(p.root.find('text').text())
    assert s['valid'] and s['rr']==1 and s['risk']==15
    assert signal('Buy Gold Entry: 4580\nSL: 4595\nTP: 4600')['valid'] is False
    assert signal('Buy Gold Entry: 4580-4585\nSL: 4570\nTP: 4600')['valid']
    assert signal('Short Now 4580\nSL: 4595\nTP: 4565 - 4560 - 4550')['tp']==[4565,4560,4550]
    assert signal('Short Now 4580\nSL: 4595\nTP: 4565')['instrument']=='user_confirmed_gold'
    assert signal('Short BTC Entry: 90000 SL: 91000 TP: 88000')['candidate'] is False
    assert signal('Short BTC Entry: 90000 SL: 91000 TP: 88000')['instrument']=='explicit_crypto'
    assert signal('Buy BTC Entry: 90000 SL: 89000 TP: 92000')['candidate'] is False
    assert numbers(r'\bentry','Entry: 4,580.50') == [4580.5]
    assert signal('Close at TP 1\nShort 4145\nSL: 4160\nTP: 4130 - 4125')['tp']==[4130,4125]

def main():
    self_check()
    messages=[]; inventory=[]
    for file in sorted(SOURCE.glob('messages*.html'), key=lambda f:int(re.search(r'(\d*)\.html', f.name)[1] or 1)):
        data=file.read_bytes(); p=Parser(); p.feed(data.decode('utf-8'))
        rows=[n for n in p.root.walk() if n.has('message') and n.has('default')]
        assert len(rows)==len(re.findall(r'class="message default', data.decode('utf-8')))
        inventory.append(dict(file=file.name, sha256=hashlib.sha256(data).hexdigest(), messages=len(rows)))
        for n in rows:
            txt=n.find('text'); date=n.find('date'); reply=n.find('reply_to')
            title=date.attrs.get('title','') if date else ''
            stamp=datetime.strptime(title, '%d.%m.%Y %H:%M:%S UTC%z') if title else None
            replyids=re.findall(r'go_to_message(\d+)',str(reply.attrs)+''.join(str(x.attrs) for x in reply.walk())) if reply else []
            media=[x.attrs['href'] for x in n.walk() if x.tag=='a' and x.attrs.get('href','').startswith(('photos/','video_files/','voice_messages/','files/'))]
            text=txt.text().strip() if txt else ''
            messages.append(dict(id=int(n.attrs['id'].replace('message','')), file=file.name,
                timestamp=stamp.isoformat() if stamp else '', text=text,
                reply_to=int(replyids[0]) if replyids else None, media=media, **signal(text)))
    ids=[m['id'] for m in messages]
    assert len(ids)==len(set(ids)), 'Duplicate message IDs require review'
    signals=[m for m in messages if m['candidate']]
    valid=[m for m in signals if m['valid']]
    byid={m['id']:m for m in messages}
    for m in signals:
        replies=[x for x in messages if x['reply_to']==m['id']]
        m['direct_reply_ids']=[x['id'] for x in replies]
        m['reply_text']='\n'.join(f"{x['id']} {x['timestamp']} {x['text']}" for x in replies)
        # Mentions are evidence of reporting, never verified trade outcomes.
        m['reply_tp_mention']=any(re.search(r'\bTP\b|take\s*profit',x['text'],re.I) for x in replies)
        m['reply_sl_mention']=any(re.search(r'\bSL\b|stop\s*loss',x['text'],re.I) for x in replies)
        m['review_flags']=[]
        if not m['valid']: m['review_flags'].append('price_order_or_abbreviated_range')
        if m['valid'] and m['risk']>80: m['review_flags'].append('unusually_wide_stop_check_source')
        if m['valid'] and m['rr']>4: m['review_flags'].append('unusual_first_target_check_source')
        if 'bonus' in m['text'].lower(): m['review_flags'].append('parenthetical_target_not_parsed')
    def quant(values):
        return dict(min=min(values), median=statistics.median(values), max=max(values)) if values else {}
    monthly=[]
    for month in sorted(set(m['timestamp'][:7] for m in messages)):
        subset=[m for m in signals if m['timestamp'].startswith(month)]
        monthly.append(dict(month=month, messages=sum(m['timestamp'].startswith(month) for m in messages),explicit_gold=sum(m['instrument']=='explicit_gold' for m in subset),
            candidates=len(subset),valid=sum(m['valid'] for m in subset),
            buys=sum(m['side']=='buy' for m in subset),sells=sum(m['side']=='sell' for m in subset)))
    summary=dict(source=str(SOURCE), inventory=inventory, total_messages=len(messages),
        first=min(m['timestamp'] for m in messages),last=max(m['timestamp'] for m in messages),
        text_messages=sum(bool(m['text']) for m in messages), media_messages=sum(bool(m['media']) for m in messages),
        candidates=len(signals),complete=sum(m['complete'] for m in signals),valid=len(valid),
        invalid_complete=[m['id'] for m in signals if m['complete'] and not m['valid']],
        reply_tp_mentions=sum(m['reply_tp_mention'] for m in signals),reply_sl_mentions=sum(m['reply_sl_mention'] for m in signals),
        no_direct_reply=sum(not m['direct_reply_ids'] for m in signals),
        explicit_gold=sum(m['instrument']=='explicit_gold' for m in signals),
        user_confirmed_gold=sum(m['instrument']=='user_confirmed_gold' for m in signals),
        instrument_scope='All 359 non-crypto price candidates are XAUUSD: 54 explicit, 305 confirmed by user on 2026-10-14. Explicit BTC/ETH posts retain their exclusion.',
        review_flags={m['id']:m['review_flags'] for m in signals if m['review_flags']},
        entry_ranges=sum(len(m['entry'])>1 for m in valid),multiple_targets=sum(len(m['tp'])>1 for m in valid),
        rr=quant([m['rr'] for m in valid]),rr_final=quant([m['rr_final'] for m in valid]),risk=quant([m['risk'] for m in valid]),reward=quant([m['reward'] for m in valid]),
        explicit_rr=quant([m['rr'] for m in valid if m['instrument']=='explicit_gold']),
        explicit_risk=quant([m['risk'] for m in valid if m['instrument']=='explicit_gold']),
        explicit_rr_final=quant([m['rr_final'] for m in valid if m['instrument']=='explicit_gold']),
        valid_sides=dict(Counter(m['side'] for m in valid)),
        valid_hours=dict(sorted(Counter(int(m['timestamp'][11:13]) for m in valid).items())),
        monthly=monthly,
        orphan_replies=sum(m['reply_to'] is not None and m['reply_to'] not in byid for m in messages),
        repeated_valid_templates=sum(c-1 for c in Counter((m['side'],tuple(m['entry']),tuple(m['sl']),tuple(m['tp'])) for m in valid).values()),
        media_inventory=dict(Counter(f.suffix.lower() for d in ['photos','video_files','voice_messages','files'] for f in (SOURCE/d).glob('*') if f.is_file())))
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    (OUT/'messages.json').write_text(json.dumps(messages,ensure_ascii=False),encoding='utf-8')
    with sqlite3.connect(OUT/'audit.sqlite') as db:
        db.executescript('DROP TABLE IF EXISTS messages; DROP TABLE IF EXISTS parsed_signals; CREATE TABLE messages(id INTEGER PRIMARY KEY, timestamp TEXT, source_file TEXT); CREATE TABLE parsed_signals(id INTEGER PRIMARY KEY, timestamp TEXT, instrument TEXT, side TEXT, entry TEXT, sl TEXT, tp TEXT, valid INTEGER, risk REAL, rr REAL, rr_final REAL);')
        db.executemany('INSERT INTO messages VALUES (?,?,?)',[(m['id'],m['timestamp'],m['file']) for m in messages])
        db.executemany('INSERT INTO parsed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?)',[(m['id'],m['timestamp'],m['instrument'],m['side'],str(m['entry']),str(m['sl']),str(m['tp']),int(m['valid']),m['risk'],m['rr'],m['rr_final']) for m in signals])
        assert db.execute('SELECT COUNT(*) FROM messages').fetchone()[0]==len(messages)
    with (OUT/'signals.csv').open('w',newline='',encoding='utf-8-sig') as f:
        fields=['id','file','timestamp','instrument','side','entry','sl','tp','complete','valid','review_flags','risk','reward','rr','rr_final','direct_reply_ids','reply_tp_mention','reply_sl_mention','text','reply_text','media']
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader();w.writerows(signals)
    print(json.dumps(summary,indent=2,ensure_ascii=True))
    for m in signals[:5]+signals[-10:]:
        print(json.dumps({k:m[k] for k in ['id','timestamp','text','reply_text']},ensure_ascii=True))

if __name__=='__main__': main()
