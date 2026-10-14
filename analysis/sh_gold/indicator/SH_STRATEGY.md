# SH Gold Signals v4

This is a private TradingView script with simple indicator visuals and a built-in strategy backtest. Orders in the strategy report are hypothetical. You execute manually in MT5. Start with demo observation; the rules have not established a profitable edge.

## Use on your phone

1. In the same TradingView account, open **XAUUSD → 5m or 15m → ordinary candles**. M5 offers more frequent opportunities and a shorter entry window; it is not proven more profitable.
2. Remove the older Gold Cent Guard / SH Gold script from the chart, then add **Indicators → My scripts → SH Gold Signals v4**. It is listed as a strategy because it includes a backtest.
3. Read the small panel: **BUY/SELL, Entry limit, SL, TP1, TP2 and estimated net reward/risk**. Only a fresh **REVIEW** candidate passes the displayed size/reward checks. **SKIP** fails them; **EXPIRED** prices are historical examples. Daily limits, news, the broker quote and your actual positions still need manual review.

For a cleaner chart, open the script's **Settings → Style** and uncheck **Trades on chart**. This hides simulated entry/exit markers while keeping the custom BUY/SELL labels; the saved layout already uses this setting.

There are two settings: current equity in USC, and a cost allowance per ounce. Default equity **1,000 USC = $10** is an assumption, not a live account reading. Default cost allowance **$0.50 per ounce** is an illustrative research assumption, not measured Exness spread/slippage. V4 uses at least $0.50 in both sizing display and simulation so the display cannot understate the simulation's default cost proxy.

For an eligible candidate, use a limit entry at the displayed reference price during the next candle only: **5 minutes on M5, 15 on M15**. The panel shows its Cambodia expiry time. If it does not fill, cancel it at that candle's close. Do not chase price or widen the SL. Attach the displayed SL and **TP2** in MT5. **TP1 is a checkpoint only**: this baseline does not close half or move to breakeven there. Minimum cent volume may make partial closing impossible.

Check the actual Exness quote and contract specification before submitting any order. Chart prices are OANDA prices, not Exness. If feed differences make the entry/stop invalid, or current minimum size cannot fit the risk budget, skip. Avoid high-impact USD news; the script has no news feed. Keep one actual position at a time, maximum two entries per Cambodia day, and stop after $0.20 total losing P/L that day. Wins do not reset the loss allowance. Stop real trading at $5 equity for a fresh $10 account. The script cannot enforce any of those rules in MT5.

## What comes from SH Data

The six exported HTML pages contain 5,411 ordinary messages and **359 gold entry/SL/TP candidates**. Your October 14 confirmation brings the 305 unnamed price signals into the gold scope alongside 54 explicitly labeled Gold/XAU signals. Both categories now inform the strategy; the category records label provenance only. The export also contains explicit crypto posts (e.g. message 608, Short BTC at 61,100), which retain their original labels and remain excluded from gold. Replies and screenshots are incomplete, so the export cannot provide an audited win rate.

Selected source evidence, preserved in `sh_evidence.json`:

| SH message | Evidence | Rule used here |
|---|---|---|
| 26, May 6, `messages.html` | Gold limit long and anticipated pullback into FVG | Retest entry concept |
| 1650, June 26, `messages2.html` | Uptrend, EMA and support box confirmation | Trend and closed-candle confirmation |
| 2938, July 28, `messages3.html` | 1H bearish FVG, downtrend EMA and trendline | FVG plus direction filter |
| 4046, August 27, `messages4.html` | Bearish FVG, under EMA, support break; linked M15 chart shows EMA20/50/200 | EMA20/50/200 on M15 |
| 2484, July 16, `messages3.html` | Below OP short; above OP long; pivot as support/resistance | Feed-day open and a classic daily pivot as objective proxies |
| 3317, August 5, `messages4.html` | Short 4235 at H4 FVG, SL 4250, targets 4220/4213/4205 | Include the formerly unnamed gold signals in the evidence |
| 5610 / 5641, October 7–8, `messages6.html` | Higher-timeframe downtrend and H1 sell direction | Completed H1 directional filter |
| 5670, October 9, `messages6.html` | M15 bullish structure and support for a buy scenario; image marks BOS | Require closed-bar structure/confirmation rather than enter on a direction forecast |

Of the 359 candidates, **357** pass basic direction/price-order checks. Among these, 348 have multiple targets and 17 have entry ranges. Median first target is **1R**, median final target **1.857R**, and median stop **$15 per ounce**. The $212 stop and two invalid instructions remain flagged. These are planned price geometries, not achieved returns. The former 54-message subset's $12/2R medians no longer define the evidence population. TP1 stays at 1R and TP2 at a simple 2R research target; technical stops remain adaptive and are not forced to $15.

This is an SH-inspired, reproducible hypothesis. SH also uses discretionary trendlines, H1/H4 zones, CHOCH, proprietary KTR/Pivot levels and different EMA periods. The export does not specify one complete mechanical system or the proprietary level formulas. V4 uses the chart feed's daily open and a classic pivot from previous-day H/L/C as transparent proxies; these do not reproduce CRAZII's OP/Pivot/KTR. Exact H1 EMA periods, the 1.5 minimum net-R threshold, gap size, confirmation window, ATR buffer and session are proposed definitions, not proven or optimized SH rules. Voice and video were not transcribed. Four additional linked charts were visually checked during this revision.

## Exact baseline rules

- Chart: XAUUSD, 5- or 15-minute standard candles, at least 200 preceding bars.
- BUY trend: EMA20 > EMA50 > EMA200 and EMA50 rising. SELL reverses these comparisons.
- Directional context: BUY requires the last completed H1 close above its EMA50 and H1 EMA20 > EMA50; SELL reverses the comparisons. Use previous completed H1 values with `lookahead_on` and a one-bar offset so historical bars do not receive future H1 closes. [TradingView's confirmed higher-timeframe pattern](https://www.tradingview.com/pine-script-docs/concepts/other-timeframes-and-data/).
- Feed-day context: BUY confirmation must close above both the current daily open and `(previous daily high + previous daily low + previous daily close) / 3`. SELL must close below both. Current daily open is already known; all other daily inputs use the completed prior bar. Day boundaries follow the chart provider, while trade caps and session follow Cambodia time. Missing context suppresses signals.
- Bullish FVG: third candle's low is above first candle's high by at least 0.1 ATR(14); middle candle bullish. Bearish FVG reverses that definition with a bearish middle candle. Recognize gaps only after the third candle closes and in the corresponding trend.
- Keep only one zone in each direction. An untouched zone can be replaced by a newer gap. It expires after eight hours of chart bars (96 on M5, 32 on M15), invalidates if a candle closes beyond its far edge or loses its trend, and cannot signal on its creation candle.
- FVG BUY: after the first overlap, allow the touch candle and the next three candles to confirm. Close bullish above the zone's upper edge, EMA20 and the previous candle's high. SELL reverses all conditions. Keep the lowest/highest price since the first touch for the stop; do not consume the zone merely because the touch candle fails confirmation.
- EMA BUY: a candle overlaps the EMA20–EMA50 band in the BUY trend and closes at/above EMA50. Allow that candle and the next three to close bullish above EMA20 and the previous candle's high. SELL reverses the conditions. Track the lowest/highest price since the pullback began. Losing the trend or exceeding three bars resets the pullback.
- Merge matching FVG and EMA confirmations into one label, with FVG taking priority. After any signal, suppress the next three candles to limit duplicates. A fired signal consumes the armed setups in that direction.
- Candidate candle must close Monday–Friday from **14:00 inclusive to 23:00 exclusive, Cambodia time**.
- Entry reference: candidate close, a next-candle limit order. No same-close fill is assumed.
- FVG BUY SL: below the lower of the tracked retest low and zone bottom by 0.2 ATR. EMA BUY SL: below the tracked pullback low by 0.2 ATR. SELL mirrors these rules. Round stops outward to the chart tick.
- TP1 = one entry-to-stop distance; TP2 = two. The full simulated position exits at SL or TP2. Price levels remain fixed after order creation.
- Before a simulated order or a REVIEW status, require estimated net reward/risk **at least 1.5**: `(2 × stop distance − cost allowance) / (stop distance + cost allowance)`. With a $0.50 allowance, a $2 stop returns 1.40 net R and is skipped; a $5 stop returns about 1.73. This measures planned payoff if TP2 is reached, not its probability. It does not account for all slippage or guarantee profit. Never tighten the stop merely to fit the account.

Historical BUY/SELL labels mark technical candidates, including candidates excluded by account sizing, daily limits, an already open simulated trade, or an unfilled limit. They are not filled-trade markers. Hover a historical label for its entry/SL/TP values. The panel retains the latest candidate with an explicit expired status; its short horizontal lines span only the candidate and the following candle.

Technical analysis identifies rule-based setups; it does not reliably predict the next price move. The new filters select aligned setups and reject poor cost geometry; they can reduce signal frequency. See `SH_VALIDATION.md` for measured tests and limitations. Profitability requires positive expectancy after actual execution costs on unseen periods and forward demo trades.

## Alerts while staying on TradingView Basic

[TradingView's plan comparison](https://www.tradingview.com/pricing/) currently lists three active price alerts for Basic and no technical alerts on scripts. Exact automatic BUY/SELL notifications therefore require a supported technical-alert plan or a separate running helper. No subscription or helper is needed for the chosen manual-price-alert workflow.

1. Review the chart during the 14:00–23:00 Cambodia session. EMA20 and EMA50 are now visible to help spot approaching pullbacks.
2. Add a **price** alert at a level you want to watch near the current EMA band or FVG: open Alert, choose XAUUSD price, Crossing, and type that price.
3. Name it **Gold: review 5m/15m setup**, select the app notification option, and enable TradingView notifications on your phone. Actual push delivery still needs a phone test.
4. When it fires, open the chart and wait for a closed-candle BUY/SELL candidate. A price crossing alone is not a strategy signal. Confirm REVIEW, expiry, sizing and the broker quote before considering an entry. Reset the manual alert when the watched level moves; it does not follow the EMA automatically.

V4 also contains `alert()` messages with side, timeframe, entry/SL/TP, estimated net R and expiry, for use if technical alerts become available later. In that case select **SH Gold Signals v4 → alert() function calls only**, not simulated order fills. Recreate the alert after changing script/settings/timeframe: TradingView alerts keep a saved snapshot. Historical labels do not send retroactive notifications. [Official alert documentation](https://www.tradingview.com/pine-script-docs/concepts/alerts/).

## $10 sizing and simulation assumptions

The size guide assumes **1 ounce per XAUUSDc cent lot**, minimum/step **0.01 cent lot**, as supported by the statement and broker documentation. [Exness's Standard Cent documentation](https://get.exness.help/hc/en-us/articles/17537782786588-Standard-Cent-account) confirms cent-lot conversion and minimum volume; the ounce exposure is corroborated by the supplied gold trades. Verify current MT5 values. Do not enter these numbers as standard lots.

Manual risk budget is the smallest nonnegative amount of **$0.10, 1% of entered equity, and equity above $5**. Size rounds down in 0.01 steps using stop distance plus the cost allowance. The full SH cohort's $15 median stop with a $0.50 allowance requires $0.155 at minimum volume, so the $10 account must **SKIP**. The display does not subtract your actual daily losses or detect positions; apply those limits manually.

The backtest separately starts at **$10**, uses its own simulated equity, one position, maximum two order attempts per Cambodia day, a $0.20 daily losing-P/L allowance and the $5 floor for new entries. Unfilled attempts count toward two. Qty is ounces, accepted only when the chart's point value is 1. Margin is modeled at 1:2,000 (0.05%), not a guarantee of current broker leverage or margin availability.

The simulated cost model charges **$0.25 per ounce per side**, or $0.50 per ounce round trip. This is a spread/cost proxy, not a claim that Exness charges that commission. Increasing the size-guide allowance reduces size but does not change the commission property: for a cost stress test, also raise strategy Properties → Commission. Intrabar paths use TradingView's broker emulator; there is no bid/ask series, tick reconstruction, measured spread, financing/swap model or live news exclusion. Gaps and slippage can exceed the intended loss/floor. Keep recalculation on fills disabled. Every-tick recalculation is enabled to update the panel's expiry on live ticks; candidates and simulated order logic still require a closed candle, and the historical test does not reconstruct ticks.

TradingView explains the execution assumptions and cost controls in its [strategy documentation](https://www.tradingview.com/pine-script-docs/concepts/strategies/). Reported results apply only to the loaded chart history and settings; they do not evaluate all SH signals. Do not tune parameters to make this short sample profitable. Validate on unseen periods and forward demo observations before considering real money.

Source: `sh_gold_signals.pine`. Prior source revisions remain in Git history; version 1 is also saved locally as an archive. Version 2–4 checks and observed performance are recorded in `SH_VALIDATION.md`.
