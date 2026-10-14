# Gold Cent Guard validation - October 14, 2026

## Verified

- The source uses Pine v6 and was accepted by TradingView's editor, saved privately as **Gold Cent Guard v1 - Manual M15**, and found again in **Indicators → My scripts** after reloading the browser.
- The saved program runs on ordinary **OANDA:XAUUSD, 15 minutes**. EMA20/50/200, historical setup triangles and the status/risk table rendered without a compiler or runtime error.
- The program's first-bar self-checks executed successfully: downward cent-lot sizing, a budget too small for minimum volume, zero stop distance, the starting budget, the $5 equity floor, remaining daily allowance, and Cambodia Friday/weekend/session boundaries.
- Historical expired-candidate handling was observed: **WAIT: no fresh setup**, expiry timestamp, and hidden current entry/SL/TP values. No historical trade results or performance statistics are generated.
- Entering **500 USC** in the running program produced **STOP: $5 equity floor**, **$0.000 / 0.0 USC** budget and **$5.00** entered equity. This was a test input, not a broker balance update; see `validation-equity-floor.jpg`.
- Entering **20 USC** daily loss with **1,000 USC** equity produced **STOP: daily limit** and a zero budget; see `validation-daily-limit.jpg`. Equity/loss inputs were restored to **1,000 / 0**, with quotes/reserve zero and news unchecked for research handoff.
- The narrow-browser preview at **390 × 844** revealed an overlap with the top chart legend. The panel was moved to the lower-right corner, recompiled/saved and checked again. See `preview-phone-width.jpg`. This is a browser-width check, not a physical-phone/native-app test.
- Account values and permissions remain manual inputs. No Exness connection, order placement, publication, paid subscription or VPS was created.

The existing chart's RSI is retained, and its saved layout was not overwritten by this installation. The chart remains open as an unsaved working view; the indicator itself is saved privately in My scripts.

Final source SHA-256: `8c25efccde6b3a9453bbfccb528e8f773399361454632a5a8bcee565bb478b4a` (128 lines).

## Remaining verification

No qualifying live setup arrived during the check, so the full fresh-candidate quote/news/size flow was not exercised against a live Exness fill. Current Exness volume step, stop constraints and margin remain manual checks. A historical profitability backtest and forward-testing are still required; successful compilation and risk checks do not establish a profitable strategy.
