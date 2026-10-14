# XAUUSD: revised gold scope and strategy evidence

## Current strategy revision — October 14, 2026

The user confirmed unnamed SH price signals are gold. All 359 non-crypto candidates now inform the strategy, including 357 with valid price ordering. Text versus user-confirmed labels are provenance, not different markets. Explicit BTC/ETH posts remain excluded. The current SH Gold Signals v4 rules add completed H1 direction, feed-day open and a classic previous-day pivot to the existing EMA/FVG pullback confirmation. Estimated net reward/risk must reach 1.5 before simulated entry or a REVIEW status. These are testable definitions inspired by SH, not a recovered proprietary formula or guaranteed profit. See [current rules](indicator/SH_STRATEGY.md) and [measured tests](indicator/SH_VALIDATION.md). Later first-proposal sections below are retained as the original research history, not current installation instructions.

## Executive Summary

- **The statement is profitable overall, but the process is fragile.** Its 64 closed XAUUSDc trades show 40 wins and 24 losses and +233.9 USC (+$2.339). Before the last two trades, net P/L was -$8.02; two overlapping 1-cent-lot buys then earned $10.359. Their size and concentration make that recovery unsuitable as evidence of a repeatable edge.
- **Fix exposure and loss controls first.** The statement records no SL on 43 trades and reconstructs a 59.9% maximum drawdown in closed-trade balance. This is not a measured mark-to-market equity drawdown, which may differ. Your next account is $10 with a $5 maximum total-loss limit; that maximum is a stop boundary, not a risk target.
- **For manual trading on your phone and free TradingView, build one visual Pine indicator.** It should show confirmed setups, entry/SL/TP, price-feed identity and cent-aware risk. You check the chart and place trades in MT5 mobile. Free TradingView does not include custom technical alerts; a desktop MT5 notification setup is an optional later path, not required now.
- **All 359 non-crypto price candidates now inform the gold strategy.** The 305 unnamed signals are gold under your October 14 clarification; 357 of the 359 pass basic price-order checks. Current implementation and test evidence are in indicator/SH_STRATEGY.md and indicator/SH_VALIDATION.md. Neither Telegram TP claims nor exploratory chart backtests establish a profitable edge.

## Your statement shows fragile recovery and excessive exposure

The three-page statement covers August 6–October 14, 2026, but its actual closed trades occur August 10–19. It contains **64 closed XAUUSDc positions**, five cancelled pending orders, and no open trades or working orders at issuance. Dates below use the statement clock because no timezone is supplied.

The statement reconciles exactly in USC: 1,500 deposited - 1,733 withdrawn + 233.9 closed P/L = 0.9 remaining. In real dollars that is **$15 deposit, $17.33 withdrawal, +$2.339 trading P/L and $0.009 balance**. The low ending balance follows a withdrawal and should not be described as the account being blown. The daily activity log had a rounded zero balance and zero recent retrieved orders; it was not a substitute for this statement.

**40 wins and 24 losses means a 62.5% win rate**, so most individual trades in this supplied period actually won. Gross winning P/L is $18.036 and absolute losing P/L is $15.697, giving a 1.149 profit factor. Commission, tax and swap columns are zero; spread is already part of execution prices, not a missing fee that should be subtracted again. This small, clustered sample does not establish an enduring profitable strategy.

**The last two wins change the story.** Removing them as a sensitivity check changes net P/L from +$2.339 to **-$8.02**. They supplied 57.4% of gross winning P/L. This is not a claim they should be removed from actual results; it demonstrates concentration. Each was 1 cent lot, while most prior volumes were 0.1–0.2. They overlapped for about 11 minutes and both show recorded SL = 0. Together they represented approximately two ounces of gold; a $2.50 adverse price move while both were open would cost about $5 before other effects. A winning result does not make that risk suitable for the proposed $10 account.

**Small wins coexist with much larger losses.** Median win is $0.0515 and median absolute loss is $0.618—approximately 12 times as large. The average win is $0.4509 and average loss $0.6540; the large final wins lift the average winner. The median position lasted 131 seconds, and 22 positions lasted under a minute. This pattern motivates testing slower closed-bar entries and predeclared exits; it does not prove a particular exit rule would have improved these trades.

**Protection and clustering need attention.** 43 of 64 trades (67.2%) show no recorded SL, and 36 show neither SL nor TP. The report stores the recorded/final values, not a complete amendment history: we cannot prove whether stops were absent for the whole lifetime or calculate original planned R. There were 20 entries within August 11, 14:06–14:27, and as many as six simultaneous positions in the full statement. Five sell positions closed together on August 19 at 07:05:57 with a combined **-$4.813** result—almost your entire new $5 total-loss limit in one cluster.

Reconstructing balance from the $15 deposit and closed P/L, grouping simultaneous closes, gives a peak of $17.404 and a trough of $6.98 before the final recovery: **$10.424 maximum closed-balance drawdown, or 59.9% of the peak**. The chart ends before the withdrawal, so withdrawing funds is not counted as trading loss. Floating equity and intratrade extremes are unavailable; this is not an equity drawdown measure.

**My interpretation:** the strongest observable problem is uncontrolled exposure and frequent discretionary trading, not simply too few winning entries. The statement cannot establish psychological motives, whether trades followed SH, or the counterfactual performance of a new indicator. Before real-money trials of any signal, rehearse one position, one stop, a fixed small loss budget and at most two entries per day. The new $5 hard stop is 50% of $10; aim to review failures much earlier rather than planning to consume that entire allowance.

## The export is a conversation, not a trading ledger

All six HTML pages were parsed. The unit counted is one ordinary Telegram message with a unique message ID; service messages such as date separators are excluded. The timestamps explicitly carry UTC+07:00, matching Cambodia. The earliest ordinary message is May 5, 2026 at 20:04:58; the latest is October 9 at 19:56:50.

There are 3,798 messages with text and 3,381 with linked media; these groups overlap. Extraction found 359 gold candidates with one textual direction, an entry price or range, a stop and targets. The user confirmed on October 14, 2026 that the unnamed SH price signals are gold: 54 name Gold/XAU and 305 are included under that confirmation. Explicit BTC/ETH headings exist in the export and remain excluded; for example, message 608 explicitly says Short BTC at 61,100. Image-only signals, Khmer-only instructions and ambiguous mixed-direction messages are outside this parser's scope.

**Both chart series are gold.** The series distinguish the source of the instrument label, not different markets. All 359 candidates inform the revised strategy; a zero in the text-labeled series is a naming change. May and October are partial months. These are posted candidates, including reposts, not unique filled trades.

|month|instrument_status|signals|messages|
|---|---|---|---|
|2026-05|Gold: labeled in text|37|346|
|2026-05|Gold: user-confirmed scope|2|346|
|2026-06|Gold: labeled in text|15|1330|
|2026-06|Gold: user-confirmed scope|60|1330|
|2026-07|Gold: labeled in text|2|1271|
|2026-07|Gold: user-confirmed scope|75|1271|
|2026-08|Gold: labeled in text|0|1027|
|2026-08|Gold: user-confirmed scope|68|1027|
|2026-09|Gold: labeled in text|0|1144|
|2026-09|Gold: user-confirmed scope|82|1144|
|2026-10|Gold: labeled in text|0|293|
|2026-10|Gold: user-confirmed scope|18|293|


## Multiple targets make a TP count misleading

Of all 359 gold candidates, 357 pass basic direction/price-order checks. Among those, 348 have multiple targets and 17 have entry ranges. Arrival at a limit entry matters; a move to TP before entry is reached is not a winning filled trade. The two invalid instructions remain flagged.

Across the 357 geometrically ordered gold candidates, median stop distance is **15 gold price dollars per ounce**, with a range of 2–212 (the 212-dollar stop remains flagged). Median first-target reward/risk is **1.0R**; median last-target reward/risk is **1.857R**. R is the original entry-to-stop price distance. For ranges, these descriptive calculations use the first quoted entry endpoint, not an assumed actual fill. They exclude costs and do not describe achieved returns. The former 54-message text-labeled subset had a $12 stop and 2R final-target median; it no longer defines the strategy's evidence population.

For example, message 9 posts a buy at 4550, SL 4535 and targets 4565/4580. These represent 1R and 2R. Taking half off at each would earn 1.5R on a full winner; taking half at 1R and stopping the rest at entry earns only 0.5R before costs. The export does not consistently specify these allocations or the timing of stop changes.

**We cannot calculate an honest win rate, profit factor, expectancy or drawdown from TP mentions.** For the 54 explicit gold candidates, 37 have no directly linked reply; 14 have a directly linked reply mentioning TP and two mention SL. These mention flags can overlap and are not outcome classifications. Unthreaded updates may exist. Across all 359 candidates, 325 have no directly linked reply.

## The extracted entries remain traceable to the export

The table is the first ten chronologically ordered valid gold candidates across both label origins, with original message IDs. It shows planned prices and gross target geometry. It is an audit sample, not a performance sample. Open the corresponding message ID in its original HTML page to inspect the text and context; the full extracted candidate list is saved in signals.csv.

|id|timestamp|side|entry|sl|tp|first_target_R|final_target_R|
|---|---|---|---|---|---|---|---|
|5|2026-05-05T20:04:58+07:00|sell|[4580.0]|[4595.0]|[4565.0]|1.0|1.0|
|9|2026-05-05T23:43:58+07:00|buy|[4550.0]|[4535.0]|[4565.0, 4580.0]|1.0|2.0|
|12|2026-05-06T10:50:30+07:00|sell|[4650.0]|[4665.0]|[4635.0, 4620.0]|1.0|2.0|
|16|2026-05-06T13:34:58+07:00|sell|[4680.0]|[4700.0]|[4660.0, 4650.0, 4640.0]|1.0|2.0|
|26|2026-05-06T16:59:59+07:00|buy|[4680.0]|[4660.0]|[4700.0, 4710.0, 4720.0]|1.0|2.0|
|42|2026-05-06T20:06:10+07:00|buy|[4675.0]|[4655.0]|[4695.0, 4705.0, 4715.0]|1.0|2.0|
|58|2026-05-06T23:44:15+07:00|buy|[4665.0]|[4645.0]|[4685.0, 4695.0]|1.0|1.5|
|71|2026-05-07T15:01:58+07:00|buy|[4740.0]|[4730.0]|[4750.0, 4755.0, 4760.0]|1.0|2.0|
|75|2026-05-07T17:00:31+07:00|sell|[4735.0]|[4755.0]|[4715.0, 4705.0, 4695.0]|1.0|2.0|
|92|2026-05-08T13:07:45+07:00|buy|[4717.0]|[4707.0]|[4727.0, 4737.0, 4747.0]|1.0|3.0|


## Text errors and discretionary updates block automatic copying

**High severity, high confidence:** message 5106, September 23 at 22:03:47, posts Buy 4289 / SL 4379 / TP 4299–4309. The stop is above a buy entry. Message 5110 at 22:06:23 says to adjust SL to 4279. Preserve both versions and their timestamps; applying the correction retroactively would hide approximately three minutes of execution risk.

**High severity, high confidence:** message 4895 quotes '4293-294'. It fails the literal price-order check; the second endpoint may be shorthand, but it was not silently changed to 4294. Message 4774 posts Short 4290 / SL 4502, a 212-dollar stop. It is geometrically possible but unusually wide; confirm whether it is intentional before use. Seven candidates have review flags for order/range issues, unusual geometry or an unparsed parenthetical bonus target. Direction/price ordering passes for 357 of 359 candidates; passing does not establish correctness or profitability.

**High severity, high confidence:** captions and selected charts use different feeds and methods. The May 22 roadmap is an OANDA H4 chart with EMA5 and fixed zones; the August 27 screenshot is an M15 chart with an EMA 20/50/200 lineup and manually drawn areas. A September 2 screenshot uses a suffixed MT5 gold symbol and H4 pending-order levels. Feed differences, chart/server time and human-drawn zones need explicit definitions before code can reproduce them.

**High severity, confidence limited by missing records:** this static export does not establish original-versus-edited signal history, deleted posts, all fills, all losses or the author's complete account history. Repeated price templates occur 18 times beyond their first occurrence among geometrically ordered candidates; these may be new attempts or reposts and were not deduplicated as trades. Two reply references point outside the parsed ordinary-message set; the cause is unknown.

The remediation is a timestamped trade ledger plus broker-price replay, with amendments taking effect only when posted. Reject ambiguous instructions rather than correcting them automatically.

## Test one objective trend-pullback hypothesis first

**This is a proposed research baseline, not a recovered SH rule set or a proven edge.** The EMA periods have visual support in one reviewed chart; the exact trigger, stop buffer, session and exit rules below are our proposed definitions. They have not been optimized or backtested.

1. **Market and clock:** gold on M15, validating the proposed XAUUSDc cent symbol and its exact Exness feed. Only consider entries Monday–Friday between 14:00 and 23:00 Cambodia time; require the entry time to fall inside the window. This is a convenient initial research window, not evidence of the best session. Liquidate the strategy's position at 23:00 at the first available executable quote. Use an explicit UTC+7 conversion rather than assuming the MT5 server clock matches Cambodia.
2. **Trend:** on the completed signal bar, a long requires EMA20 > EMA50 > EMA200 and EMA50 above its previous-bar value. A short requires EMA20 < EMA50 < EMA200 and EMA50 below its previous-bar value. No trade without that ordering. No extra H1 filter in the initial baseline.
3. **Pullback:** the immediately preceding completed candle's high/low range must overlap its EMA20–EMA50 band. For a long, the signal candle closes bullish, above its EMA20 and above the preceding candle's high. For a short, it closes bearish, below its EMA20 and below the preceding candle's low.
4. **Entry model for testing:** simulate one market order on the next M15 bar's first available quote; for actual use, present an alert for your manual review, subject to session, spread/cost and risk checks. Use completed candles only; no retrospective signals, future pivots or intrabar repainting. Allow one position and a maximum of two entries per Cambodia calendar day.
5. **Stop:** for a long, the lowest low of the last five completed bars including the signal bar, minus 0.2 × ATR(14). For a short, the highest high plus 0.2 × ATR(14). Require correct stop placement relative to the actual fill and compliance with broker stop levels. Do not widen a stop after entry.
6. **Exit:** one full-position target at 2 × the actual fill-to-stop distance. No partial exits or automatic break-even changes in this first version. A single exit is easier to evaluate and avoids splitting a minimum-size position. Include the 23:00 time exit in every test.
7. **News and costs:** use a timestamped event calendar. Skip entries 30 minutes before and after scheduled US CPI/NFP; for FOMC skip from 30 minutes before the rate release until 60 minutes after the scheduled press conference starts. If event data or spread information is unavailable, suppress entries. Initially reject trades whose estimated spread, commission and slippage cost exceeds 0.1R. Historical tests need the same event exclusions and actual bid/ask conventions.

The group's FVG, manually drawn trend-line, pivot and liquidity-sweep ideas remain research candidates. They require precise definitions and evidence of incremental benefit before being added. Several correlated visual confirmations do not establish a reliable probability of winning.

## A $10 cent account needs cent-aware risk estimates

You propose $10 capital and manual trades. **$10 corresponds to 1,000 USC.** Exness describes Standard Cent volumes as cent lots, with one cent lot equal to 0.01 standard lot, and lists a 0.01-cent-lot minimum and XAUUSDc availability. It also lists no trading commission for this account type; spread and any applicable financing still matter. [Exness Standard Cent](https://get.exness.help/hc/en-us/articles/17537782786588-Standard-Cent-account)

Combining that lot conversion with the published 100-ounce standard gold contract suggests **one cent lot represents one ounce, and 0.01 cent lot represents 0.01 ounce**. Every one of the 64 statement trades corroborates this exposure within the printed price/P&L rounding tolerance. Current terminal volume step and stop levels remain unchecked. Confirm the symbol's contract size, minimum volume, volume step and profit units before acting. [Exness gold contract](https://get.exness.help/hc/en-us/articles/17854173039388-Commodities)

Under that assumption, at 0.01 cent lot, a $1 move in gold is about $0.01 in account P/L, displayed as 1 USC. A $12 stop therefore risks about **$0.12 = 12 USC = 1.2% of $10**, before spread/slippage. A full 2R target would pay about $0.24 before costs. Gold's quote price stays in dollars per ounce even though account P/L is in cents.

| Proposed account risk | Dollar budget | USC budget | Maximum price stop at 0.01 cent lot before costs |
|---|---:|---:|---:|
| 0.5% | $0.05 | 5 USC | $5 |
| 1% | $0.10 | 10 USC | $10 |
| 2% — illustration, not a recommendation | $0.20 | 20 USC | $20 |

The full gold cohort's median $15 stop would not fit a 1% budget at minimum volume. A conservative 0.5% research budget is likely to suppress many setups at this capital. **Do not increase risk or tighten a technical stop just to get a trade.** Your stated maximum total loss is $5, or 500 USC. For a fresh $10 account with no additional deposits/withdrawals, stop at $5 equity or sooner if the process fails. My proposed initial per-trade ceiling is $0.10 (10 USC, 1% of starting capital), reduced as equity falls; typical $15 stops may therefore require skipping the setup at minimum size. This is a proposed learning rule, not evidence that live trading has a positive expected return.

For a future sizing display, calculate expected loss in account currency from the terminal's actual profit calculation, include costs, and round volume down to its allowed step. Skip a trade that cannot fit minimum volume or margin. Leverage reduces margin requirements, not price-loss exposure. Avoid splitting a minimum-size trade into multiple targets, martingale, averaging down or trying to turn $10 into income.

Proposed controls: one position, at most two entries per Cambodia day, and no new trades after two losses or $0.20 daily loss including open P/L. Pause and review well before the $5 total-loss boundary. Do not add to a losing position or increase size to recover. The daily limit does not supersede the remaining total-loss budget. Gaps/slippage can exceed planned losses. At +2R/-1R, a theoretical break-even win rate is 33.3% without costs or time exits, or 36.7% if every trade costs 0.1R. These figures describe payoffs, not our expected win rate.

## Use a visual TradingView indicator with MT5 mobile execution

| Platform/build | Role for your confirmed setup | Constraint |
|---|---|---|
| One TradingView Pine visual indicator | Recommended chart companion: trend, confirmation, entry/SL/TP and USD/USC risk | You check the chart manually; its gold feed can differ from Exness |
| Free TradingView | Existing chart surface; basic price alerts can prompt review | The current Basic plan lists three price alerts and no technical/script alerts |
| MT5 mobile on XAUUSDc | You enter and manage trades manually | Desktop custom MQL5 indicators/EAs do not run natively in the mobile app |
| Desktop MT5 indicator | Optional later source of broker-feed push alerts | Requires a running desktop terminal; not your current setup |
| Bot, webhook bridge, paid data or VPS | No immediate role | Unnecessary cost/complexity for the current manual learning workflow |

TradingView's current plan comparison separates price alerts from technical/script alerts. Build the first version around visible chart labels, not a promised free push-alert service. [TradingView plans](https://www.tradingview.com/pricing/)

MT5 mobile does not support custom desktop indicators or EAs. A desktop MQL5 program can send push notifications to a mobile MetaQuotes ID if you later choose that setup. [MetaQuotes mobile limitation](https://www.mql5.com/en/forum/442119), [MT5 notification settings](https://www.metatrader5.com/en/terminal/help/startworking/settings)

Pine strategies use simulated orders and do not directly trade through integrated brokerage accounts. Use a strategy only for research; manual chart guidance fits your stated preference. [TradingView strategies](https://www.tradingview.com/pine-script-docs/faq/strategies/)

MT5's Strategy Tester supports real ticks and delay simulation for a future research harness. Check actual tick coverage, spreads and costs; selecting the mode alone does not prove an edge. [MT5 Strategy Tester](https://www.metatrader5.com/en/terminal/help/algotrading/testing)

## The attached log and plugin prices do not supply a backtest yet

The entire attached October 14 log is an application connection/activity log. It reports USC account currency, 0.00 balance at its recorded time, and two history requests each returning zero orders; positions and pending-order requests also return zero. It contains no completed trades, deal prices, SL/TP values, symbol specifications or P/L. It cannot establish your prior performance, and zero retrieved trades in this short session is not proof you have never traded. The log's timezone is unspecified, so its timestamps were not converted.

Alpha Vantage's connected gold-history tool returned XAUUSD daily date/price rows through October 13. A bounded 166-row subset for May 1–October 13, 2026 is saved in alpha_vantage_gold_daily.json. The returned rows have no intraday OHLC, bid/ask spread or tick order and include weekend dates. They cannot resolve M15 entries or which stop/target was hit first. This feed is not the Exness execution feed.

An XAU/USD 15-minute request to the connected FX endpoint returned a premium-access error. No subscription was purchased, and the error does not establish that XAU is supported by that endpoint. Other available equity/crypto feeds should not be substituted for gold CFD data. **The useful next source is MT5/Exness XAUUSDc history, or an independently documented gold intraday feed.** We have not obtained that history or run a strategy backtest.

For your log, the smallest useful replacement is a completed-deals account history report if one exists; for strategy research, export M1/M15 bars and preferably bid/ask ticks with symbol specification and server-time information. Do not send credentials. Daily history remains context only.

## Profitability must survive independent prices, costs and new trades

There are two different tests: **replay the group's posted instructions** and **test our new price-based strategy**. A successful result for one would not validate the other.

1. Obtain the exact Exness XAUUSD bid/ask tick history, symbol specifications, commission/swap schedule and server-time conversion. M1 OHLC is useful for preliminary analysis but cannot resolve all same-bar SL/TP ordering or spread-sensitive fills. Do not assign a win when both targets and stop appear reachable but sequence is unknown.
2. For the Telegram replay, manually reconcile instrument identity, repeated attempts, market/limit intent, expiry, target allocation and stop amendments. Apply messages only after publication and realistic receipt delay. Leave ambiguous trades unresolved and show their count separately.
3. For the new strategy, use at least 12–24 months spanning different gold regimes if available. Predefine rules, then use chronological development/validation/holdout splits. Reserve the final 20% of price history for one untouched test. Already inspecting Telegram posts means this export itself is not pristine unseen evidence; add a genuinely future demo period. Record every tested variant to expose selection bias.
4. Measure net expectancy in R, profit factor, maximum equity drawdown, trade count, monthly stability, losing streaks and fill/rejection rates. Compare the single 2R exit against a separate, predeclared partial-exit experiment only after the baseline is measured. Stress costs and delays; assess long and short results separately. Do not select rules from the best-looking total return alone.
5. Proposed screening gates are at least 200 out-of-sample trades, positive net expectancy, net profit factor above 1.2, drawdown inside your agreed cap, and an edge that remains positive under reasonable cost stress. Assess dependence and uncertainty, for example with trading-day block resampling; these thresholds are research gates, not proof of future profit. If evidence is weak, stay in research.
6. Forward-test on demo for at least eight weeks and 50 executed trades, extending the period if necessary. Check alert timing, MT5 fills and protection, reconnection, duplicate handling and stop limits. Only discuss a small live allocation after those checks and your risk limits are settled.

## Cambodia affects account checks and time conversion

Use UTC+7 for your journal and displayed schedule. London/New York session relationships shift with their daylight-saving calendars, so a fixed Cambodia research window is not the same as an automatically adjusted London/New York session. Recheck event times from a current calendar rather than copying old Telegram announcements.

SERC publishes the local list of derivative brokers and approved products. **Exness was not named on the specific SERC derivative-broker list reviewed on October 14, 2026.** This observation does not establish whether your particular cross-border arrangement is lawful, prohibited or protected. The supplied statement names Exness (SC) Ltd; verify account eligibility and applicable protections with Exness/SERC; local licensing should not be inferred from successful registration. [SERC derivative-broker list](https://www.serc.gov.kh/english/m67.php)

Choose account type by measured all-in costs and execution for your strategy, not by advertised leverage. Confirm regular XAUUSD versus a different gold product, account currency, minimum volume, stop distance and maintenance hours in the terminal. Broker-country eligibility was not conclusively verified from the country-restrictions help page in this run.

## The next build should make discipline visible

Confirmed: $10 intended capital, $5 maximum total loss, XAUUSDc, manual execution in MT5 on your phone, free TradingView, and knowledge of basic trading concepts. The PDF confirms a Standard Cent USC account and shows Exness (SC) Ltd as its entity. Historical price/volume/P&L pairs corroborate cent-gold exposure; current volume step and stop-level specifications still need a terminal check.

The recommended next deliverable is one **TradingView visual indicator** that combines the EMA setup and entry/stop/target/risk display in one chart slot. A companion backtest or replay measures the rules separately. Save/add the script through TradingView's browser Pine Editor, then verify that the saved chart and script load on your phone; the mobile installation path has not been tested here. With the free plan, check signals manually at M15 closes and use available price alerts only as a reminder to review the chart. A price alert is not an automated strategy confirmation.

Record account equity, accepted/skipped setups, actual fill, SL, TP, size, result and running P/L manually. The TradingView script cannot see your Exness balance, positions or $5 loss limit; its risk display depends on correctly entered account values. No bot, webhook, paid subscription or VPS is needed. No indicator was built or attached to your accounts during this analysis.

## Coverage and uncertainty

This is a complete structural/text parse of the six HTML pages and a targeted visual review of five linked images: messages 296, 2938, 4046, 4331 and 5397. It is not a full translation or transcription audit. The folder contains 1,340 OGG voice files; voice and video contents were not transcribed. Images were not exhaustively OCR-processed. Instructions in these media can materially change outcomes and strategy interpretation.

The parser uses explicit English price labels and simple numeric direction headers. It retains entry ranges as quoted and flags ambiguity; optional parenthetical targets can be omitted from computed geometry and are flagged. A candidate is a posted instruction, not evidence of a fill. 'Valid' means basic price ordering only. Media/text classification is not exhaustive and missing reply links do not imply a loss or a win.

The Exness activity log and all three pages of the supplied account statement were inspected. All 64 closed positions reconcile to printed totals and their price/volume/P&L calculations. No Exness intraday price history, original signal edit history or live terminal was available. External daily gold prices were obtained as context only. No historical market replay, backtest, forward test or live execution occurred. Group-reported probabilities and macro commentary were not treated as verified forecasts. Profitability remains unestablished.

The SH Data source files were read without modification. HTML-page hashes, extracted candidates, reproducible code, a SQLite metadata audit and a companion notebook are saved locally. No files were pushed or publicly published.
