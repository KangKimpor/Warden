import test from 'node:test';
import assert from 'node:assert/strict';
import { runV7, breakout, levels, timeDue, ema, atr, inSession } from '../src/v7.js';
import { marketOpen } from '../src/index.js';

const MIN = 60000;
const T0 = Date.UTC(2026, 0, 5, 0, 0); // a Monday

// Flat history, then a rising ramp so EMA50 > EMA200, then custom tail bars.
function series(tail, tf = 15) {
  const bars = [];
  let p = 1000;
  for (let i = 0; i < 260; i++) {
    p += 0.2;
    bars.push({ t: T0 + i * tf * MIN, o: p - 0.1, h: p + 0.5, l: p - 0.5, c: p });
  }
  tail.forEach((x, k) => {
    const i = 260 + k;
    bars.push({ t: T0 + i * tf * MIN, ...x });
  });
  return bars;
}
const last = (bars) => bars[bars.length - 1];
const NOW_FAR = (bars, tf = 15) => last(bars).t + 10 * tf * MIN;

test('mirrors the indicator self-checks', () => {
  assert.deepEqual(levels(100, 3, 6, 1), [97, 106]);
  assert.deepEqual(levels(100, 3, 6, -1), [103, 94]);
  assert.equal(breakout(105, 104, 95, 102, 100), 1);
  assert.equal(breakout(94, 104, 95, 98, 100), -1);
  assert.equal(breakout(104, 104, 95, 102, 100), 0);
  assert.equal(breakout(105, 104, 95, 98, 100), 0);
  assert.equal(timeDue(23, 24, true), false);
  assert.equal(timeDue(24, 24, true), true);
  assert.equal(timeDue(24, 24, false), false);
  assert.equal(timeDue(1, 1, true), true);
});

test('ema and atr follow Pine seeding', () => {
  assert.deepEqual(ema([10, 10, 10], 5), [10, 10, 10]);
  const bars = Array.from({ length: 20 }, () => ({ o: 1, h: 3, l: 1, c: 2 }));
  const a = atr(bars, 14);
  assert.ok(Number.isNaN(a[12]));
  assert.equal(a[13], 2); // SMA of 14 true ranges of 2 (first bar h-l)
  assert.ok(Math.abs(a[19] - 2) < 1e-9);
});

test('breakout -> next-open entry with ATR based SL and 2x TP, then TP exit', () => {
  const tail = [
    { o: 1052, h: 1053, l: 1051.5, c: 1052.8 }, // strong close above the 24-bar high => signal
    { o: 1053.0, h: 1053.4, l: 1052.5, c: 1053.1 }, // next open => entry at 1053.0
  ];
  const bars = series(tail);
  const { events, active } = runV7(bars, 15, NOW_FAR(bars));
  const entries = events.filter((e) => e.type === 'entry');
  const e = entries.find((x) => x.t === bars[261].t);
  assert.ok(e, 'entry on the bar after the signal');
  assert.equal(e.side, 1);
  assert.equal(e.entry, 1053.0);
  const dist = e.entry - e.sl;
  assert.ok(Math.abs((e.tp - e.entry) - 2 * dist) < 0.0011, 'TP is 2x stop distance');
  assert.equal(active, true);

  // price rallies to TP
  const bars2 = series([...tail, { o: 1053.1, h: e.tp + 1, l: 1053, c: e.tp }]);
  const r = runV7(bars2, 15, NOW_FAR(bars2));
  const end = r.events.find((x) => x.type === 'end' && x.entryT === e.entryT);
  assert.equal(end.reason, 'TP touched: plan ended');
});

test('SL touched, and SL+TP in one bar is reported as unknown', () => {
  const tail = [
    { o: 1052, h: 1053, l: 1051.5, c: 1052.8 },
    { o: 1053.0, h: 1053.4, l: 1052.5, c: 1053.1 },
  ];
  const probe = runV7(series(tail), 15, Infinity).events.find((x) => x.type === 'entry' && x.t === series(tail)[261].t);
  const sl = probe.sl;
  const tp = probe.tp;

  const bSl = series([...tail, { o: 1053, h: 1053.2, l: sl - 0.01, c: 1052 }]);
  assert.equal(runV7(bSl, 15, NOW_FAR(bSl)).events.find((x) => x.type === 'end').reason, 'SL touched: plan ended');

  const bBoth = series([...tail, { o: 1053, h: tp + 0.01, l: sl - 0.01, c: 1053 }]);
  assert.equal(runV7(bBoth, 15, NOW_FAR(bBoth)).events.find((x) => x.type === 'end').reason, 'SL + TP touched: order unknown');
});

test('time exit only on a confirmed 24th bar, and no signal while a plan is active', () => {
  const tail = [
    { o: 1052, h: 1053, l: 1051.5, c: 1052.8 },
    { o: 1053.0, h: 1053.4, l: 1052.5, c: 1053.1 },
  ];
  for (let k = 0; k < 30; k++) tail.push({ o: 1053.1, h: 1053.5, l: 1052.9, c: 1053.2 }); // quiet drift inside SL/TP
  const bars = series(tail);
  const { events } = runV7(bars, 15, NOW_FAR(bars));
  const entry = events.find((e) => e.type === 'entry');
  const end = events.find((e) => e.type === 'end' && e.entryT === entry.entryT);
  assert.equal(end.reason, 'Time exit: close remaining trade');
  assert.equal(end.t, entry.t + 23 * 15 * MIN); // age = bars since entry + 1 >= 24
  assert.equal(events.filter((e) => e.type === 'entry' && e.t > entry.t && e.t < end.t).length, 0);

  // Same data, but "now" is inside the 24th bar: not yet confirmed, so no time exit.
  const early = runV7(bars, 15, end.t + 1 * MIN).events.filter((e) => e.type === 'end' && e.entryT === entry.entryT);
  assert.equal(early.length, 0);
});

test('short side breakout', () => {
  const bars = [];
  let p = 1100;
  for (let i = 0; i < 260; i++) {
    p -= 0.2;
    bars.push({ t: T0 + i * 15 * MIN, o: p + 0.1, h: p + 0.5, l: p - 0.5, c: p });
  }
  bars.push({ t: T0 + 260 * 15 * MIN, o: p - 1, h: p - 0.5, l: p - 3, c: p - 2.8 });
  bars.push({ t: T0 + 261 * 15 * MIN, o: p - 2.9, h: p - 2.5, l: p - 3.2, c: p - 3 });
  const { events } = runV7(bars, 15, NOW_FAR(bars));
  const e = events.find((x) => x.type === 'entry' && x.t === bars[261].t);
  assert.equal(e.side, -1);
  assert.ok(e.sl > e.entry && e.tp < e.entry);
});

test('session filter uses Cambodia time (UTC+7)', () => {
  assert.equal(inSession(Date.UTC(2026, 0, 5, 7, 0)), true); // Mon 14:00 KH
  assert.equal(inSession(Date.UTC(2026, 0, 5, 15, 59)), true); // Mon 22:59 KH
  assert.equal(inSession(Date.UTC(2026, 0, 5, 16, 0)), false); // Mon 23:00 KH
  assert.equal(inSession(Date.UTC(2026, 0, 3, 8, 0)), false); // Sat
});

test('market hours gate', () => {
  assert.equal(marketOpen(Date.UTC(2026, 0, 6, 12)), true); // Tue
  assert.equal(marketOpen(Date.UTC(2026, 0, 9, 21, 59)), true); // Fri before close
  assert.equal(marketOpen(Date.UTC(2026, 0, 9, 22, 0)), false); // Fri close
  assert.equal(marketOpen(Date.UTC(2026, 0, 10, 12)), false); // Sat
  assert.equal(marketOpen(Date.UTC(2026, 0, 11, 21, 59)), false); // Sun before open
  assert.equal(marketOpen(Date.UTC(2026, 0, 11, 22, 0)), true); // Sun open
});
