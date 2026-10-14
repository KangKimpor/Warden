# SH Gold Signals v2 validation — October 14, 2026

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
