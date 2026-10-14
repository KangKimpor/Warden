# SH Gold Signals v2

This is a private TradingView script with simple indicator visuals and a built-in strategy backtest. Orders in the strategy report are hypothetical. You execute manually in MT5. Start with demo observation; the rules have not established a profitable edge.

## Use on your phone

1. In the same TradingView account, open **XAUUSD → 15m → ordinary candles**.
2. Remove **Gold Cent Guard v1** from the chart, then add **Indicators → My scripts → SH Gold Signals v2**. It is listed as a strategy because it includes a backtest.
3. Read the small panel: **BUY/SELL, Entry limit, SL, TP1, TP2**. Only a fresh **REVIEW** candidate can be considered. **EXPIRED** prices are historical examples; do not trade them.

There are two settings: current equity in USC, and a cost allowance per ounce. Default equity **1,000 USC = $10** is an assumption, not a live account reading. Default cost allowance **$0.50 per ounce** is an illustrative research assumption, not measured Exness spread/slippage.

For an eligible candidate, use a limit entry at the displayed reference price during the next 15-minute candle only. If it does not fill, cancel it at that candle's close. Do not chase price or widen the SL. Attach the displayed SL and **TP2** in MT5. **TP1 is a checkpoint only**: this baseline does not close half or move to breakeven there. Minimum cent volume may make partial closing impossible.

Check the actual Exness quote and contract specification before submitting any order. Chart prices are OANDA prices, not Exness. If feed differences make the entry/stop invalid, or current minimum size cannot fit the risk budget, skip. Avoid high-impact USD news; the script has no news feed. Keep one actual position at a time, maximum two entries per Cambodia day, and stop after $0.20 total losing P/L that day. Wins do not reset the loss allowance. Stop real trading at $5 equity for a fresh $10 account. The script cannot enforce any of those rules in MT5.

## What comes from SH Data

The six exported HTML pages contain 5,411 ordinary messages and 359 possible entry/SL/TP messages. Only 54 explicitly identify gold; others leave the instrument unspecified. Replies and screenshots are incomplete, so the export cannot provide an audited win rate.

Selected source evidence, preserved in `sh_evidence.json`:

| SH message | Evidence | Rule used here |
|---|---|---|
| 26, May 6, `messages.html` | Gold limit long and anticipated pullback into FVG | Retest entry concept |
| 1650, June 26, `messages2.html` | Uptrend, EMA and support box confirmation | Trend and closed-candle confirmation |
| 2938, July 28, `messages3.html` | 1H bearish FVG, downtrend EMA and trendline | FVG plus direction filter |
| 4046, August 27, `messages4.html` | Bearish FVG, under EMA, support break; linked M15 chart shows EMA20/50/200 | EMA20/50/200 on M15 |

There are 15 text messages mentioning FVG/BFVG, five mentioning EMA, and three mentioning both. These counts concern English text labels only, not all Khmer explanations, images or audio. Among the 54 explicit gold candidates, median first target is **1R**, median final target is **2R**, and median stop is **$12 per ounce**. The exit proportions inform TP1/TP2; stops here adapt to the zone instead of imposing $12 everywhere.

This is an SH-inspired, reproducible hypothesis. SH also uses discretionary trendlines, H1/H4 zones, CHOCH, pivots and different EMA periods. The export does not specify one complete mechanical system. The gap threshold, eight-hour zone expiry, confirmation test, ATR buffer and session below are proposed definitions, not proven SH rules or optimized parameters. Voice and video were not transcribed; five linked images were reviewed in the original audit.

## Exact baseline rules

- Chart: XAUUSD, 15-minute standard candles, at least 200 preceding bars.
- BUY trend: EMA20 > EMA50 > EMA200 and EMA50 rising. SELL reverses these comparisons.
- Bullish FVG: third candle's low is above first candle's high by at least 0.1 ATR(14); middle candle bullish. Bearish FVG reverses that definition with a bearish middle candle. Recognize gaps only after the third candle closes and in the corresponding trend.
- Keep only the latest zone in each direction. It expires after 32 bars, invalidates if a candle closes beyond its far edge, and is consumed on its first overlap even if confirmation fails. No signal on its creation candle.
- BUY confirmation: first retest overlaps the bullish zone, closes bullish above its upper edge, above EMA20 and above the previous candle's high. SELL reverses all conditions.
- Candidate candle must close Monday–Friday from **14:00 inclusive to 23:00 exclusive, Cambodia time**.
- Entry reference: candidate close, a next-candle limit order. No same-close fill is assumed.
- BUY SL: below the lower of the retest low and zone bottom by 0.2 ATR. SELL SL: above the higher of the retest high and zone top by 0.2 ATR. Round stops outward to the chart tick.
- TP1 = one entry-to-stop distance; TP2 = two. The full simulated position exits at SL or TP2. Price levels remain fixed after order creation.

Historical BUY/SELL labels mark technical candidates, including candidates excluded by account sizing, daily limits, an already open simulated trade, or an unfilled limit. They are not filled-trade markers. Hover a historical label for its entry/SL/TP values. The panel retains the latest candidate with an explicit expired status; its short horizontal lines span only the candidate and the following candle.

## $10 sizing and simulation assumptions

The size guide assumes **1 ounce per XAUUSDc cent lot**, minimum/step **0.01 cent lot**, as supported by the statement and broker documentation. [Exness's Standard Cent documentation](https://get.exness.help/hc/en-us/articles/17537782786588-Standard-Cent-account) confirms cent-lot conversion and minimum volume; the ounce exposure is corroborated by the supplied gold trades. Verify current MT5 values. Do not enter these numbers as standard lots.

Manual risk budget is the smallest nonnegative amount of **$0.10, 1% of entered equity, and equity above $5**. Size rounds down in 0.01 steps using stop distance plus the cost allowance. A $12 stop with a $0.50 allowance requires $0.125 at minimum volume, so the $10 account must **SKIP**. The display does not subtract your actual daily losses or detect positions; apply those limits manually.

The backtest separately starts at **$10**, uses its own simulated equity, one position, maximum two order attempts per Cambodia day, a $0.20 daily losing-P/L allowance and the $5 floor for new entries. Unfilled attempts count toward two. Qty is ounces, accepted only when the chart's point value is 1. Margin is modeled at 1:2,000 (0.05%), not a guarantee of current broker leverage or margin availability.

The simulated cost model charges **$0.25 per ounce per side**, or $0.50 per ounce round trip. This is a spread/cost proxy, not a claim that Exness charges that commission. Increasing the size-guide allowance reduces size but does not change the commission property: for a cost stress test, also raise strategy Properties → Commission. Intrabar paths use TradingView's broker emulator; there is no bid/ask series, tick reconstruction, measured spread, financing/swap model or live news exclusion. Gaps and slippage can exceed the intended loss/floor. Do not enable recalculation on fills or on every tick when comparing this baseline.

TradingView explains the execution assumptions and cost controls in its [strategy documentation](https://www.tradingview.com/pine-script-docs/concepts/strategies/). Reported results apply only to the loaded chart history and settings; they do not evaluate all SH signals. Do not tune parameters to make this short sample profitable. Validate on unseen periods and forward demo observations before considering real money.

Source: `sh_gold_signals.pine`. Version 1 source and its validation remain as an archive. Version 2 checks and observed performance are recorded in `SH_VALIDATION.md`.
