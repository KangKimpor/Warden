# SH Gold Signals v3 validation — October 14, 2026

V3 was saved privately in the existing TradingView account, reopened after a browser refresh, compiled with Pine v6, and run on ordinary **OANDA:XAUUSD M15 and M5**. It replaces the chart's v2 instance; the private v2 script remains available. The existing layout was saved on M5 with RSI retained. Style → Trades on chart was disabled to hide simulated fill markers while keeping BUY/SELL candidate labels and the price panel. The Pine first-bar sizing, budget, zone, confirmation-window, cooldown and Cambodia-session checks ran without a runtime error. `git diff --check` passed.

The frequency change is an eight-hour FVG zone lifetime, confirmation on the touch candle or next three candles, plus EMA20–EMA50 trend pullbacks. A three-candle cooldown merges nearby candidates. M5 uses a five-minute next-candle entry window; M15 retains fifteen minutes. Signals still require candle close. Every-tick calculation updates the live expiry panel without enabling intrabar entries.

## Observed chart tests

Default simulation: $10 initial equity, $0.10 maximum / 1% equity risk, $0.50 per ounce round-trip cost proxy, $0.20 daily losing-P/L allowance, two order attempts per Cambodia day, one position and $5 new-entry equity floor. The size-guide equity input does not set simulated initial capital.

| Version / chart | Report range shown | Technical candidates | Fit a static $10 budget | Closed trades | Total P/L shown | Win rate | Profit factor | Max drawdown shown |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| V2 M15, rerun unchanged | July 1–October 14 | 4 | 0 | 0 | No trades | — | — | — |
| V3 M15 | July 1–October 14 | 135 (104 EMA, 31 FVG) | 23 | 17 | −$0.84 / −8.40% | 11.76% (2/17) | 0.266 | $0.98 / 9.69% |
| V3 M5 | September 14–October 14 | 124 (99 EMA, 25 FVG) | 90 | 38 | About +$0.37 / +3.68% | 39.47% (15/38) | 1.199 | $0.81 / 7.44% |

The M5 snapshot was taken around **18:48 Cambodia time**, with **one additional open simulated short** entered at 17:30. Total P/L includes its changing unrealized P/L, so it is not a final closed-trade result. Closed gross profit/loss were displayed as $2.04 / $1.70 (rounded). The two timeframes have different loaded-history ranges and cannot be compared as equal-period returns. Report ranges describe history available to the chart, not broker tick data. Counts are technical candidates; static $10 affordability ignores changing simulated equity, daily loss, order limits and fill eligibility. Neither count is a count of real trades.

The latest M5 candidate observed was a SELL on the **18:25–18:30** candle: entry 4139.265, SL 4144.259, stop distance 4.994, estimated 0.01 cent lot at the static $10 budget. It expired at **18:35**. Logs prefix the candle-open timestamp, so add five or fifteen minutes for confirmation time.

**More signals were achieved: M15 increased from 4 to 135 candidates in the same displayed period. Profitability was not established.** M15 lost money; M5's small, partly unrealized gain is insufficient evidence of an edge. Treat both as demo research. No parameters were selected by repeatedly optimizing profit, and no live broker order was submitted.

## Alerts and limitations

`alert()` calls compile and contain direction, feed, timeframe, setup type, entry/SL/TP and Cambodia expiry. Events are emitted only at candle close. Actual delivery was not tested: TradingView Basic offers price alerts, not custom script alerts. No technical alert or paid plan was activated. The manual price-alert procedure is in `SH_STRATEGY.md`; price reminders do not follow EMA values or prove a BUY/SELL candidate exists. Phone delivery and physical-phone layout remain unverified.

No actual Exness fills, measured spread, swap, tick/slippage reconstruction, news filtering, unseen-period validation or forward demo results are available. Simulated guards cannot enforce account limits in MT5. Default costs and margin remain illustrative assumptions. Existing Telegram exports, statements and their analysis were not modified by this update.

Final v3 source SHA-256: `0b21d0076ac10125a0fd2ecfa979a0d98892655cdc39754529e66d0d8af7e6d2`.

---

# SH Gold Signals v2 validation — October 14, 2026 (archive)

Saved privately in the existing TradingView account as **SH Gold Signals v2**, reopened through My scripts after refresh, and accepted by Pine v6. It runs on ordinary **OANDA:XAUUSD M15**. Existing RSI remains. The original Gold Cent Guard script is preserved. No broker connection, actual order, paid plan or public publication was created.

Pine's first-bar checks ran without a runtime error: downward cent-volume sizing, a too-wide stop, zero distance, $5 equity floor, remaining daily allowance, first-zone-bar exclusion, 32-bar expiry, directional invalidation, overlap/non-overlap and Cambodia weekday/session boundaries.

An initial display issue was corrected: strategies do not necessarily execute on the currently open realtime candle, so the panel now renders on `barstate.islastconfirmedhistory` as well as the last bar. Historical prices are retained with an explicit **EXPIRED** label.

## Exploratory $10 test

TradingView's selected report range was **July 1–October 14, 2026**. The test concerns the history available to the chart, not complete broker tick history or replay of all Telegram signals. The final Pine logs reported **4 technical candidates**, chart guard true, point value **1**, minimum contract **0.01**. Both BUY and SELL branches produced candidates. No eligible simulated orders occurred: all four minimum sizes exceeded the $0.10 budget at the default $0.50 per ounce cost allowance.

| Candidate candle close, Cambodia time | Side | Reference entry | SL | Stop distance / oz | Minimum loss incl. allowance |
|---|---|---:|---:|---:|---:|
| Aug 3, 20:15 | SELL | 4038.990 | 4056.246 | 17.256 | $0.17756 |
| Aug 7, 16:45 | BUY | 4317.525 | 4298.929 | 18.596 | $0.19096 |
| Sep 3, 18:45 | BUY | 4438.730 | 4425.014 | 13.716 | $0.14216 |
| Sep 14, 14:30 | SELL | 4317.045 | 4327.015 | 9.970 | $0.10470 |

Pine log prefixes are candle-open timestamps; the table adds 15 minutes to show confirmation times. The latest candidate's TP1/TP2 are **4307.075 / 4297.105**. The chart panel correctly displays **SELL — EXPIRED** and **SKIP: minimum lot too large**.

**This test provides no win rate, profit factor, or evidence of profitability.** Four rejected candidates cannot establish an edge. Do not increase the risk budget or tighten technical stops merely to manufacture a trade. This baseline is currently suitable for observation, with insufficient evidence for funded use on a $10 account.

The cost proxy is $0.25 per ounce per side, margin 0.05%, one position, two order attempts/day, a $0.20 daily losing-P/L allowance and a $5 new-entry floor. Tick/slippage/news/swap behavior and actual Exness fills remain unverified. The simulation's daily accounting and fill lifecycle were not exercised by completed orders in this sample.

All six SH HTML files were rehashed and match the prior inventory. Text evidence and linked source image names are retained in `sh_evidence.json`. Original exports and statements are unchanged.

The panel was checked at 390 × 844 browser width. A candle-overlap issue was fixed by putting the overlay in front of the chart (`behind_chart=false`) and re-adding the saved script. This is a browser preview, not a native phone test. Desktop and phone previews are `sh-preview-desktop.jpg` and `sh-preview-phone.jpg`; both show historical, expired reference levels.

Final source SHA-256: `ce36c9795c2e61c9866e3b9791e289ca24c94627ebd6d89f19ad8b17e3e0e427`. The Pine file contains its own executed self-checks and candidate diagnostic logs. No separate dependency or testing framework was introduced.
