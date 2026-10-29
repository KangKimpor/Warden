# Gold Entry v7 - Telegram alerts (Cloudflare Worker)

Sends the same BUY/SELL entry and plan-ended alerts as the TradingView indicator
[gold_entry_v7.pine](../indicator/gold_entry_v7.pine), without a paid TradingView plan and without
your PC running. The indicator is unchanged; `src/v7.js` is a line-by-line port of its logic
(24-bar breakout + EMA50/EMA200 filter, entry at next candle open, SL = ceil(ATR14 x 1.5), TP = 2x SL,
24-bar plan lifetime, one plan at a time, SL/TP/time exit). It checks M15 and H1 independently.

Messages you get: a **SETUP** heads-up when the v7 triangle appears at a candle close, the **entry** alert
(v7's own `alert()` text) when the next candle opens, and the **plan ended** alert (SL / TP / time exit).
Set `SIGNAL_ALERT = "false"` in `[vars]` to drop the heads-up. `TEST_PING=true` (deploy with
`--var TEST_PING:true`) sends a one-off setup check instead.

Runs every 5 minutes (UTC `:01, :06, ...`, Sunday-Friday, skipped while gold is closed) and polls
Twelve Data for XAU/USD. Free tiers cover it: about 550 Twelve Data credits/day (limit 800) and a
handful of KV writes.

## One-time setup

1. **Telegram bot.** In Telegram message `@BotFather`, send `/newbot`, keep the token.
   Send any message to your new bot, then open
   `https://api.telegram.org/bot<TOKEN>/getUpdates` and copy `message.chat.id`.
2. **Twelve Data key.** Free account at twelvedata.com, copy the API key.
3. Install and log in (from this folder):

   ```bash
   npm install
   npx wrangler login
   ```

4. **KV namespace** (stores which alerts were already sent):

   ```bash
   npx wrangler kv namespace create STATE
   ```

   Paste the printed `id` into `wrangler.toml` in place of `REPLACE_WITH_KV_NAMESPACE_ID`.
5. **Secrets** (each command prompts for the value; they never go in a file):

   ```bash
   npx wrangler secret put TELEGRAM_TOKEN
   npx wrangler secret put TELEGRAM_CHAT_ID
   npx wrangler secret put TWELVE_DATA_KEY
   ```

6. Deploy:

   ```bash
   npx wrangler deploy
   ```

Quick Telegram check before deploying (replace the placeholders):
`curl "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=test"`.

## Settings (`wrangler.toml` `[vars]`)

| Var | Default | Meaning |
|---|---|---|
| `SESSION_ONLY` | `false` | Same as the indicator's "Signals only 14:00-23:00 Cambodia weekdays" input. v7's default is off. Match whatever your chart uses. |
| `MINTICK` | `0.001` | Price tick used to round SL/TP (OANDA XAUUSD on TradingView shows 3 decimals). |
| `SYMBOL` | `XAU/USD` | Twelve Data symbol. |
| `DRY_RUN` | `false` | `true` logs messages instead of sending to Telegram. |

The other indicator inputs (lookback 24, SL 1.5 ATR, TP 2R, plan lifetime 24 bars) are the defaults in
`src/v7.js`. If you changed them on your chart, tell me and they go into config.

## Differences from TradingView you should know about

- **Different price feed.** Twelve Data's XAU/USD is not the OANDA/Exness feed, so candles, breakout
  timing, ATR and therefore SL/TP can differ a little from your chart. Like the indicator says, anchor
  the distances to your MT5 fill. Compare the first few alerts with your chart.
- **Up to ~5 minutes latency** for SL/TP/time-exit notices (poll interval). The entry alert arrives
  within about 1-5 minutes of the new candle opening; the message says how old the candle is.
- **History window.** The Worker replays the last 1200 M15 / 700 H1 candles each poll, not TradingView's
  full history. Indicators converge, but the "which plan is currently active" chain can differ from your
  chart right after a plan boundary.
- If Twelve Data or Telegram fails, you get one warning message per hour instead of silence.

## Tests

```bash
npm test
```

Covers the indicator's own self-checks, ATR/EMA seeding, long and short entries, SL/TP/both/time exit,
the one-plan-at-a-time rule, Cambodia session filter, market-hours gate, and the Worker flow with mocked
Twelve Data and Telegram (single alert, de-duplication, stale-history suppression, outage warning).
It does not compare against real TradingView output, since TradingView doesn't export that on a free plan.
