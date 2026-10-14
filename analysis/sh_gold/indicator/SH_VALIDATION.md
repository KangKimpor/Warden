# SH Gold Signals v5 validation — October 14, 2026

## Late entry and wide-stop correction

The supplied screenshot shows a SELL tag at the high of a large bearish candle. V4 confirmed only after close, used that close as its limit price, and drew the tag at the high. This presentation implied an earlier entry, while the close-to-swing stop could be large. V5 uses a next-candle retest limit at the previous high (BUY) or low (SELL), places the label at that exact planned entry on the following candle, and states the order type and price. This is a plan, not a claimed fill or an intrabar prediction.

The shared candidate guard rejects wrong-side limits/stops, confirmation ranges over 2 times prior ATR(14), stops over 1.5 times prior ATR, and stops over the configured dollar cap (default $5/oz). Original swing/zone stops remain intact; no stop is tightened merely to fit the cap. Both visuals and simulated orders use the same accepted entry and stop. At default settings TP1 is at most $5/oz away and TP2 at most $10/oz away. These caps are proposed practical bounds, not optimized or recovered SH parameters.

The panel names the chart feed and the user's stated XAUUSDc cent symbol, shows dollar-per-ounce distances separately from exact tick prices, and blocks new-entry review once the chart has touched the limit or reached TP1 during its next-candle window. A chart touch does not verify a broker fill. Existing size, estimated net-R, account and session guards remain in place. Gray SKIP labels fail static size/cost eligibility. Historical labels still do not enforce actual MT5 account limits.

## Verification and exploratory results

V5 compiled privately in Pine v6 on standard OANDA:XAUUSD M5 and M15. The saved editor source was copied back and exactly matched the local file after newline normalization. First-bar checks passed for sizing, budgets, zones, session, direction, reward and both limit sides, including rejection of a 20-point spike against 3-point prior ATR, excessive stops, wrong-side stops/limits and missing volatility. The chart feed's tick precision is retained. Source/doc whitespace checks passed. The existing layout was saved on M5 with v5, explicit limit-price markers and the new feed/distance rows; simulated trade markers are hidden. The private v4 copy remains available.

| Chart | Report range shown | Accepted plans | Static $10 size + net-R eligible | Rejected late/wide/invalid confirmations | Closed trades | Net P/L | Win rate | Profit factor | Max drawdown |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| M5 | September 14–October 14 | 35 (32 EMA, 3 FVG) | 31 | 42 | 13 | +$0.23 / +2.25% | 46.15% (6/13) | 1.376 | $0.32 / 3.16% |
| M15 | July 1–October 14 | 10 (9 EMA, 1 FVG) | 10 | 130 | 4 | +$0.16 / +1.63% | 50.00% (2/4) | 2.515 | $0.07 / 0.67% |

Observed around 21:03–21:05 Cambodia time with $10 initial capital, the default $5 stop cap and $0.25/oz/side commission proxy. Both trade lists show closed latest trades and no open trade. For example, M5's October 14 15:25 candle generated the short plan at its 15:30 close; the simulator entered on the 15:30 candle at 4150.395 and exited at 15:55. M15's October 13 13:45 confirmation generated the plan at 14:00; its simulated entry is on the 14:00 candle. The limit is not filled retrospectively on its confirmation candle.

The rules were fixed before viewing returns; no profit-driven threshold search was performed. Rejected confirmations do not start the accepted-signal cooldown, so these counts are not a one-to-one partition of v4 candidates. A label is not a fill; an unfilled limit expires after one candle and still consumes a simulated daily order attempt. The reported periods differ between timeframes, prices use TradingView's assumed intrabar paths rather than broker ticks, and the cost allowance is not a measured spread. Only 17 trades across unequal periods is insufficient to establish an edge. **Profitability gate remains unproven: demo/research only pending unseen-period and forward execution evidence.**

Final v5 source SHA-256: `7b496cf0a942f6be22ec63333f466b7515afac818baa14b88cd5355f4ab2fd6d`.

---

# SH Gold Signals v4 validation — October 14, 2026 (archive)

## Scope correction and evidence

All **359 non-crypto price candidates** now form the gold evidence population: 54 explicitly labeled gold and 305 unnamed signals confirmed by the user on October 14. The labels record provenance only. **357** pass price ordering, with median first target **1R**, final target **1.857R** and stop **$15/oz**. The two invalid instructions (4895 and 5106) and unusually wide stop (4774) remain flagged. Explicit BTC/ETH posts are preserved and excluded from gold; message 608 explicitly quotes BTC at 61,100.

The current local SH Data folder's six HTML hashes exactly match the prior inventory. The originals were read without modification. The parser, CSV, JSON, SQLite tables, notebook and report were regenerated consistently; candidate IDs, prices and original message text are unchanged. Counts, cohort medians and crypto exclusion were independently reconciled, and the statement's 51-row closed-balance table was preserved. CSV source text contains original trailing spaces, so whitespace QA excludes that evidence file rather than rewriting quotations.

Four additional linked charts were visually reviewed (messages 1650, 2938, 5610, 5670); evidence is in `sh_evidence.json`. They show OP/pivot context, bearish pullback zones, higher-timeframe sell direction and M15 bullish structure/BOS. Classic daily pivot and H1 EMA20/50 are objective research proxies, not recovered proprietary CRAZII or SH formulas.

## Implementation verification

V4 was saved privately in TradingView, compiled in Pine v6 and run on standard OANDA:XAUUSD M5 and M15. The editor's full source was copied back and exactly matched the local file after newline normalization. First-bar sizing, budget, zone, session, confirmation, cooldown, direction and net-R self-checks passed without a runtime error. Code/document whitespace checks passed. The existing layout was saved on M5 with RSI retained and simulated fill markers hidden; BUY/SELL candidate labels, levels, expiry and the new estimated net-R row remain visible. The original private v3 script remains available.

The new BUY/SELL candidates require completed H1 direction and alignment with the feed-day open and classic prior-day pivot. H1 close/EMAs and prior daily H/L/C use one-bar offsets with `lookahead_on`; only the daily open uses the already-known current value. A 1.5 estimated net-R threshold blocks simulated entries and REVIEW when costs leave too little planned payoff. The cost floor is $0.50/oz consistently in display and simulation. Other sizing, exposure and daily limits remain unchanged. These checks measure alignment and payoff geometry, not the probability of reaching TP.

## Fixed-rule exploratory tests

| Chart | Report range shown | Candidates | Static $10 size + net-R eligible | Closed trades | Net P/L shown | Win rate | Profit factor | Max drawdown shown |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| M5 | September 14–October 14 | 71 (58 EMA, 13 FVG) | 49 | 26 | −$0.03 / −0.31% | 34.62% (9/26) | 0.976 | $0.35 / 3.45% |
| M15 | July 1–October 14 | 120 (93 EMA, 27 FVG) | 21 | 15 | −$0.69 / −6.85% | 13.33% (2/15) | 0.308 | $0.83 / 8.16% |

Observed around **19:10–19:13 Cambodia time**, default $10 simulation and $0.25/oz/side cost proxy. M5's latest simulated short entered October 14 at 17:30 and closed at its SL at 19:05; the final M5 table shows no open trade. Unlike the earlier v3 M5 snapshot, these M5 figures are closed-trade results. The prior v3 M5 snapshot showed $0.81 drawdown versus v4's $0.35; v3's P/L included an open trade and was captured earlier, so it is not a matched closed-return comparison.

Both variants were tested with the rules fixed before inspecting their results. No threshold search or repeated profit optimization was performed. Candidates are not filled orders; static eligibility does not apply changing equity, day limits or fill conditions. Report dates describe selected/available chart history, not complete broker tick coverage. These tests evaluate the mechanical hypothesis, not a replay of all 359 Telegram instructions. The two timeframes have different histories and cannot be compared as equal-period returns.

**Profitability gate: not passed.** M5 is approximately breakeven with a small loss after the modeled costs; M15 loses money. Lower drawdown does not establish positive expectancy. V4 identifies aligned setups with potential reward, but cannot identify guaranteed profitable entries. Keep it in demo/research until unseen-period and forward results establish an edge after actual costs.

Phone operation, actual Exness fills, measured spreads, financing/swap, news filters and tick/slippage behavior remain unverified. Expiry status updates on chart execution/live ticks; manually check the displayed expiry if quotes are quiet. Script alerts compile but delivery is unavailable on Basic and was not tested. Simulated account guards cannot enforce actual MT5 exposure or daily losses.

Final v4 source SHA-256: `3fdb1cbc57bc906454d51ea45bbefeb491e214ed6fce9bd661f96c52a7b11741`.

---

# SH Gold Signals v3 validation — October 14, 2026 (archive)

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
