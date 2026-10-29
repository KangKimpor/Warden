import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/index.js';

const MIN = 60000;
const tf = 15;
// Tuesday so the market-hours gate is open.
const T0 = Date.UTC(2026, 0, 6, 0, 0) - 262 * tf * MIN;

function build(withEntryBar) {
  const rows = [];
  let p = 1000;
  for (let i = 0; i < 260; i++) {
    p += 0.2;
    rows.push([T0 + i * tf * MIN, p - 0.1, p + 0.5, p - 0.5, p]);
  }
  rows.push([T0 + 260 * tf * MIN, 1052, 1053, 1051.5, 1052.8]); // breakout signal bar
  if (withEntryBar) rows.push([T0 + 261 * tf * MIN, 1053.0, 1053.4, 1052.5, 1053.1]);
  return rows;
}

const fmt = (ms) => new Date(ms).toISOString().slice(0, 19).replace('T', ' ');

function setup(rows) {
  const sent = [];
  globalThis.fetch = async (url, init) => {
    const u = String(url);
    if (u.includes('twelvedata')) {
      const interval = new URL(u).searchParams.get('interval');
      const data = interval === '15min' ? rows : [];
      return new Response(JSON.stringify({
        status: 'ok',
        values: data.map(([t, o, h, l, c]) => ({ datetime: fmt(t), open: String(o), high: String(h), low: String(l), close: String(c) })),
      }));
    }
    if (u.includes('api.telegram.org')) {
      sent.push(JSON.parse(init.body).text);
      return new Response('{}', { status: 200 });
    }
    throw new Error('unexpected fetch ' + u);
  };
  const store = new Map();
  const env = {
    TWELVE_DATA_KEY: 'k', TELEGRAM_TOKEN: 't', TELEGRAM_CHAT_ID: 'c', SYMBOL: 'XAU/USD', MINTICK: '0.001',
    STATE: { get: async (k) => store.get(k) ?? null, put: async (k, v) => void store.set(k, v) },
  };
  return { env, sent };
}

async function tick(env, scheduledTime) {
  let p;
  await worker.scheduled({ scheduledTime }, env, { waitUntil: (x) => (p = x) });
  await p;
}

test('sends one BUY alert after the entry candle opens, then dedupes', async () => {
  const { env, sent } = setup(build(true));
  const now = T0 + 261 * tf * MIN + 1 * MIN;
  await tick(env, now);
  assert.equal(sent.length, 2);
  assert.match(sent[0], /^BUY SETUP \| XAU\/USD \(Twelve Data\) 15m/);
  assert.match(sent[0], /Check vs chart: close [\d.]+ > 24-candle high [\d.]+ \| EMA50 [\d.]+ \| EMA200 [\d.]+ \| ATR14 [\d.]+/);
  sent.shift();
  assert.equal(sent.length, 1);
  assert.match(sent[0], /^BUY \| XAU\/USD \(Twelve Data\) 15m \| Chart entry 1053\.000 \| SL \d+\.\d{3} \| TP \d+\.\d{3}/);
  await tick(env, now + 5 * MIN);
  assert.equal(sent.length, 1, 'same events are not re-sent');
});

test('only the setup heads-up before the entry candle appears', async () => {
  const { env, sent } = setup(build(false));
  await tick(env, T0 + 261 * tf * MIN - 1 * MIN + 2 * MIN); // signal bar closed, next bar row absent
  assert.equal(sent.length, 1);
  assert.match(sent[0], /^BUY SETUP/);
});

test('stale history is not announced', async () => {
  const { env, sent } = setup(build(true));
  await tick(env, T0 + 261 * tf * MIN + 4 * 60 * MIN);
  assert.equal(sent.length, 0);
});

test('data failure sends one outage warning per hour', async () => {
  const sent = [];
  globalThis.fetch = async (url, init) => {
    if (String(url).includes('twelvedata')) return new Response(JSON.stringify({ status: 'error', message: 'bad key' }));
    sent.push(JSON.parse(init.body).text);
    return new Response('{}');
  };
  const store = new Map();
  const env = { TELEGRAM_TOKEN: 't', TELEGRAM_CHAT_ID: 'c', STATE: { get: async (k) => store.get(k) ?? null, put: async (k, v) => void store.set(k, v) } };
  const now = Date.UTC(2026, 0, 6, 12, 1);
  await tick(env, now);
  await tick(env, now + 5 * MIN);
  assert.equal(sent.length, 1);
  assert.match(sent[0], /bad key/);
});
