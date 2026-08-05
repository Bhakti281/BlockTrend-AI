import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";
import { cachedFetch } from "./api-cache";

const CG = "https://api.coingecko.com/api/v3";

export const COIN_META: Record<string, { id: string; symbol: string; name: string }> = {
  BTC: { id: "bitcoin", symbol: "BTC", name: "Bitcoin" },
  ETH: { id: "ethereum", symbol: "ETH", name: "Ethereum" },
  SOL: { id: "solana", symbol: "SOL", name: "Solana" },
  ADA: { id: "cardano", symbol: "ADA", name: "Cardano" },
  BNB: { id: "binancecoin", symbol: "BNB", name: "BNB" },
  XRP: { id: "ripple", symbol: "XRP", name: "XRP" },
};

const IdsSchema = z.object({ ids: z.array(z.string()).min(1).max(20) });

export type MarketRow = {
  id: string;
  symbol: string;
  name: string;
  image: string;
  current_price: number;
  price_change_percentage_24h: number;
  market_cap: number;
  total_volume: number;
  sparkline_in_7d?: { price: number[] };
};

// Cache TTLs optimized per endpoint volatility:
// - Markets: 15s (live prices need freshness)
// - OHLC: 60s (candle data changes less frequently)
// - Chart: 30s (balance between freshness and performance)
const MARKETS_TTL = 15_000;
const OHLC_TTL = 60_000;
const CHART_TTL = 30_000;

export const fetchMarkets = createServerFn({ method: "GET" })
  .inputValidator((data: unknown) => IdsSchema.parse(data))
  .handler(async ({ data }): Promise<MarketRow[]> => {
    const url =
      `${CG}/coins/markets?vs_currency=usd&ids=${data.ids.join(",")}` +
      `&order=market_cap_desc&per_page=20&page=1&sparkline=true&price_change_percentage=24h`;
    return cachedFetch<MarketRow[]>(url, { headers: { accept: "application/json" } }, MARKETS_TTL);
  });

const OhlcSchema = z.object({
  id: z.string(),
  days: z.number().int().min(1).max(365).default(30),
});

export type OhlcPoint = { t: number; o: number; h: number; l: number; c: number };

export const fetchOhlc = createServerFn({ method: "GET" })
  .inputValidator((data: unknown) => OhlcSchema.parse(data))
  .handler(async ({ data }): Promise<OhlcPoint[]> => {
    const url = `${CG}/coins/${data.id}/ohlc?vs_currency=usd&days=${data.days}`;
    const rows = await cachedFetch<[number, number, number, number, number][]>(
      url,
      { headers: { accept: "application/json" } },
      OHLC_TTL,
    );
    return rows.map(([t, o, h, l, c]) => ({ t, o, h, l, c }));
  });

const ChartSchema = z.object({
  id: z.string(),
  days: z.number().int().min(1).max(365).default(30),
});

export type ChartPoint = { t: number; price: number; volume: number };

export const fetchChart = createServerFn({ method: "GET" })
  .inputValidator((data: unknown) => ChartSchema.parse(data))
  .handler(async ({ data }): Promise<ChartPoint[]> => {
    const url = `${CG}/coins/${data.id}/market_chart?vs_currency=usd&days=${data.days}`;
    const j = await cachedFetch<{
      prices: [number, number][];
      total_volumes: [number, number][];
    }>(url, { headers: { accept: "application/json" } }, CHART_TTL);
    return j.prices.map(([t, price], i) => ({
      t,
      price,
      volume: j.total_volumes[i]?.[1] ?? 0,
    }));
  });
