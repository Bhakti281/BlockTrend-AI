import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { useQuery } from "@tanstack/react-query";
import { fetchMarkets, COIN_META } from "@/lib/coingecko.functions";
import { useServerFn } from "@tanstack/react-start";
import { formatUsd, formatPct } from "@/lib/format";
import { Card } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
} from "recharts";

export const Route = createFileRoute("/_authenticated/multi-coin")({
  head: () => ({
    meta: [
      { title: "Multi-Coin Analysis — CryptoVision AI" },
      {
        name: "description",
        content: "Compare price, volume, indicators, prediction, and risk across coins.",
      },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: MultiCoin,
});

const ids = Object.values(COIN_META).map((c) => c.id);

// Radar data is static — defined once outside component to avoid re-creation
const radar = [
  { metric: "Momentum", BTC: 82, ETH: 74, SOL: 60, ADA: 40, BNB: 68, XRP: 55 },
  { metric: "Volume", BTC: 88, ETH: 80, SOL: 66, ADA: 45, BNB: 62, XRP: 51 },
  { metric: "Sentiment", BTC: 85, ETH: 68, SOL: 74, ADA: 42, BNB: 66, XRP: 52 },
  { metric: "Volatility", BTC: 55, ETH: 60, SOL: 78, ADA: 62, BNB: 58, XRP: 65 },
  { metric: "Trend", BTC: 84, ETH: 72, SOL: 63, ADA: 38, BNB: 70, XRP: 50 },
];

const colors = [
  "var(--chart-1)",
  "var(--chart-2)",
  "var(--chart-3)",
  "var(--chart-4)",
  "var(--chart-5)",
  "var(--color-primary)",
];

function MultiCoin() {
  const fetch = useServerFn(fetchMarkets);
  const { data = [] } = useQuery({
    // Share cache with dashboard/live-prices for instant navigation
    queryKey: ["markets", ids.join(",")],
    queryFn: () => fetch({ data: { ids } }),
    refetchInterval: 30_000,
    placeholderData: (prev) => prev,
    staleTime: 15_000,
  });

  return (
    <PageShell
      title="Multi-coin analysis"
      subtitle="Side-by-side price, prediction, sentiment, and risk across the majors."
    >
      <Card className="glass border-border/60 p-0 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Coin</TableHead>
              <TableHead>Price</TableHead>
              <TableHead>24H</TableHead>
              <TableHead>Volume</TableHead>
              <TableHead>Signal</TableHead>
              <TableHead>Sentiment</TableHead>
              <TableHead>Risk</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((c, i) => {
              const up = c.price_change_percentage_24h >= 0;
              const meta = ["BUY", "BUY", "HOLD", "SELL", "BUY", "HOLD"][i % 6] as
                "BUY" | "SELL" | "HOLD";
              const cls =
                meta === "BUY"
                  ? "border-[color:var(--bull)]/30 bg-[color:var(--bull)]/15 text-[color:var(--bull)]"
                  : meta === "SELL"
                    ? "border-[color:var(--bear)]/30 bg-[color:var(--bear)]/15 text-[color:var(--bear)]"
                    : "border-primary/30 bg-primary/10 text-primary";
              return (
                <TableRow key={c.id}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <img src={c.image} alt="" className="h-6 w-6 rounded-full" />
                      <div>
                        <div className="text-sm font-semibold">{c.symbol.toUpperCase()}</div>
                        <div className="text-[10px] text-muted-foreground">{c.name}</div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="font-mono">{formatUsd(c.current_price)}</TableCell>
                  <TableCell
                    className={`font-mono ${up ? "text-[color:var(--bull)]" : "text-[color:var(--bear)]"}`}
                  >
                    {formatPct(c.price_change_percentage_24h)}
                  </TableCell>
                  <TableCell className="font-mono">{formatUsd(c.total_volume)}</TableCell>
                  <TableCell>
                    <Badge className={`border ${cls}`}>{meta}</Badge>
                  </TableCell>
                  <TableCell className="font-mono">
                    {[0.71, 0.44, 0.62, -0.31, 0.5, 0.08][i]?.toFixed(2)}
                  </TableCell>
                  <TableCell>
                    <span className="text-xs text-muted-foreground">
                      {["Moderate", "Moderate", "Elevated", "High", "Moderate", "Moderate"][i]}
                    </span>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </Card>

      <Card className="glass mt-6 border-border/60 p-6">
        <div className="mb-4">
          <h3 className="font-display text-base font-semibold">Multi-factor radar</h3>
          <p className="text-xs text-muted-foreground">
            Momentum, volume, sentiment, volatility, trend — normalized.
          </p>
        </div>
        <div className="h-96">
          <ResponsiveContainer>
            <RadarChart data={radar}>
              <PolarGrid stroke="var(--border)" />
              <PolarAngleAxis
                dataKey="metric"
                tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
              />
              <PolarRadiusAxis tick={false} axisLine={false} />
              {Object.keys(COIN_META).map((s, i) => (
                <Radar key={s} dataKey={s} stroke={colors[i]} fill={colors[i]} fillOpacity={0.15} />
              ))}
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </PageShell>
  );
}
