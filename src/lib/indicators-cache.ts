// Memoized indicator computation cache.
// Avoids recomputing expensive technical indicators when the underlying
// price data hasn't changed. Uses a simple hash of the last few prices
// as a cache key for O(1) lookup.

import { rsi, macd, ema, sma, bollinger, last } from "./indicators";

type IndicatorResult = {
  rsi: (number | null)[];
  macd: ReturnType<typeof macd>;
  ema20: (number | null)[];
  ema50: (number | null)[];
  sma20: (number | null)[];
  bb: ReturnType<typeof bollinger>;
  rsiLast: number;
  macdLast: number;
  histLast: number;
  ema20Last: number;
  ema50Last: number;
  priceLast: number;
};

// Simple hash for cache key — uses length + last 3 prices
function hashPrices(closes: number[]): string {
  const len = closes.length;
  if (len === 0) return "empty";
  const tail = closes
    .slice(-3)
    .map((v) => v.toFixed(4))
    .join(",");
  return `${len}:${tail}`;
}

const indicatorCache = new Map<string, IndicatorResult>();
const MAX_CACHE = 20;

/**
 * Compute all indicators with memoization.
 * Returns cached result if price data hasn't changed.
 */
export function computeIndicators(closes: number[]): IndicatorResult {
  const key = hashPrices(closes);
  const cached = indicatorCache.get(key);
  if (cached) return cached;

  // Evict old entries
  if (indicatorCache.size >= MAX_CACHE) {
    const firstKey = indicatorCache.keys().next().value;
    if (firstKey !== undefined) indicatorCache.delete(firstKey);
  }

  const r = rsi(closes, 14);
  const m = macd(closes);
  const e20 = ema(closes, 20);
  const e50 = ema(closes, 50);
  const s20 = sma(closes, 20);
  const bb = bollinger(closes, 20, 2);

  const result: IndicatorResult = {
    rsi: r,
    macd: m,
    ema20: e20,
    ema50: e50,
    sma20: s20,
    bb,
    rsiLast: last(r) ?? 50,
    macdLast: last(m.macd) ?? 0,
    histLast: last(m.hist) ?? 0,
    ema20Last: last(e20) ?? 0,
    ema50Last: last(e50) ?? 0,
    priceLast: closes[closes.length - 1] ?? 0,
  };

  indicatorCache.set(key, result);
  return result;
}
