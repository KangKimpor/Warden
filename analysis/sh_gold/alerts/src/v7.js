// Port of Gold Entry v7 - M15 / H1 (analysis/sh_gold/indicator/gold_entry_v7.pine).
// Same rules and per-bar order of evaluation as the Pine script; do not change them here
// without changing the indicator first.

export const DEFAULTS = {
  lookback: 24,
  stopATR: 1.5,
  targetR: 2,
  holdBars: 24,
  sessionOnly: false,
  mintick: 0.001,
};

// ta.ema: seeded with the first source value.
export function ema(src, len) {
  const a = 2 / (len + 1);
  const out = new Array(src.length);
  for (let i = 0; i < src.length; i++) {
    out[i] = i === 0 ? src[0] : a * src[i] + (1 - a) * out[i - 1];
  }
  return out;
}

// ta.atr: RMA of true range, seeded with the SMA of the first `len` values.
export function atr(bars, len = 14) {
  const out = new Array(bars.length).fill(NaN);
  let sum = 0;
  let prev = NaN;
  for (let i = 0; i < bars.length; i++) {
    const b = bars[i];
    const tr = i === 0
      ? b.h - b.l
      : Math.max(b.h - b.l, Math.abs(b.h - bars[i - 1].c), Math.abs(b.l - bars[i - 1].c));
    if (i < len - 1) {
      sum += tr;
    } else if (i === len - 1) {
      sum += tr;
      prev = sum / len;
      out[i] = prev;
    } else {
      prev = (prev * (len - 1) + tr) / len;
      out[i] = prev;
    }
  }
  return out;
}

export function breakout(c, upper, lower, fast, slow) {
  return c > upper && fast > slow ? 1 : c < lower && fast < slow ? -1 : 0;
}

export function levels(entry, distance, reward, side) {
  return [entry - side * distance, entry + side * reward];
}

export function timeDue(age, maximum, confirmed) {
  return confirmed && age >= maximum;
}

// Monday-Friday, 14:00-22:59 Asia/Phnom_Penh (UTC+7, no DST).
export function inSession(stampMs) {
  const d = new Date(stampMs + 7 * 3600 * 1000);
  const day = d.getUTCDay();
  const h = d.getUTCHours();
  return day >= 1 && day <= 5 && h >= 14 && h < 23;
}

// bars: ascending [{t: bar open (ms UTC), o, h, l, c}]. A bar is confirmed once t + tf <= now.
// Returns every entry/end event the indicator would have alerted on across the supplied history.
export function runV7(bars, tfMin, now, options = {}) {
  const o = { ...DEFAULTS, ...options };
  const tfMs = tfMin * 60000;
  const n = bars.length;
  const closes = bars.map((b) => b.c);
  const fast = ema(closes, 50);
  const slow = ema(closes, 200);
  const atrs = atr(bars, 14);

  let planSide = 0;
  let entryBar = NaN;
  let entryT = NaN;
  let entry = NaN;
  let distance = NaN;
  let reward = NaN;
  let active = false;
  let pending = false;
  let pendingSide = 0;
  let pendingDistance = NaN;
  let pendingReward = NaN;

  const events = [];

  for (let i = 0; i < n; i++) {
    const b = bars[i];
    const confirmed = b.t + tfMs <= now;

    let upper = NaN;
    let lower = NaN;
    if (i >= o.lookback) {
      upper = -Infinity;
      lower = Infinity;
      for (let k = i - o.lookback; k < i; k++) {
        if (bars[k].h > upper) upper = bars[k].h;
        if (bars[k].l < lower) lower = bars[k].l;
      }
    }
    const side = breakout(b.c, upper, lower, fast[i], slow[i]);

    if (pending) {
      planSide = pendingSide;
      entryBar = i;
      entryT = b.t;
      entry = b.o;
      distance = pendingDistance;
      reward = pendingReward;
      active = true;
      pending = false;
      const [sl, tp] = levels(entry, distance, reward, planSide);
      events.push({ type: 'entry', side: planSide, entry, sl, tp, t: b.t, entryT });
    }

    const [stop, target] = levels(entry, distance, reward, planSide);
    const stopHit = active && (planSide === 1 ? b.l <= stop : b.h >= stop);
    const targetHit = active && (planSide === 1 ? b.h >= target : b.l <= target);
    const timeExit = active && timeDue(i - entryBar + 1, o.holdBars, confirmed);
    if (active && (stopHit || targetHit || timeExit)) {
      active = false;
      const reason = stopHit && targetHit
        ? 'SL + TP touched: order unknown'
        : stopHit
          ? 'SL touched: plan ended'
          : targetHit
            ? 'TP touched: plan ended'
            : 'Time exit: close remaining trade';
      events.push({ type: 'end', reason, side: planSide, entry, sl: stop, tp: target, t: b.t, entryT });
    }

    const signal = confirmed
      && i >= Math.max(200, o.lookback)
      && atrs[i] > 0
      && side !== 0
      && !active && !pending
      && (!o.sessionOnly || inSession(b.t + tfMs));
    if (signal) {
      pending = true;
      pendingSide = side;
      const distTicks = Math.max(1, Math.ceil(atrs[i] * o.stopATR / o.mintick));
      pendingDistance = distTicks * o.mintick;
      pendingReward = Math.max(1, Math.round(distTicks * o.targetR)) * o.mintick;
      events.push({ type: 'signal', side, close: b.c, distance: pendingDistance, reward: pendingReward, t: b.t });
    }
  }

  return { events, active, pending, planSide, entry, distance, reward, entryT };
}

const decimals = (mintick) => Math.max(0, Math.round(-Math.log10(mintick)));

export function formatEvent(ev, { tfMin, tickerid, mintick, now }) {
  const fx = (v) => v.toFixed(decimals(mintick));
  const kh = (ms) => {
    const d = new Date(ms + 7 * 3600 * 1000);
    const p = (x) => String(x).padStart(2, '0');
    return `${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())} ${p(d.getUTCHours())}:${p(d.getUTCMinutes())} KH`;
  };
  if (ev.type === 'signal') {
    return `${ev.side === 1 ? 'BUY' : 'SELL'} SETUP | ${tickerid} ${tfMin}m | v7 breakout confirmed at candle close ${fx(ev.close)}. Wait for the next candle open for the entry.
Planned SL distance ${fx(ev.distance)}, TP distance ${fx(ev.reward)}. The entry alert with exact levels follows.`;
  }
  if (ev.type === 'entry') {
    const ageMin = Math.max(0, Math.floor((now - ev.t) / 60000));
    return `${ev.side === 1 ? 'BUY' : 'SELL'} | ${tickerid} ${tfMin}m | Chart entry ${fx(ev.entry)} | SL ${fx(ev.sl)} | TP ${fx(ev.tp)} | Anchor distances to your MT5 fill. Ignore if already in a position or late.\nCandle opened ${kh(ev.t)} (${ageMin} min ago).`;
  }
  return `${ev.reason} | ${tickerid} ${tfMin}m | Check your actual MT5 position.\nPlan was ${ev.side === 1 ? 'BUY' : 'SELL'} ${fx(ev.entry)} / SL ${fx(ev.sl)} / TP ${fx(ev.tp)}.`;
}
