import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { useQuery } from "@tanstack/react-query";
import { fetchMarkets, COIN_META } from "@/lib/coingecko.functions";
import { useServerFn } from "@tanstack/react-start";
import { formatUsd, formatPct } from "@/lib/format";
import { ResponsiveContainer, AreaChart, Area } from "recharts";
import { TrendingUp, TrendingDown } from "lucide-react";

export const Route = createFileRoute("/_authenticated/live-prices")({
  head: () => ({
    meta: [
      { title: "Live Prices — CryptoVision AI" },
      { name: "description", content: "Real-time crypto prices across major coins." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: LivePrices,
});

const ids = Object.values(COIN_META).map((c) => c.id);

function LivePrices() {
  const fetch = useServerFn(fetchMarkets);
  const {
    data = [],
    isLoading,
    dataUpdatedAt,
  } = useQuery({
    // Use same query key as dashboard to share cached data
    queryKey: ["markets", ids.join(",")],
    queryFn: () => fetch({ data: { ids } }),
    refetchInterval: 15_000,
    // Keep previous data visible during refetch
    placeholderData: (prev) => prev,
    staleTime: 10_000,
  });

  return (
    <PageShell
      title="Live prices"
      subtitle={`Streaming from CoinGecko · last update ${new Date(dataUpdatedAt).toLocaleTimeString()}`}
    >
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {isLoading &&
          Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-56 animate-pulse rounded-2xl bg-secondary/40" />
          ))}
        {data.map((c) => {
          const up = c.price_change_percentage_24h >= 0;
          const spark = (c.sparkline_in_7d?.price ?? []).map((y, x) => ({ x, y }));
          return (
            <div
              key={c.id}
              className="glass group relative overflow-hidden rounded-2xl p-6 transition-all hover:-translate-y-0.5 hover:border-primary/40"
            >
              <div className="flex items-center gap-3">
                <img src={c.image} alt={c.name} className="h-10 w-10 rounded-full" />
                <div>
                  <div className="text-lg font-semibold">{c.symbol.toUpperCase()}</div>
                  <div className="text-xs text-muted-foreground">{c.name}</div>
                </div>
                <div
                  className={`ml-auto flex items-center gap-1 rounded-md px-2 py-1 text-xs ${
                    up
                      ? "bg-[color:var(--bull)]/15 text-[color:var(--bull)]"
                      : "bg-[color:var(--bear)]/15 text-[color:var(--bear)]"
                  }`}
                >
                  {up ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                  {formatPct(c.price_change_percentage_24h)}
                </div>
              </div>

              <div className="mt-6 font-mono text-3xl font-bold">{formatUsd(c.current_price)}</div>

              <div className="mt-2 h-20">
                <ResponsiveContainer>
                  <AreaChart data={spark}>
                    <defs>
                      <linearGradient id={`grad-${c.id}`} x1="0" y1="0" x2="0" y2="1">
                        <stop
                          offset="0%"
                          stopColor={up ? "var(--bull)" : "var(--bear)"}
                          stopOpacity={0.5}
                        />
                        <stop
                          offset="100%"
                          stopColor={up ? "var(--bull)" : "var(--bear)"}
                          stopOpacity={0}
                        />
                      </linearGradient>
                    </defs>
                    <Area
                      type="monotone"
                      dataKey="y"
                      stroke={up ? "var(--bull)" : "var(--bear)"}
                      strokeWidth={2}
                      fill={`url(#grad-${c.id})`}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="mt-4 grid grid-cols-2 gap-3 border-t border-border/60 pt-4 text-xs">
                <div>
                  <div className="text-[10px] uppercase text-muted-foreground">Market cap</div>
                  <div className="mt-0.5 font-mono">{formatUsd(c.market_cap)}</div>
                </div>
                <div>
                  <div className="text-[10px] uppercase text-muted-foreground">24h volume</div>
                  <div className="mt-0.5 font-mono">{formatUsd(c.total_volume)}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </PageShell>
  );
}
