# Gold Cent Guard v1 (archive)

The current SH-based version is **SH Gold Signals v4**, for M5 or M15, using all 359 gold candidates, completed H1 direction, feed-day open/pivot context and a net reward/risk check. See [SH_STRATEGY.md](SH_STRATEGY.md) for installation, exact rules, free-plan price reminders and risk limits, and [SH_VALIDATION.md](SH_VALIDATION.md) for test evidence. Version 1 below is retained as an archive.

A private TradingView Pine v6 indicator for manual XAUUSDc trading practice. It does not place orders, monitor Exness, enforce account limits in MT5, or claim profitability.

## Open it on your phone

1. Sign in to the same TradingView account used here.
2. Open an ordinary XAUUSD candlestick chart (the validation chart uses OANDA:XAUUSD) and select **15 minutes**.
3. Open **Indicators → My scripts → Gold Cent Guard v1 - Manual M15**. If it is already on your saved chart, do not add a duplicate.
4. Open its settings and update the manual inputs. The default **1,000 USC = $10** is your proposed learning account, not a reading of your current Exness balance.
5. Use it for observation/demo practice first. A triangle is an historical price setup, not an executed trade or proof of a profitable opportunity.

Backup source: `gold_cent_guard.pine`. Through TradingView's browser Pine Editor, create an indicator, replace the template with this entire file, save privately, and select **Add to chart**. Never select Publish script for installation.

## What it shows

- EMA20/50/200 and long/short pullback-confirmation triangles only after M15 candles close.
- Candidate generation Monday–Friday, **14:00–23:00 Cambodia time**, checked at the signal candle's close. This session is a proposed research window, not an optimized one.
- Technical SL: lowest/highest of five completed candles, plus a 0.2 × ATR(14) buffer, rounded outward to the chart's price tick.
- Latest candidate entry/SL and a full-position 2R target, plus a cent-lot estimate and loss in USD and USC.
- Candidate expiry **15 minutes after confirmation**. It cannot remain fresh beyond the 23:00 session end. The timestamp remains visible as expired, while its price/risk values disappear.
- An explicit chart-feed label. TradingView's feed is not your Exness execution feed.

Historical triangles are independent of today's manually entered account/news checks. They are not a backtest. Changing equity or news inputs must not be interpreted as retrospectively qualifying earlier setups.

## Manual inputs: refresh before each candidate

| Input | What to enter |
|---|---|
| Current equity | Actual equity in **USC**, including floating P/L. 1,000 USC is $10; 500 USC is $5. |
| Loss used today | Sum of today's losing P/L in USC; do not use later wins to erase this loss allowance. Include losses on open exposure conservatively. Reset at the next Cambodia calendar day, not after a win. |
| Trades taken today | Actual entries today, including trades taken without this indicator. Reset at the next Cambodia calendar day. |
| Open position | Check while any position is open. The indicator cannot detect it. |
| MT5 entry quote | Copy the current **Ask for BUY** or **Bid for SELL** from XAUUSDc. Gold quotes remain dollars per ounce, not cents. Replace the quote for every candidate and refresh it if price changes. |
| Extra cost reserve | A positive, conservative dollar-price allowance **per ounce** for adverse slippage and costs not already captured by the entry-to-stop calculation. For example, 0.50 means $0.50 per ounce, not $0.50 per trade. Do not automatically add entry spread again when already reflected in the executable quote. Zero is treated as unchecked. |
| News check | Check only after verifying no restricted USD event now: CPI/NFP within 30 minutes before/after; FOMC from 30 minutes before its release until 60 minutes after the scheduled press conference starts. Uncheck if uncertain. |

No inputs are synchronized or reset from Exness. A saved quote/news check can become stale. The script has no live event calendar, so you must refresh those checks for each candidate. Do not select the news check merely to make a signal appear.

## Risk model and statuses

The cent-lot model is fixed to **one ounce per XAUUSDc cent lot**, with a **0.01 cent-lot minimum and step**. Your supplied statement corroborates the ounce exposure; verify current minimum, step and stop rules in MT5 before use. It is not a model for standard gold lots, other instruments, or another broker's cent convention.

Budget in USD is the smallest nonnegative value of:

- $0.10;
- 1% of entered current equity;
- entered equity above the fixed **$5 floor**;
- the remaining **$0.20 daily loss allowance**.

Size is rounded **down** to 0.01 cent-lot steps using entry-to-stop distance plus the extra cost reserve. If the minimum size cannot fit, it shows **SKIP**, rather than raising risk or moving the stop. Positive cost reserves exceeding 10% of the original price risk also block review. The 2R target uses actual entered quote-to-stop distance and excludes the reserve; realized net reward can therefore be less than 2R.

Example: entry 100, stop 95, reserve 0.50, budget $0.10 → 0.01 cent lot, estimated loss $0.055 = 5.5 USC. Entry 100, stop 88 with the same budget/reserve → minimum-volume risk $0.125, so skip.

| Status | Meaning |
|---|---|
| USE XAUUSD, 15m, candles | Wrong instrument, timeframe or chart type. |
| WAIT | No fresh candidate, insufficient history, or an entered open position. |
| STOP | Entered equity is at/below 500 USC, two entries used, or 20 USC daily loss used. |
| CHECK / ENTER | News, current executable quote or cost allowance still needs review. |
| SKIP | Quote is beyond the stop, or minimum cent volume cannot fit the budget. |
| REVIEW BUY / SELL | The entered values pass these limited checks. You must still verify the actual broker SL/TP, allowed volume, margin, quote freshness and feed difference. This is not an instruction to trade. |

For a fresh $10 account without additional cash flows, the $5 floor corresponds to your requested $5 total-loss limit. Deposits, withdrawals or changing the starting amount require revisiting this fixed model. The indicator does not close a position at the floor. Keep your protective stop in MT5; gaps/slippage can exceed the estimate.

## First use

Observe and journal at least 20 eligible/rejected candidates before considering real entries. This is an operating check, not a sufficient profitability test. Record candidate time, screenshot, executable MT5 quote, SL/TP, size, estimated/actual loss and skip reason. Count every actual entry toward the two-per-day cap. If later testing does not show positive expectancy after execution costs, keep the tool in research.

On the free TradingView plan, use visible chart marks and available price alerts as reminders to review. This version does not promise custom technical push alerts. Actual installation and use on your physical phone have not been verified here.

## Verification

The Pine program runs assert-like checks on its first bar for cent conversion, downward lot rounding, minimum-size rejection, zero stop distance, daily/total-budget exhaustion, and Cambodia weekday/session boundaries. A failed check raises a runtime error. Compiler and chart checks are recorded separately in `validation.md`.

No historical performance backtest, Exness order execution, or physical-phone test was performed. The file is a working research indicator, not a certified trading system.
