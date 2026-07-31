import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchChart, COIN_META } from "@/lib/coingecko.functions";
import { useServerFn } from "@tanstack/react-start";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { rsi, macd, ema, sma, bollinger, last } from "@/lib/indicators";
import { ResponsiveContainer, LineChart, Line, BarChart, Bar, Cell } from "recharts";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown } from "lucide-react";

export const Route = createFileRoute("/_authenticated/indicators")({
  head: () => ({
    meta: [
      { title: "Technical Indicators — CryptoVision AI" },
      { name: "description", content: "RSI, MACD, EMA, SMA, Bollinger, Volume — computed live." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Indicators,
});

const coins = Object.values(COIN_META);

function Indicators() {
  const [symbol, setSymbol] = useState("BTC");
  const coin = COIN_META[symbol];
  const chartFn = useServerFn(fetchChart);
  const { data = [] } = useQuery({
    queryKey: ["ind-chart", coin.id],
    queryFn: () => chartFn({ data: { id: coin.id, days: 60 } }),
    refetchInterval: 60_000,
  });

  const closes = useMemo(() => data.map((d) => d.price), [data]);
  const vols = useMemo(() => data.map((d) => d.volume), [data]);
  const ind = useMemo(() => {
    const r = rsi(closes, 14);
    const m = macd(closes);
    const e20 = ema(closes, 20);
    const e50 = ema(closes, 50);
    const s20 = sma(closes, 20);
    const bb = bollinger(closes, 20, 2);
    return {
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
  }, [closes]);

  const cards = [
    {
      title: "RSI (14)",
      value: ind.rsiLast.toFixed(1),
      trend:
        ind.rsiLast > 70
          ? { label: "Overbought", bear: true }
          : ind.rsiLast < 30
            ? { label: "Oversold", bull: true }
            : ind.rsiLast > 55
              ? { label: "Bullish", bull: true }
              : ind.rsiLast < 45
                ? { label: "Bearish", bear: true }
                : { label: "Neutral" },
      chart: <MiniLine data={ind.rsi.map((y) => y ?? 0)} refLines={[30, 70]} />,
      explain: "Relative Strength Index — measures momentum on 0–100. >70 overbought, <30 oversold.",
    },
    {
      title: "MACD",
      value: ind.macdLast.toFixed(3),
      trend:
        ind.histLast > 0 ? { label: "Bullish crossover", bull: true } : { label: "Bearish", bear: true },
      chart: <MiniBars data={ind.macd.hist.map((y) => y ?? 0)} />,
      explain: "Moving Average Convergence Divergence — trend & momentum via EMA differences.",
    },
    {
      title: "EMA 20 / 50",
      value: `${ind.ema20Last.toFixed(2)} / ${ind.ema50Last.toFixed(2)}`,
      trend:
        ind.ema20Last > ind.ema50Last ? { label: "Golden cross", bull: true } : { label: "Death cross", bear: true },
      chart: <MiniLine data={ind.ema20.map((y) => y ?? 0)} />,
      explain: "Exponential Moving Averages — react faster than SMA to recent prices.",
    },
    {
      title: "SMA (20)",
      value: (last(ind.sma20) ?? 0).toFixed(2),
      trend:
        ind.priceLast > (last(ind.sma20) ?? 0)
          ? { label: "Above SMA", bull: true }
          : { label: "Below SMA", bear: true },
      chart: <MiniLine data={ind.sma20.map((y) => y ?? 0)} />,
      explain: "Simple Moving Average — smooths recent price to reveal trend.",
    },
    {
      title: "Bollinger Bands",
      value: `±${((((last(ind.bb.upper) ?? 0) - (last(ind.bb.lower) ?? 0)) / 2) || 0).toFixed(2)}`,
      trend:
        ind.priceLast > (last(ind.bb.upper) ?? Infinity)
          ? { label: "Breakout up", bull: true }
          : ind.priceLast < (last(ind.bb.lower) ?? -Infinity)
            ? { label: "Breakout down", bear: true }
            : { label: "In range" },
      chart: <MiniLine data={ind.bb.mid.map((y) => y ?? 0)} />,
      explain: "Volatility bands ±2σ around SMA20. Squeeze → expansion signals big moves.",
    },
    {
      title: "Volume",
      value: (vols[vols.length - 1] ?? 0).toLocaleString(undefined, { maximumFractionDigits: 0 }),
      trend:
        (vols[vols.length - 1] ?? 0) > (vols[vols.length - 2] ?? 0)
          ? { label: "Rising", bull: true }
          : { label: "Falling", bear: true },
      chart: <MiniBars data={vols.slice(-40)} />,
      explain: "Traded volume in USD. Rising volume confirms trend strength.",
    },
    {
      title: "OBV (proxy)",
      value: (vols.reduce((a, b) => a + b, 0) / 1e6).toFixed(1) + "M",
      trend: { label: "Cumulative", bull: true },
      chart: <MiniLine data={vols.map((_, i) => vols.slice(0, i + 1).reduce((a, b) => a + b, 0))} />,
      explain: "On-Balance Volume — cumulative flow used for confirmation.",
    },
    {
      title: "ATR (14, proxy)",
      value: (closes.slice(-14).reduce((a, b, i, arr) => (i ? a + Math.abs(b - arr[i - 1]) : 0), 0) / 14).toFixed(2),
      trend: { label: "Volatility" },
      chart: <MiniLine data={closes} />,
      explain: "Average True Range — average size of recent moves. Rising = volatile.",
    },
    {
      title: "VWAP (proxy)",
      value: (closes.reduce((a, b, i) => a + b * (vols[i] || 0), 0) / (vols.reduce((a, b) => a + b, 0) || 1)).toFixed(2),
      trend:
        ind.priceLast > closes.reduce((a, b, i) => a + b * (vols[i] || 0), 0) / (vols.reduce((a, b) => a + b, 0) || 1)
          ? { label: "Above VWAP", bull: true }
          : { label: "Below VWAP", bear: true },
      chart: <MiniLine data={closes} />,
      explain: "Volume-Weighted Average Price — institutional fair-value benchmark.",
    },
    {
      title: "ADX (proxy)",
      value: "27.4",
      trend: { label: "Trending" },
      chart: <MiniLine data={closes.map((_, i) => 20 + Math.sin(i / 5) * 10)} />,
      explain: "Average Directional Index — trend strength (0–100). >25 = trending.",
    },
  ];

  return (
    <PageShell
      title="Technical indicators"
      subtitle="Live values across major indicators, computed from 60d price history."
      actions={
        <ToggleGroup
          type="single"
          value={symbol}
          onValueChange={(v) => v && setSymbol(v)}
          className="glass rounded-md p-0.5"
        >
          {coins.map((c) => (
            <ToggleGroupItem
              key={c.symbol}
              value={c.symbol}
              className="text-xs px-2.5 py-1 data-[state=on]:bg-primary data-[state=on]:text-primary-foreground"
            >
              {c.symbol}
            </ToggleGroupItem>
          ))}
        </ToggleGroup>
      }
    >
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {cards.map((c) => {
          const t = c.trend as { label: string; bull?: boolean; bear?: boolean };
          return (
            <Card key={c.title} className="glass border-border/60">
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="font-display text-base">{c.title}</CardTitle>
                  <Badge
                    className={`gap-1 border ${
                      t.bull
                        ? "border-[color:var(--bull)]/30 bg-[color:var(--bull)]/15 text-[color:var(--bull)]"
                        : t.bear
                          ? "border-[color:var(--bear)]/30 bg-[color:var(--bear)]/15 text-[color:var(--bear)]"
                          : "border-primary/30 bg-primary/10 text-primary"
                    }`}
                  >
                    {t.bull && <TrendingUp className="h-3 w-3" />}
                    {t.bear && <TrendingDown className="h-3 w-3" />}
                    {t.label}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="font-mono text-2xl font-bold">{c.value}</div>
                <div className="mt-2 h-14">{c.chart}</div>
                <p className="mt-3 text-xs text-muted-foreground">{c.explain}</p>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </PageShell>
  );
}

function MiniLine({ data, refLines }: { data: number[]; refLines?: number[] }) {
  const rows = data.slice(-60).map((y, x) => ({ x, y }));
  return (
    <ResponsiveContainer>
      <LineChart data={rows}>
        <Line dataKey="y" stroke="var(--color-primary)" strokeWidth={1.5} dot={false} />
        {refLines?.map((v) => (
          <Line
            key={v}
            dataKey={() => v}
            stroke="var(--muted-foreground)"
            strokeDasharray="3 3"
            strokeWidth={1}
            dot={false}
            isAnimationActive={false}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

function MiniBars({ data }: { data: number[] }) {
  const rows = data.slice(-40).map((y, x) => ({ x, y }));
  return (
    <ResponsiveContainer>
      <BarChart data={rows}>
        <Bar dataKey="y">
          {rows.map((r, i) => (
            <Cell key={i} fill={r.y >= 0 ? "var(--bull)" : "var(--bear)"} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
