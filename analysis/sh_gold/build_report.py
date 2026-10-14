from pathlib import Path
import json, sqlite3

ROOT=Path(__file__).parent
s=json.loads((ROOT/'summary.json').read_text(encoding='utf-8'))
monthly_sql="""WITH months AS (
 SELECT substr(timestamp,1,7) AS month, COUNT(*) AS messages FROM messages GROUP BY 1
), cohorts AS (
 SELECT substr(timestamp,1,7) AS month, instrument, COUNT(*) AS signals,
 SUM(valid) AS valid_signals, SUM(side='buy') AS buys, SUM(side='sell') AS sells
 FROM parsed_signals GROUP BY 1,2
), instruments AS (SELECT 'explicit_gold' AS instrument UNION ALL SELECT 'unspecified')
SELECT months.month, instruments.instrument, COALESCE(cohorts.signals,0) AS signals,
 COALESCE(cohorts.valid_signals,0) AS valid_signals, months.messages,
 COALESCE(cohorts.buys,0) AS buys, COALESCE(cohorts.sells,0) AS sells
FROM months CROSS JOIN instruments LEFT JOIN cohorts
 ON cohorts.month=months.month AND cohorts.instrument=instruments.instrument
ORDER BY months.month, instruments.instrument;"""
sample_sql="""SELECT id, timestamp, side, entry, sl, tp, ROUND(risk,2) AS stop_distance,
 ROUND(rr,3) AS first_target_R, ROUND(rr_final,3) AS final_target_R
FROM parsed_signals WHERE instrument='explicit_gold' AND valid=1 ORDER BY timestamp,id LIMIT 10;"""
with sqlite3.connect(ROOT/'audit.sqlite') as db:
    db.row_factory=sqlite3.Row
    monthly=[dict(row) for row in db.execute(monthly_sql)]
    sample=[dict(row) for row in db.execute(sample_sql)]
assert sum(r['signals'] for r in monthly)==s['candidates']==359
assert sum(r['signals'] for r in monthly if r['instrument']=='explicit_gold')==54
assert len(sample)==10 and sample[0]['id']==5 and sample[0]['first_target_R']==1
for r in monthly:
    r['instrument_status']='Explicit gold' if r['instrument']=='explicit_gold' else 'Instrument unspecified'

sections=[
('summary',"""## Executive Summary

- **Start with a TradingView strategy and alerts you approve manually; consider an MT5 Expert Advisor after evidence supports it.** A strategy script adds simulated trades and performance measurement to an indicator's visual signals. Use your existing platforms before buying a bridge or VPS.
- **The group is a source of hypotheses, not a verified profitable system.** The audit covers 5,411 ordinary messages from May 5 to October 9, 2026. It finds 54 explicit gold signal candidates and 305 further candidates whose instrument is unspecified. Neither cohort is a verified trade history.
- **Trend pullbacks are a reasonable first experiment.** Reviewed commentary and selected charts combine EMAs, support/resistance, trend lines and fair-value gaps (FVGs). The group also discusses reversals; that is a separate strategy and should not be combined into the first experiment.
- **Capital and your broker's minimum lot can decide whether gold is suitable.** No account-specific sizing or live-trading recommendation is possible until your capital, acceptable drawdown, account type and symbol specifications are known.
"""),
('coverage',"""## The export is a conversation, not a trading ledger

All six HTML pages were parsed. The unit counted is one ordinary Telegram message with a unique message ID; service messages such as date separators are excluded. The timestamps explicitly carry UTC+07:00, matching Cambodia. The earliest ordinary message is May 5, 2026 at 20:04:58; the latest is October 9 at 19:56:50.

There are 3,798 messages with text and 3,381 with linked media; these groups overlap. Extraction found 359 candidates with one textual direction, an entry price or range, a stop and targets. Explicit BTC/ETH headings are excluded. Of these, 54 explicitly mention Gold/XAU, while 305 do not name the instrument. Image-only signals, Khmer-only instructions and ambiguous mixed-direction messages are outside this parser's scope.

**A zero in the explicit-gold series means the naming convention disappeared, not that the group stopped trading gold.** The additional cohort preserves that uncertainty instead of inferring the symbol from price. May and October are partial months, so counts should not be used to compare trading frequency directly. These are posted candidates, including reposts, not unique filled trades.
"""),
('geometry',"""## Multiple targets make a TP count misleading

All 54 explicit gold candidates pass a basic direction/price-order check. Of those, 51 have multiple targets and five have entry ranges. Ten contain the word 'limit', showing that arrival at entry matters; a move to TP before entry is reached is not a winning filled trade.

For this cohort, median stop distance is **12 gold price dollars per ounce**, with a range of 5–30. Median first-target reward/risk is **1.0R**; median last-target reward/risk is **2.0R**. R is the original entry-to-stop price distance. For ranges, these descriptive calculations use the first quoted entry endpoint, not an assumed actual fill. They exclude costs and do not describe achieved returns.

For example, message 9 posts a buy at 4550, SL 4535 and targets 4565/4580. These represent 1R and 2R. Taking half off at each would earn 1.5R on a full winner; taking half at 1R and stopping the rest at entry earns only 0.5R before costs. The export does not consistently specify these allocations or the timing of stop changes.

**We cannot calculate an honest win rate, profit factor, expectancy or drawdown from TP mentions.** For the 54 explicit gold candidates, 37 have no directly linked reply; 14 have a directly linked reply mentioning TP and two mention SL. These mention flags can overlap and are not outcome classifications. Unthreaded updates may exist. Across all 359 candidates, 325 have no directly linked reply.
"""),
('sample',"""## The extracted entries remain traceable to the export

The table is the first ten chronologically ordered explicit gold candidates, with original message IDs. It shows planned prices and gross target geometry. It is an audit sample, not a performance sample. Open the corresponding message ID in its original HTML page to inspect the text and context; the full extracted candidate list is saved in signals.csv.
"""),
('quality',"""## Text errors and discretionary updates block automatic copying

**High severity, high confidence:** message 5106, September 23 at 22:03:47, posts Buy 4289 / SL 4379 / TP 4299–4309. The stop is above a buy entry. Message 5110 at 22:06:23 says to adjust SL to 4279. Preserve both versions and their timestamps; applying the correction retroactively would hide approximately three minutes of execution risk.

**High severity, high confidence:** message 4895 quotes '4293-294'. It fails the literal price-order check; the second endpoint may be shorthand, but it was not silently changed to 4294. Message 4774 posts Short 4290 / SL 4502, a 212-dollar stop. It is geometrically possible but unusually wide; confirm whether it is intentional before use. Seven candidates have review flags for order/range issues, unusual geometry or an unparsed parenthetical bonus target. Direction/price ordering passes for 357 of 359 candidates; passing does not establish correctness or profitability.

**High severity, high confidence:** captions and selected charts use different feeds and methods. The May 22 roadmap is an OANDA H4 chart with EMA5 and fixed zones; the August 27 screenshot is an M15 chart with an EMA 20/50/200 lineup and manually drawn areas. A September 2 screenshot uses a suffixed MT5 gold symbol and H4 pending-order levels. Feed differences, chart/server time and human-drawn zones need explicit definitions before code can reproduce them.

**High severity, confidence limited by missing records:** this static export does not establish original-versus-edited signal history, deleted posts, all fills, all losses or the author's complete account history. Repeated price templates occur 18 times beyond their first occurrence among geometrically ordered candidates; these may be new attempts or reposts and were not deduplicated as trades. Two reply references point outside the parsed ordinary-message set; the cause is unknown.

The remediation is a timestamped trade ledger plus broker-price replay, with amendments taking effect only when posted. Reject ambiguous instructions rather than correcting them automatically.
"""),
('strategy',"""## Test one objective trend-pullback hypothesis first

**This is a proposed research baseline, not a recovered SH rule set or a proven edge.** The EMA periods have visual support in one reviewed chart; the exact trigger, stop buffer, session and exit rules below are our proposed definitions. They have not been optimized or backtested.

1. **Market and clock:** regular XAUUSD on M15, using the exact Exness symbol/feed for final validation. Only consider entries Monday–Friday between 14:00 and 23:00 Cambodia time; require the entry time to fall inside the window. This is a convenient initial research window, not evidence of the best session. Liquidate the strategy's position at 23:00 at the first available executable quote. Use an explicit UTC+7 conversion rather than assuming the MT5 server clock matches Cambodia.
2. **Trend:** on the completed signal bar, a long requires EMA20 > EMA50 > EMA200 and EMA50 above its previous-bar value. A short requires EMA20 < EMA50 < EMA200 and EMA50 below its previous-bar value. No trade without that ordering. No extra H1 filter in the initial baseline.
3. **Pullback:** the immediately preceding completed candle's high/low range must overlap its EMA20–EMA50 band. For a long, the signal candle closes bullish, above its EMA20 and above the preceding candle's high. For a short, it closes bearish, below its EMA20 and below the preceding candle's low.
4. **Entry:** send one market order on the next M15 bar's first available quote, subject to session, spread/cost and risk checks. Use completed candles only; no retrospective signals, future pivots or intrabar repainting. Allow one position and a maximum of two entries per Cambodia calendar day.
5. **Stop:** for a long, the lowest low of the last five completed bars including the signal bar, minus 0.2 × ATR(14). For a short, the highest high plus 0.2 × ATR(14). Require correct stop placement relative to the actual fill and compliance with broker stop levels. Do not widen a stop after entry.
6. **Exit:** one full-position target at 2 × the actual fill-to-stop distance. No partial exits or automatic break-even changes in this first version. A single exit is easier to evaluate and avoids splitting a minimum-size position. Include the 23:00 time exit in every test.
7. **News and costs:** use a timestamped event calendar. Skip entries 30 minutes before and after scheduled US CPI/NFP; for FOMC skip from 30 minutes before the rate release until 60 minutes after the scheduled press conference starts. If event data or spread information is unavailable, suppress entries. Initially reject trades whose estimated spread, commission and slippage cost exceeds 0.1R. Historical tests need the same event exclusions and actual bid/ask conventions.

The group's FVG, manually drawn trend-line, pivot and liquidity-sweep ideas remain research candidates. They require precise definitions and evidence of incremental benefit before being added. Several correlated visual confirmations do not establish a reliable probability of winning.
"""),
('risk',"""## Risk sizing matters more than the indicator's arrows

Until you provide your constraints, **0.25% of equity per trade is a proposed demo-testing limit**, not a personalized allocation. Stop opening trades after two losing trades in a day or a 1% day-start-equity decline including open P/L, whichever occurs first. Use a 5% peak-equity drawdown pause as a provisional review trigger; all limits should ultimately reflect your stated tolerance. Gaps and slippage can exceed planned loss limits.

For USD-denominated standard-lot gold, planned price loss is stop distance × contract ounces × lots. Exness currently lists a 100-troy-ounce contract and a 0.01-lot minimum for regular XAUUSD. Confirm the actual account/symbol settings, particularly cent-unit conventions, before using this formula. Prefer MT5's broker-aware profit calculation for one lot, then size down to the permitted volume step and include costs and margin checks. If the minimum volume exceeds the risk budget, skip the trade. Leverage changes required margin; it does not reduce the loss caused by a price move. [Exness instrument specifications](https://get.exness.help/hc/en-us/articles/17854173039388-Commodities)

**Illustration only:** with $500 equity and a 0.25% budget, risk is $1.25. A $12 stop at 100 ounces per lot calls for about 0.00104 lots before costs. If the account minimum is 0.01, the minimum trade risks $12, or 2.4% of that account, before costs. That trade does not fit the budget. Never round up or tighten the technical stop merely to force a trade.

With a hypothetical single +2R/-1R exit and no time exits, break-even win rate is 33.3% before costs. If every trade costs 0.1R, it becomes 36.7%. At +1R/-1R, the corresponding figures are 50% and 55%. These are payoff arithmetic, not forecasts; varying exits and costs require measuring actual net expectancy.
"""),
('platform',"""## TradingView is the first research surface; MT5 is the execution target

| Platform/build | Recommended role | Main limitation |
|---|---|---|
| TradingView Pine strategy with chart marks and alerts | First version: inspect signals, simulate defined rules, approve trades manually in MT5 | Broker-emulator fills and a possibly different gold feed require validation |
| MT5 MQL5 Expert Advisor | Broker-specific historical tests, then demo automation; live automation only after evidence and your decision | Requires execution safeguards and an operating terminal or VPS |
| Exness | Your proposed broker/feed; confirm account entity, costs, symbol, volume and stop rules | Broker eligibility, local protections and execution conditions are account-specific |
| TradingView webhook to an MT5 bridge | An alternative if later you need cross-platform automation | Adds alert delay, third-party cost, duplicate-order and outage handling |
| Telegram signal-copy bot | Not recommended for the first build | Inconsistent labels, corrections, expiry and discretionary management |

TradingView's Pine strategies simulate orders; they do not directly place orders through TradingView's integrated brokerage panel. External tools can interpret alerts for execution. For your stack, a native MT5 EA is the simpler eventual execution route. [TradingView strategy documentation](https://www.tradingview.com/pine-script-docs/faq/strategies/)

MT5 provides a Strategy Tester, including real-tick tests and delay simulation. Check real-tick coverage, spreads and gaps, and include account costs; selecting that mode alone does not validate an edge. [MT5 Strategy Tester](https://www.metatrader5.com/en/terminal/help/algotrading/testing)

If automation is eventually justified, require symbol/account checks, volume rounding down, margin and stop validation, broker-side protection, duplicate-order prevention, restart reconciliation, daily/drawdown controls and a manual stop. Confirm order/protection acceptance and log failures. Treat missing data or uncertain position state as a reason to halt new entries. Start on desktop demo; assess a VPS only once continuous operation is necessary. [Exness VPS](https://get.exness.help/hc/en-us/articles/360004040011-About-Exness-VPS)
"""),
('testing',"""## Profitability must survive independent prices, costs and new trades

There are two different tests: **replay the group's posted instructions** and **test our new price-based strategy**. A successful result for one would not validate the other.

1. Obtain the exact Exness XAUUSD bid/ask tick history, symbol specifications, commission/swap schedule and server-time conversion. M1 OHLC is useful for preliminary analysis but cannot resolve all same-bar SL/TP ordering or spread-sensitive fills. Do not assign a win when both targets and stop appear reachable but sequence is unknown.
2. For the Telegram replay, manually reconcile instrument identity, repeated attempts, market/limit intent, expiry, target allocation and stop amendments. Apply messages only after publication and realistic receipt delay. Leave ambiguous trades unresolved and show their count separately.
3. For the new strategy, use at least 12–24 months spanning different gold regimes if available. Predefine rules, then use chronological development/validation/holdout splits. Reserve the final 20% of price history for one untouched test. Already inspecting Telegram posts means this export itself is not pristine unseen evidence; add a genuinely future demo period. Record every tested variant to expose selection bias.
4. Measure net expectancy in R, profit factor, maximum equity drawdown, trade count, monthly stability, losing streaks and fill/rejection rates. Compare the single 2R exit against a separate, predeclared partial-exit experiment only after the baseline is measured. Stress costs and delays; assess long and short results separately. Do not select rules from the best-looking total return alone.
5. Proposed screening gates are at least 200 out-of-sample trades, positive net expectancy, net profit factor above 1.2, drawdown inside your agreed cap, and an edge that remains positive under reasonable cost stress. Assess dependence and uncertainty, for example with trading-day block resampling; these thresholds are research gates, not proof of future profit. If evidence is weak, stay in research.
6. Forward-test on demo for at least eight weeks and 50 executed trades, extending the period if necessary. Check alert timing, MT5 fills and protection, reconnection, duplicate handling and stop limits. Only discuss a small live allocation after those checks and your risk limits are settled.
"""),
('cambodia',"""## Cambodia affects account checks and time conversion

Use UTC+7 for your journal and displayed schedule. London/New York session relationships shift with their daylight-saving calendars, so a fixed Cambodia research window is not the same as an automatically adjusted London/New York session. Recheck event times from a current calendar rather than copying old Telegram announcements.

SERC publishes the local list of derivative brokers and approved products. **Exness was not named on the specific SERC derivative-broker list reviewed on October 14, 2026.** This observation does not establish whether your particular cross-border arrangement is lawful, prohibited or protected. Identify the exact legal entity in your Exness agreement and verify account eligibility and applicable protections with Exness/SERC; local licensing should not be inferred from successful registration. [SERC derivative-broker list](https://www.serc.gov.kh/english/m67.php)

Choose account type by measured all-in costs and execution for your strategy, not by advertised leverage. Confirm regular XAUUSD versus a different gold product, account currency, minimum volume, stop distance and maintenance hours in the terminal. Broker-country eligibility was not conclusively verified from the country-restrictions help page in this run.
"""),
('questions',"""## The next decision depends on your account and preferences

Please provide your starting capital, maximum acceptable account drawdown, trading experience and whether you prefer manual alerts or eventual automation. Also provide the Exness account type, exact gold symbol, and whether MT5 price history or your own trade-history export is available. Do not send passwords or trading credentials.

The recommended next deliverable is one Pine strategy with closed-bar chart signals and alerts, matched to a written rule sheet. The exact session and risk settings remain provisional until your answers arrive. No trading indicator or bot was built or connected in this analysis.
"""),
('caveats',"""## Coverage and uncertainty

This is a complete structural/text parse of the six HTML pages and a targeted visual review of five linked images: messages 296, 2938, 4046, 4331 and 5397. It is not a full translation or transcription audit. The folder contains 1,340 OGG voice files; voice and video contents were not transcribed. Images were not exhaustively OCR-processed. Instructions in these media can materially change outcomes and strategy interpretation.

The parser uses explicit English price labels and simple numeric direction headers. It retains entry ranges as quoted and flags ambiguity; optional parenthetical targets can be omitted from computed geometry and are flagged. A candidate is a posted instruction, not evidence of a fill. 'Valid' means basic price ordering only. Media/text classification is not exhaustive and missing reply links do not imply a loss or a win.

No broker history, account statement, original edit history or live terminal was provided or inspected. No historical market replay, backtest, forward test or live execution occurred. Group-reported probabilities and macro commentary were not treated as verified forecasts. Profitability remains unestablished.

The SH Data source files were read without modification. HTML-page hashes, extracted candidates, reproducible code, a SQLite metadata audit and a companion notebook are saved locally. No files were pushed or publicly published.
""")]

updates={
'summary':"""## Executive Summary

- **Build for manual decisions.** You chose manual trading and a proposed $10 Standard Cent account, with basic trading knowledge. An alert-only indicator with entry, SL, TP and cent-aware risk estimates fits that goal. No automatic order placement is needed.
- **Use your existing tools without new subscriptions.** MT5 desktop can provide broker-feed alerts; TradingView can be a visual/research companion if its current plan supports what you need. Platform choice still depends on desktop-versus-phone access and TradingView alert entitlement.
- **The group provides hypotheses, not a verified profitable system.** The audit covers 5,411 ordinary messages from May 5 to October 9, 2026: 54 explicit gold candidates and 305 candidates with no explicit instrument name. Trend pullbacks are the first proposed test, not a proven edge.
- **The $10 account is for learning.** Cent lots reduce exposure, but not by turning the balance into more real money. Your actual symbol specifications and total-loss limit remain necessary before choosing live sizes. The attached log reports zero balance at its recorded time and no retrieved trades.
""",
'risk':"""## A $10 cent account needs cent-aware risk estimates

You propose $10 capital and manual trades. **$10 corresponds to 1,000 USC.** Exness describes Standard Cent volumes as cent lots, with one cent lot equal to 0.01 standard lot, and lists a 0.01-cent-lot minimum and XAUUSDc availability. It also lists no trading commission for this account type; spread and any applicable financing still matter. [Exness Standard Cent](https://get.exness.help/hc/en-us/articles/17537782786588-Standard-Cent-account)

Combining that lot conversion with the published 100-ounce standard gold contract suggests **one cent lot represents one ounce, and 0.01 cent lot represents 0.01 ounce**. This is a derived sizing assumption, not a verified reading of your exact terminal. Confirm the symbol's contract size, minimum volume, volume step and profit units before acting. [Exness gold contract](https://get.exness.help/hc/en-us/articles/17854173039388-Commodities)

Under that assumption, at 0.01 cent lot, a $1 move in gold is about $0.01 in account P/L, displayed as 1 USC. A $12 stop therefore risks about **$0.12 = 12 USC = 1.2% of $10**, before spread/slippage. A full 2R target would pay about $0.24 before costs. Gold's quote price stays in dollars per ounce even though account P/L is in cents.

| Proposed account risk | Dollar budget | USC budget | Maximum price stop at 0.01 cent lot before costs |
|---|---:|---:|---:|
| 0.5% | $0.05 | 5 USC | $5 |
| 1% | $0.10 | 10 USC | $10 |
| 2% — illustration, not a recommendation | $0.20 | 20 USC | $20 |

The explicit gold cohort's median $12 stop would not fit a 1% budget at minimum volume. A conservative 0.5% research budget is likely to suppress many setups at this capital. **Do not increase risk or tighten a technical stop just to get a trade.** Your total-loss tolerance is still unanswered; no live risk percentage is approved or calibrated. Use demo while testing the rule set, then decide whether the real account can accommodate the stops.

For a future sizing display, calculate expected loss in account currency from the terminal's actual profit calculation, include costs, and round volume down to its allowed step. Skip a trade that cannot fit minimum volume or margin. Leverage reduces margin requirements, not price-loss exposure. Avoid splitting a minimum-size trade into multiple targets, martingale, averaging down or trying to turn $10 into income.

Provisional research controls remain one position, at most two entries per Cambodia day, no new trades after two losses or a 1% day-start-equity decline including open P/L, and a pause at 5% peak-equity drawdown. The latter is a proposed review threshold pending your total-loss limit. Gaps/slippage can exceed planned losses. At +2R/-1R, a theoretical break-even win rate is 33.3% without costs or time exits, or 36.7% if every trade costs 0.1R. These figures describe payoffs, not our expected win rate.
""",
'questions':"""## Set the loss limit and platform before implementation

Confirmed: manual trading, $10 intended capital, cent currency, and some basic gold-trading knowledge. Still needed: the maximum total loss that should make you stop; the exact gold symbol and MT5 contract/minimum-volume specifications; whether MT5 is available on a desktop or only mobile; and whether TradingView is free or paid.

The recommended next build is an **alert-only indicator**, with chart marks, proposed entry/stop/target and correctly labeled USD/USC risk. A companion strategy/replay harness measures results; it does not send live orders. An alert means a candidate to review, not a command to buy or sell. Manual fills can differ from the next-bar model, so keep a journal of actual entry, exit, spread, size and reason for accepting/skipping.

No indicator or bot was built or connected during this analysis. No passwords or account credentials are needed for discussion or a file-based history review.
"""
}
sections=[(id,updates.get(id,body)) for id,body in sections]
sections=[(id,body.replace('regular XAUUSD on M15, using the exact Exness symbol/feed for final validation.', 'gold on M15, validating the proposed XAUUSDc cent symbol and its exact Exness feed.').replace('**Entry:** send one market order on the next M15 bar\'s first available quote', '**Entry model for testing:** simulate one market order on the next M15 bar\'s first available quote; for actual use, present an alert for your manual review')) if id=='strategy' else (id,body) for id,body in sections]
platform_index=next(i for i,(id,_) in enumerate(sections) if id=='platform')
sections[platform_index]=('platform',"""## An alert-only indicator fits manual trading and the budget

| Platform/build | Role for you | Constraint |
|---|---|---|
| MT5 desktop custom indicator | Preferred broker-feed signal/risk display if you have a PC; you place orders manually | Desktop must run for its alerts; exact cent-symbol settings required |
| TradingView Pine indicator/strategy | Visual companion and preliminary rule testing; alerts if your existing plan permits | Different price feed and plan-specific technical-alert limits |
| Exness cent account | Small real exposure after testing and loss-limit agreement | Minimum size still must fit stop distance and risk budget |
| MT5 EA, webhook bridge or VPS | Unnecessary for your stated manual workflow | Adds cost/complexity without improving the evidence |
| Telegram copier | Not recommended | Ambiguous symbols, amended stops and discretionary instructions |

MT5 desktop MQL5 programs can send push notifications to a configured mobile MetaQuotes ID. The phone receives alerts; the desktop runs the custom logic. Native mobile charts do not provide the desktop custom-indicator workflow. [MT5 notification settings](https://www.metatrader5.com/en/terminal/help/startworking/settings)

TradingView separates price alerts from technical/script alerts, with limits by subscription. Check your existing entitlement before choosing it for notifications; do not buy an alert subscription solely to support this $10 account. [TradingView alert types](https://www.tradingview.com/support/solutions/43000696403-alerts-separation-by-type/)

Pine strategies use simulated orders and cannot directly trade through integrated brokerage accounts. For manual trading, chart marks and alerts are sufficient. [TradingView strategies](https://www.tradingview.com/pine-script-docs/faq/strategies/)

MT5's Strategy Tester supports real ticks and execution-delay simulation for a future research harness. Check actual tick coverage, spreads and costs; the mode alone does not prove profitability. [MT5 Strategy Tester](https://www.metatrader5.com/en/terminal/help/algotrading/testing)

No running MT5 process, default MetaQuotes terminal-data folder, matching standard installation folder or installed MetaTrader5 Python package was found in the bounded local checks. That does not prove MT5 is absent elsewhere or unavailable on your phone. No broker connection was opened.
""")
log_index=next(i for i,(id,_) in enumerate(sections) if id=='testing')
sections.insert(log_index,('data',"""## The attached log and plugin prices do not supply a backtest yet

The entire attached October 14 log is an application connection/activity log. It reports USC account currency, 0.00 balance at its recorded time, and two history requests each returning zero orders; positions and pending-order requests also return zero. It contains no completed trades, deal prices, SL/TP values, symbol specifications or P/L. It cannot establish your prior performance, and zero retrieved trades in this short session is not proof you have never traded. The log's timezone is unspecified, so its timestamps were not converted.

Alpha Vantage's connected gold-history tool returned XAUUSD daily date/price rows through October 13. A bounded 166-row subset for May 1–October 13, 2026 is saved in alpha_vantage_gold_daily.json. The returned rows have no intraday OHLC, bid/ask spread or tick order and include weekend dates. They cannot resolve M15 entries or which stop/target was hit first. This feed is not the Exness execution feed.

An XAU/USD 15-minute request to the connected FX endpoint returned a premium-access error. No subscription was purchased, and the error does not establish that XAU is supported by that endpoint. Other available equity/crypto feeds should not be substituted for gold CFD data. **The useful next source is MT5/Exness XAUUSDc history, or an independently documented gold intraday feed.** We have not obtained that history or run a strategy backtest.

For your log, the smallest useful replacement is a completed-deals account history report if one exists; for strategy research, export M1/M15 bars and preferably bid/ask ticks with symbol specification and server-time information. Do not send credentials. Daily history remains context only.
"""))
caveat_index=next(i for i,(id,_) in enumerate(sections) if id=='caveats')
sections[caveat_index]=('caveats',sections[caveat_index][1].replace('No broker history, account statement, original edit history or live terminal was provided or inspected.', 'A short Exness application log was inspected, but no completed-deal account statement, Exness price history, original signal edit history or live terminal was available. External daily gold prices were obtained as context only.'))

statement=json.loads((ROOT/'statement_metrics.json').read_text(encoding='utf-8'))
balance_sql='SELECT ROW_NUMBER() OVER (ORDER BY closed) - 1 AS close_event, closed, balance_usd, net_usd, closed_trades FROM closed_balance ORDER BY closed;'
with sqlite3.connect(ROOT/'audit.sqlite') as db:
    db.row_factory=sqlite3.Row
    balance_rows=[dict(row) for row in db.execute(balance_sql)]
assert balance_rows[0]['balance_usd']==15 and balance_rows[-1]['balance_usd']==17.339
latest={
'summary':"""## Executive Summary

- **The statement is profitable overall, but the process is fragile.** Its 64 closed XAUUSDc trades show 40 wins and 24 losses and +233.9 USC (+$2.339). Before the last two trades, net P/L was -$8.02; two overlapping 1-cent-lot buys then earned $10.359. Their size and concentration make that recovery unsuitable as evidence of a repeatable edge.
- **Fix exposure and loss controls first.** The statement records no SL on 43 trades and reconstructs a 59.9% maximum drawdown in closed-trade balance. This is not a measured mark-to-market equity drawdown, which may differ. Your next account is $10 with a $5 maximum total-loss limit; that maximum is a stop boundary, not a risk target.
- **For manual trading on your phone and free TradingView, build one visual Pine indicator.** It should show confirmed setups, entry/SL/TP, price-feed identity and cent-aware risk. You check the chart and place trades in MT5 mobile. Free TradingView does not include custom technical alerts; a desktop MT5 notification setup is an optional later path, not required now.
- **The entry idea remains untested.** The Telegram audit covers 5,411 ordinary messages, including 54 explicit gold candidates and 305 with unspecified instruments. The proposed M15 trend-pullback rules need intraday price testing. Neither your short statement nor Telegram TP claims proves that strategy profitable.
""",
'questions':"""## The next build should make discipline visible

Confirmed: $10 intended capital, $5 maximum total loss, XAUUSDc, manual execution in MT5 on your phone, free TradingView, and knowledge of basic trading concepts. The PDF confirms a Standard Cent USC account and shows Exness (SC) Ltd as its entity. Historical price/volume/P&L pairs corroborate cent-gold exposure; current volume step and stop-level specifications still need a terminal check.

The recommended next deliverable is one **TradingView visual indicator** that combines the EMA setup and entry/stop/target/risk display in one chart slot. A companion backtest or replay measures the rules separately. Save/add the script through TradingView's browser Pine Editor, then verify that the saved chart and script load on your phone; the mobile installation path has not been tested here. With the free plan, check signals manually at M15 closes and use available price alerts only as a reminder to review the chart. A price alert is not an automated strategy confirmation.

Record account equity, accepted/skipped setups, actual fill, SL, TP, size, result and running P/L manually. The TradingView script cannot see your Exness balance, positions or $5 loss limit; its risk display depends on correctly entered account values. No bot, webhook, paid subscription or VPS is needed. No indicator was built or attached to your accounts during this analysis.
""",
'platform':"""## Use a visual TradingView indicator with MT5 mobile execution

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
"""
}
sections=[(id,latest.get(id,body)) for id,body in sections]
risk_index=next(i for i,(id,_) in enumerate(sections) if id=='risk')
risk_body=sections[risk_index][1]
risk_body=risk_body.replace('This is a derived sizing assumption, not a verified reading of your exact terminal.', 'Every one of the 64 statement trades corroborates this exposure within the printed price/P&L rounding tolerance. Current terminal volume step and stop levels remain unchecked.')
risk_body=risk_body.replace('Your total-loss tolerance is still unanswered; no live risk percentage is approved or calibrated. Use demo while testing the rule set, then decide whether the real account can accommodate the stops.', 'Your stated maximum total loss is $5, or 500 USC. For a fresh $10 account with no additional deposits/withdrawals, stop at $5 equity or sooner if the process fails. My proposed initial per-trade ceiling is $0.10 (10 USC, 1% of starting capital), reduced as equity falls; typical $12 stops may therefore require skipping the setup at minimum size. This is a proposed learning rule, not evidence that live trading has a positive expected return.')
risk_body=risk_body.replace('Provisional research controls remain one position, at most two entries per Cambodia day, no new trades after two losses or a 1% day-start-equity decline including open P/L, and a pause at 5% peak-equity drawdown. The latter is a proposed review threshold pending your total-loss limit.', 'Proposed controls: one position, at most two entries per Cambodia day, and no new trades after two losses or $0.20 daily loss including open P/L. Pause and review well before the $5 total-loss boundary. Do not add to a losing position or increase size to recover. The daily limit does not supersede the remaining total-loss budget.')
sections[risk_index]=('risk',risk_body)
cambodia_index=next(i for i,(id,_) in enumerate(sections) if id=='cambodia')
sections[cambodia_index]=('cambodia',sections[cambodia_index][1].replace('Identify the exact legal entity in your Exness agreement and verify account eligibility and applicable protections with Exness/SERC;', 'The supplied statement names Exness (SC) Ltd; verify account eligibility and applicable protections with Exness/SERC;'))
personal="""## Your statement shows fragile recovery and excessive exposure

The three-page statement covers August 6–October 14, 2026, but its actual closed trades occur August 10–19. It contains **64 closed XAUUSDc positions**, five cancelled pending orders, and no open trades or working orders at issuance. Dates below use the statement clock because no timezone is supplied.

The statement reconciles exactly in USC: 1,500 deposited - 1,733 withdrawn + 233.9 closed P/L = 0.9 remaining. In real dollars that is **$15 deposit, $17.33 withdrawal, +$2.339 trading P/L and $0.009 balance**. The low ending balance follows a withdrawal and should not be described as the account being blown. The daily activity log had a rounded zero balance and zero recent retrieved orders; it was not a substitute for this statement.

**40 wins and 24 losses means a 62.5% win rate**, so most individual trades in this supplied period actually won. Gross winning P/L is $18.036 and absolute losing P/L is $15.697, giving a 1.149 profit factor. Commission, tax and swap columns are zero; spread is already part of execution prices, not a missing fee that should be subtracted again. This small, clustered sample does not establish an enduring profitable strategy.

**The last two wins change the story.** Removing them as a sensitivity check changes net P/L from +$2.339 to **-$8.02**. They supplied 57.4% of gross winning P/L. This is not a claim they should be removed from actual results; it demonstrates concentration. Each was 1 cent lot, while most prior volumes were 0.1–0.2. They overlapped for about 11 minutes and both show recorded SL = 0. Together they represented approximately two ounces of gold; a $2.50 adverse price move while both were open would cost about $5 before other effects. A winning result does not make that risk suitable for the proposed $10 account.

**Small wins coexist with much larger losses.** Median win is $0.0515 and median absolute loss is $0.618—approximately 12 times as large. The average win is $0.4509 and average loss $0.6540; the large final wins lift the average winner. The median position lasted 131 seconds, and 22 positions lasted under a minute. This pattern motivates testing slower closed-bar entries and predeclared exits; it does not prove a particular exit rule would have improved these trades.

**Protection and clustering need attention.** 43 of 64 trades (67.2%) show no recorded SL, and 36 show neither SL nor TP. The report stores the recorded/final values, not a complete amendment history: we cannot prove whether stops were absent for the whole lifetime or calculate original planned R. There were 20 entries within August 11, 14:06–14:27, and as many as six simultaneous positions in the full statement. Five sell positions closed together on August 19 at 07:05:57 with a combined **-$4.813** result—almost your entire new $5 total-loss limit in one cluster.

Reconstructing balance from the $15 deposit and closed P/L, grouping simultaneous closes, gives a peak of $17.404 and a trough of $6.98 before the final recovery: **$10.424 maximum closed-balance drawdown, or 59.9% of the peak**. The chart ends before the withdrawal, so withdrawing funds is not counted as trading loss. Floating equity and intratrade extremes are unavailable; this is not an equity drawdown measure.

**My interpretation:** the strongest observable problem is uncontrolled exposure and frequent discretionary trading, not simply too few winning entries. The statement cannot establish psychological motives, whether trades followed SH, or the counterfactual performance of a new indicator. Before real-money trials of any signal, rehearse one position, one stop, a fixed small loss budget and at most two entries per day. The new $5 hard stop is 50% of $10; aim to review failures much earlier rather than planning to consume that entire allowance.
"""
sections.insert(1,('personal',personal))
ci=next(i for i,(id,_) in enumerate(sections) if id=='caveats')
sections[ci]=('caveats',sections[ci][1].replace('A short Exness application log was inspected, but no completed-deal account statement, Exness price history, original signal edit history or live terminal was available.', 'The Exness activity log and all three pages of the supplied account statement were inspected. All 64 closed positions reconcile to printed totals and their price/volume/P&L calculations. No Exness intraday price history, original signal edit history or live terminal was available.'))

title='XAUUSD: evidence and a testable first strategy'
def md_table(rows, fields):
    return '\n\n|'+'|'.join(fields)+'|\n|'+'|'.join('---' for _ in fields)+'|\n'+'\n'.join('|'+'|'.join(str(row.get(field,'')) for field in fields)+'|' for row in rows)+'\n'
report='# '+title+'\n\n'+'\n\n'.join(body.strip()+(md_table(monthly,['month','instrument_status','signals','messages']) if id=='coverage' else md_table(sample,['id','timestamp','side','entry','sl','tp','first_target_R','final_target_R']) if id=='sample' else '') for id,body in sections)+'\n'
(ROOT/'research_report.md').write_text(report,encoding='utf-8')
sources=[dict(id='audit',label='SH Forex Signal export audit, May 5–October 9, 2026',path='summary.json',
    description='Read-only parse of messages.html and messages2.html through messages6.html in the user-provided SH Data folder. Parser and SHA-256 inventory saved locally.'),
    dict(id='monthly_query',label='Monthly parsed candidate cohorts',path='audit.sqlite',query=dict(sql=monthly_sql,engine='SQLite',language='sql',tables_used=['messages','parsed_signals'],filters=['All ordinary messages, May 5–October 9, 2026','English-label/direction candidate parser; BTC/ETH headings excluded','Explicit gold and unspecified instrument kept separate'],metric_definitions={'signals':'COUNT of candidate message IDs per export month and instrument-label cohort; reposts retained','messages':'COUNT of all ordinary message IDs per month'},description='Count explicit-gold and unspecified candidates without inferring their instruments. audit.sqlite is generated by analyze_export.py.',executed_at='2026-10-14')),
    dict(id='sample_query',label='First ten explicit gold candidates',path='audit.sqlite',query=dict(sql=sample_sql,engine='SQLite',language='sql',tables_used=['parsed_signals'],filters=["instrument = explicit_gold AND valid = 1",'First 10 ordered by timestamp, id'],metric_definitions={'first_target_R':'abs(first_target-first_quoted_entry)/abs(first_quoted_entry-stop); no costs','final_target_R':'abs(last_parsed_target-first_quoted_entry)/abs(first_quoted_entry-stop); no costs','stop_distance':'abs(first_quoted_entry-stop), gold price dollars/ounce'},description='Planned geometry only, not verified fills.',executed_at='2026-10-14')),
    dict(id='provided_log',label='User-provided Exness application log, October 14, 2026',path='log_audit.json',description='Whole supplied log reviewed locally. Contains connection/activity events and no completed trade records; account identifiers and connection addresses omitted.'),
    dict(id='alpha_daily',label='Alpha Vantage connected gold daily history',path='alpha_vantage_gold_daily.json',description='gold_silver_history(symbol=XAU, interval=daily, datatype=json), retrieved October 14, 2026. 166 rows from May 1–October 13 retained; date/price only, not Exness bid/ask or intraday bars.'),
    dict(id='statement',label='User-provided Standard Cent PDF statement, issued October 14, 2026',path='statement_metrics.json',description='All three PDF pages visually reviewed; 64 closed gold positions extracted, reconciled to 233.9 USC P/L and printed deposit/withdrawal/balance. Account/payment identifiers excluded from report datasets.'),
    dict(id='balance_query',label='Reconstructed closed-trade balance before withdrawal',path='audit.sqlite',query=dict(sql=balance_sql,engine='SQLite',language='sql',tables_used=['closed_balance'],filters=['Initial $15 deposit plus all 64 closed position P/L, grouped by exact close timestamp','Exclude final withdrawal from trading drawdown','Statement time; timezone unknown'],metric_definitions={'balance_usd':'1500 USC initial deposit plus cumulative closed P/L in USC, divided by 100; no floating P/L','closed_trades':'Cumulative count of closed positions'},description='Derived from supplied PDF via parse_statement.py; not a mark-to-market equity curve.',executed_at='2026-10-14'))]
blocks=[dict(id='title',type='markdown',body='# '+title)]
for id,body in sections:
    b=dict(id=id,type='markdown',body=body)
    if id in ['coverage','geometry','quality']: b['sourceId']='audit'
    blocks.append(b)
    if id=='coverage': blocks.append(dict(id='monthly_visual',type='chart',chartId='monthly_chart'))
    if id=='sample': blocks.append(dict(id='sample_table',type='table',tableId='gold_sample'))
    if id=='personal': blocks.append(dict(id='balance_visual',type='chart',chartId='balance_chart'))
artifact=dict(surface='report',manifest=dict(version=1,surface='report',title=title,description='Telegram evidence audit and an untested strategy proposal for discussion; no established profitability.',sources=sources,blocks=blocks,
    charts=[dict(id='monthly_chart',type='bar',dataset='monthly',sourceId='monthly_query',title='Parsed signal candidates by month and instrument label',subtitle='Posted candidates, not filled trades; May and October are partial months',encodings={'x':{'field':'month'},'y':{'field':'signals'},'color':{'field':'instrument_status'}},options={'grouping':'grouped','showLegend':True}),dict(id='balance_chart',type='line',dataset='closed_balance',sourceId='balance_query',title='Closed-trade balance before withdrawal',subtitle='USD after each close event; August 10–19, 2026; excludes floating P/L',encodings={'x':{'field':'close_event'},'y':{'field':'balance_usd'},'tooltip':[{'field':'closed'},{'field':'closed_trades'}]},options={'showLegend':False})],
    tables=[dict(id='gold_sample',title='First ten explicit gold candidates',dataset='gold_sample',sourceId='sample_query',defaultSort={'field':'id','direction':'asc'},columns=[{'field':field,'label':label} for field,label in [('id','Message'),('timestamp','UTC+7 timestamp'),('side','Side'),('entry','Entry'),('sl','SL'),('tp','Targets'),('stop_distance','Stop $/oz'),('first_target_R','First R'),('final_target_R','Final R')]])]),snapshot=dict(version=1,status='ready',datasets={'monthly':monthly,'gold_sample':sample,'closed_balance':balance_rows}),sources=[])
(ROOT/'artifact.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'source_notes.md').write_text('Report plan: executive summary; personal trade evidence and closed-balance curve; cohort and monthly counts; target geometry; 10-row audit sample; data errors; objective research rules; sizing; platform tradeoffs; testing; Cambodia; questions; limitations.\nMonthly grouped bars use 12 rows, six discrete calendar periods and two instrument-label cohorts; a chronological category comparison rather than a six-point continuous trend. Count axis starts at zero; legend names the cohorts. Geometric medians are exact-text descriptive measures, not P/L.\nClosed-balance chart: line with one chronological statement-time axis and one USD value axis, no redundant legend; '+str(len(balance_rows))+' rows from initial deposit through final trade close. Single blue-root default, direct axis labels. Floating P/L unavailable; withdrawal excluded. It describes historical closed-account performance, not a test of the proposed strategy. All printed closed P/L and balance totals reconcile exactly in USC; per-trade price/exposure verification allows 0.15 USC printed rounding tolerance.\nRenderer output must be validated before handoff.\nSource folder: '+s['source']+'\n',encoding='utf-8')
notebook={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}},'cells':[
    {'cell_type':'markdown','metadata':{},'source':['# SH Gold export audit\n','Run from this notebook folder. Source files are read only. Candidate detection is intentionally conservative; review instrument identity and all media before replay. No performance backtest was run.\n']},
    {'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':['from pathlib import Path\n','import runpy\n',"runpy.run_path(str(Path('analyze_export.py').resolve()), run_name='__main__')\n"]},
    {'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':['import sqlite3\n','db = sqlite3.connect("audit.sqlite")\n','db.row_factory = sqlite3.Row\n','monthly_sql = '+repr(monthly_sql)+'\n','[dict(row) for row in db.execute(monthly_sql)]\n']},
    {'cell_type':'markdown','metadata':{},'source':['## Reviewed run summary\n','```json\n',json.dumps(s,indent=2,ensure_ascii=False),'\n```\n']},
    {'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':["runpy.run_path(str(Path('parse_statement.py').resolve()), run_name='__main__')\n",'balance_sql = '+repr(balance_sql)+'\n','[dict(row) for row in db.execute(balance_sql)]\n']},
    {'cell_type':'markdown','metadata':{},'source':['## Statement metrics\n','```json\n',json.dumps({k:v for k,v in statement.items() if k!='last_two'},indent=2),'\n```\n']}]}
(ROOT/'audit.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'report':str(ROOT/'research_report.md'),'monthly_rows':len(monthly),'sample_rows':len(sample),'sections':len(sections)}))
