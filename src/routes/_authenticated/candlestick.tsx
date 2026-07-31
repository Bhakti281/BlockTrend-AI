import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchOhlc, fetchChart, COIN_META } from "@/lib/coingecko.functions";
import { useServerFn } from "@tanstack/react-start";
import { Card } from "@/components/ui/card";
import {
  ComposedChart,
  Bar,
  Line,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
  ReferenceLine,
  Cell,
} from "recharts";
import { formatUsd } from "@/lib/format";
import { ema, bollinger } from "@/lib/indicators";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";

export const Route = createFileRoute("/_authenticated/candlestick")({
  head: () => ({
    meta: [
      { title: "Candlestick Charts — CryptoVision AI" },
      { name: "description", content: "Interactive candlestick charts with EMA & Bollinger overlays." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Candles,
});

const coins = Object.values(COIN_META);

function Candles() {
  const [symbol, setSymbol] = useState("BTC");
  const [days, setDays] = useState<number>(30);
  const [overlay, setOverlay] = useState<"none" | "ema" | "bollinger">("ema");

  const coin = COIN_META[symbol];
  const ohlcFn = useServerFn(fetchOhlc);
  const chartFn = useServerFn(fetchChart);

  const { data: ohlc = [] } = useQuery({
    queryKey: ["ohlc", coin.id, days],
    queryFn: () => ohlcFn({ data: { id: coin.id, days } }),
    refetchInterval: 60_000,
  });

  const { data: chartRows = [] } = useQuery({
    queryKey: ["chart", coin.id, days],
    queryFn: () => chartFn({ data: { id: coin.id, days } }),
    refetchInterval: 60_000,
  });

  const rows = useMemo(() => {
    const closes = ohlc.map((r) => r.c);
    const e20 = ema(closes, 20);
    const e50 = ema(closes, 50);
    const bb = bollinger(closes, 20, 2);
    return ohlc.map((r, i) => ({
      t: r.t,
      label: new Date(r.t).toLocaleDateString(undefined, { month: "short", day: "numeric" }),
      o: r.o,
      h: r.h,
      l: r.l,
      c: r.c,
      base: Math.min(r.o, r.c),
      body: Math.abs(r.c - r.o),
      wickL: Math.abs(Math.min(r.o, r.c) - r.l),
      wickH: Math.abs(r.h - Math.max(r.o, r.c)),
      up: r.c >= r.o,
      ema20: e20[i] ?? undefined,
      ema50: e50[i] ?? undefined,
      bbUpper: bb.upper[i] ?? undefined,
      bbLower: bb.lower[i] ?? undefined,
      bbMid: bb.mid[i] ?? undefined,
    }));
  }, [ohlc]);

  const volumeRows = useMemo(() => {
    // downsample daily volume
    const bucket: Record<string, number> = {};
    for (const p of chartRows) {
      const k = new Date(p.t).toISOString().slice(0, 10);
      bucket[k] = (bucket[k] ?? 0) + p.volume;
    }
    return Object.entries(bucket)
      .slice(-days)
      .map(([k, v]) => ({ label: k.slice(5), v }));
  }, [chartRows, days]);

  return (
    <PageShell
      title="Candlestick charts"
      subtitle="OHLC candles with EMA / Bollinger overlays and volume."
      actions={
        <div className="flex flex-wrap items-center gap-2">
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
          <ToggleGroup
            type="single"
            value={String(days)}
            onValueChange={(v) => v && setDays(+v)}
            className="glass rounded-md p-0.5"
          >
            {[
              [1, "1D"],
              [7, "7D"],
              [30, "30D"],
              [90, "90D"],
              [365, "1Y"],
            ].map(([d, l]) => (
              <ToggleGroupItem
                key={d}
                value={String(d)}
                className="text-xs px-2.5 py-1 data-[state=on]:bg-primary data-[state=on]:text-primary-foreground"
              >
                {l}
              </ToggleGroupItem>
            ))}
          </ToggleGroup>
          <ToggleGroup
            type="single"
            value={overlay}
            onValueChange={(v) => v && setOverlay(v as typeof overlay)}
            className="glass rounded-md p-0.5"
          >
            <ToggleGroupItem value="ema" className="text-xs px-2.5 py-1 data-[state=on]:bg-primary data-[state=on]:text-primary-foreground">EMA</ToggleGroupItem>
            <ToggleGroupItem value="bollinger" className="text-xs px-2.5 py-1 data-[state=on]:bg-primary data-[state=on]:text-primary-foreground">Bollinger</ToggleGroupItem>
            <ToggleGroupItem value="none" className="text-xs px-2.5 py-1 data-[state=on]:bg-primary data-[state=on]:text-primary-foreground">None</ToggleGroupItem>
          </ToggleGroup>
        </div>
      }
    >
      <Card className="glass border-border/60 p-4">
        <div className="h-[440px] w-full">
          <ResponsiveContainer>
            <ComposedChart data={rows} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <XAxis dataKey="label" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} minTickGap={24} />
              <YAxis
                domain={["auto", "auto"]}
                tick={{ fill: "var(--muted-foreground)", fontSize: 10 }}
                tickLine={false}
                axisLine={false}
                width={72}
                tickFormatter={(v) => formatUsd(v as number)}
              />
              <Tooltip
                contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8, fontSize: 12 }}
                formatter={(v: number | string) => (typeof v === "number" ? formatUsd(v) : v)}
                labelFormatter={(l) => `Date: ${l}`}
              />

              {/* wick */}
              <Bar dataKey="l" stackId="wick" fill="transparent" isAnimationActive={false} />
              <Bar dataKey="wickL" stackId="wick" isAnimationActive={false}>
                {rows.map((r, i) => (
                  <Cell key={i} fill={r.up ? "var(--bull)" : "var(--bear)"} />
                ))}
              </Bar>
              <Bar dataKey="body" stackId="wick" isAnimationActive={false}>
                {rows.map((r, i) => (
                  <Cell key={i} fill={r.up ? "var(--bull)" : "var(--bear)"} />
                ))}
              </Bar>
              <Bar dataKey="wickH" stackId="wick" isAnimationActive={false}>
                {rows.map((r, i) => (
                  <Cell key={i} fill={r.up ? "var(--bull)" : "var(--bear)"} />
                ))}
              </Bar>

              {overlay === "ema" && (
                <>
                  <Line dataKey="ema20" stroke="var(--color-primary)" dot={false} strokeWidth={1.5} />
                  <Line dataKey="ema50" stroke="var(--chart-2)" dot={false} strokeWidth={1.5} />
                </>
              )}
              {overlay === "bollinger" && (
                <>
                  <Line dataKey="bbUpper" stroke="var(--chart-2)" dot={false} strokeWidth={1} strokeDasharray="3 3" />
                  <Line dataKey="bbMid" stroke="var(--color-primary)" dot={false} strokeWidth={1.5} />
                  <Line dataKey="bbLower" stroke="var(--chart-2)" dot={false} strokeWidth={1} strokeDasharray="3 3" />
                </>
              )}
              <ReferenceLine y={0} stroke="transparent" />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 h-32">
          <ResponsiveContainer>
            <ComposedChart data={volumeRows}>
              <XAxis dataKey="label" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickLine={false} axisLine={false} minTickGap={24} />
              <YAxis hide />
              <Tooltip
                contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8, fontSize: 12 }}
                formatter={(v: number | string) => (typeof v === "number" ? formatUsd(v) : v)}
              />
              <Bar dataKey="v" fill="var(--color-primary)" opacity={0.55} radius={[4, 4, 0, 0]} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </PageShell>
  );
}
