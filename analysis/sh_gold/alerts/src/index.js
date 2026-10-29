import { runV7, formatEvent } from './v7.js';

// Gold Entry v7 runs on M15 and H1; each timeframe is evaluated independently.
const TIMEFRAMES = [
  { min: 15, interval: '15min', size: 1200 },
  { min: 60, interval: '1h', size: 700 },
];

const MIN = 60000;

// Spot gold is closed from Friday 22:00 UTC to Sunday 22:00 UTC; skip those polls to save API credits.
export function marketOpen(now) {
  const d = new Date(now);
  const day = d.getUTCDay();
  const h = d.getUTCHours();
  if (day === 6) return false;
  if (day === 5 && h >= 22) return false;
  if (day === 0 && h < 22) return false;
  return true;
}

async function fetchBars(env, tf) {
  const url = new URL('https://api.twelvedata.com/time_series');
  url.search = new URLSearchParams({
    symbol: env.SYMBOL || 'XAU/USD',
    interval: tf.interval,
    outputsize: String(tf.size),
    order: 'asc',
    timezone: 'UTC',
    apikey: env.TWELVE_DATA_KEY,
  }).toString();
  const res = await fetch(url);
  const body = await res.json();
  if (body.status === 'error' || !Array.isArray(body.values)) {
    throw new Error(`Twelve Data ${tf.interval}: ${body.message || res.status}`);
  }
  return body.values
    .map((v) => ({
      t: Date.parse(v.datetime.replace(' ', 'T') + 'Z'),
      o: Number(v.open),
      h: Number(v.high),
      l: Number(v.low),
      c: Number(v.close),
    }))
    .filter((b) => Number.isFinite(b.t) && [b.o, b.h, b.l, b.c].every(Number.isFinite))
    .sort((a, b) => a.t - b.t);
}

async function telegram(env, text) {
  if (env.DRY_RUN === 'true') {
    console.log('[dry run] ' + text);
    return;
  }
  const res = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text }),
  });
  if (!res.ok) throw new Error(`Telegram ${res.status}: ${await res.text()}`);
}

const eventKey = (tf, ev) => (ev.type === 'end' ? `${tf.min}|end|${ev.entryT}` : `${tf.min}|${ev.type}|${ev.t}`);

async function handleTimeframe(env, tf, now) {
  const bars = await fetchBars(env, tf);
  const options = {
    sessionOnly: env.SESSION_ONLY === 'true',
    mintick: Number(env.MINTICK) || 0.001,
  };
  const { events } = runV7(bars, tf.min, now, options);

  // Only announce recent events; older ones are history, or were already sent.
  const horizon = now - 3 * tf.min * MIN;
  const sentRaw = await env.STATE.get(`sent:${tf.min}`);
  const sent = sentRaw ? JSON.parse(sentRaw) : [];
  const fresh = events.filter((ev) => ev.t >= horizon && !sent.includes(eventKey(tf, ev))
    && !(ev.type === 'signal' && env.SIGNAL_ALERT === 'false'));

  for (const ev of fresh) {
    await telegram(env, formatEvent(ev, {
      tfMin: tf.min,
      tickerid: `${env.SYMBOL || 'XAU/USD'} (Twelve Data)`,
      mintick: options.mintick,
      now,
    }));
    sent.push(eventKey(tf, ev));
    await env.STATE.put(`sent:${tf.min}`, JSON.stringify(sent.slice(-40)));
  }
}

// Setup check: deploy with TEST_PING=true to get one Telegram message per run with the latest candles.
async function testPing(env) {
  const lines = [];
  for (const tf of TIMEFRAMES) {
    const bars = await fetchBars(env, tf);
    const b = bars[bars.length - 1];
    lines.push(`${tf.min}m: ${bars.length} candles, latest ${new Date(b.t).toISOString().slice(0, 16)}Z close ${b.c}`);
  }
  await telegram(env, `Gold Entry v7 alerts: setup OK.\n${lines.join('\n')}`);
}

async function run(env, now) {
  if (env.TEST_PING === 'true') {
    try {
      await testPing(env);
    } catch (e) {
      console.error(e);
      await telegram(env, `Gold Entry v7 alerts: setup test failed.\n${e.message}`).catch(() => {});
    }
    return;
  }
  if (!marketOpen(now)) return;
  const results = await Promise.allSettled(TIMEFRAMES.map((tf) => handleTimeframe(env, tf, now)));
  const failures = results.filter((r) => r.status === 'rejected').map((r) => String(r.reason?.message || r.reason));
  if (!failures.length) return;
  console.error(failures.join('; '));

  // A silent outage means missed signals, so say so, at most once an hour.
  const last = Number(await env.STATE.get('lastErrorAlert')) || 0;
  if (now - last >= 60 * MIN) {
    try {
      await telegram(env, `Gold Entry v7 alerts: data or Telegram error, signals may be missed.\n${failures.join('\n')}`);
      await env.STATE.put('lastErrorAlert', String(now));
    } catch (e) {
      console.error('error alert failed', e);
    }
  }
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(run(env, event.scheduledTime || Date.now()));
  },
};
