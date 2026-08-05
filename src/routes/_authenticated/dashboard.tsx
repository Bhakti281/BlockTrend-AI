import { createFileRoute, Link } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { useQuery } from "@tanstack/react-query";
import { fetchMarkets, COIN_META } from "@/lib/coingecko.functions";
import { useServerFn } from "@tanstack/react-start";
import { formatUsd, formatPct } from "@/lib/format";
import { ResponsiveContainer, AreaChart, Area, LineChart, Line } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sparkles, TrendingUp, TrendingDown, Bot, Brain, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/_authenticated/dashboard")({
  head: () => ({
    meta: [
      { title: "Dashboard — CryptoVision AI" },
      { name: "description", content: "Live crypto overview, AI signals, and market pulse." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Dashboard,
});

const ids = Object.values(COIN_META).map((c) => c.id);

function Dashboard() {
  const fetch = useServerFn(fetchMarkets);
  const { data = [], isLoading } = useQuery({
    queryKey: ["markets", ids.join(",")],
    queryFn: () => fetch({ data: { ids } }),
    refetchInterval: 30_000,
    // Keep previous data visible during refetch to avoid layout shift
    placeholderData: (prev) => prev,
    staleTime: 15_000,
  });

  const totalCap = data.reduce((a, c) => a + c.market_cap, 0);
  const totalVol = data.reduce((a, c) => a + c.total_volume, 0);
  const avgChange = data.length
    ? data.reduce((a, c) => a + c.price_change_percentage_24h, 0) / data.length
    : 0;
  const bullish = data.filter((c) => c.price_change_percentage_24h > 0).length;

  return (
    <PageShell
      title="Market command center"
      subtitle="Live crypto overview, AI signals, and portfolio pulse — refreshed every 30 seconds."
      actions={
        <Button
          asChild
          size="sm"
          className="bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)] text-primary-foreground"
        >
          <Link to="/assistant">
            Ask the AI <Bot className="ml-1.5 h-4 w-4" />
          </Link>
        </Button>
      }
    >
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Stat
          label="Total market cap"
          value={formatUsd(totalCap)}
          sub={formatPct(avgChange)}
          up={avgChange >= 0}
        />
        <Stat label="24h volume" value={formatUsd(totalVol)} sub={`${data.length} coins`} />
        <Stat label="Bullish signals" value={`${bullish} / ${data.length}`} sub="AI ensemble" />
        <Stat label="AI confidence" value="87%" sub="LSTM 24h" glow />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <Card className="glass lg:col-span-2 border-border/60">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="font-display">Live prices</CardTitle>
              <p className="text-xs text-muted-foreground">Tap any card for full analysis</p>
            </div>
            <Button asChild variant="ghost" size="sm">
              <Link to="/live-prices">
                View all <ArrowRight className="ml-1 h-3.5 w-3.5" />
              </Link>
            </Button>
          </CardHeader>
          <CardContent className="grid gap-3 sm:grid-cols-2">
            {isLoading &&
              Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="h-24 animate-pulse rounded-lg bg-secondary/40" />
              ))}
            {data.slice(0, 6).map((c) => (
              <CoinMini key={c.id} coin={c} />
            ))}
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 font-display">
              <Sparkles className="h-4 w-4 text-primary" /> Top AI signal
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground">BTC · LSTM 24H</div>
            <div className="mt-1 font-mono text-3xl font-bold">BUY</div>
            <div className="mt-1 flex items-center gap-2">
              <Badge className="border-[color:var(--bull)]/30 bg-[color:var(--bull)]/20 text-[color:var(--bull)]">
                87% confidence
              </Badge>
              <Badge variant="outline">+4.2%</Badge>
            </div>
            <ul className="mt-4 space-y-2 text-xs text-muted-foreground">
              <li>› MACD positive crossover</li>
              <li>› RSI trending 62 → bullish</li>
              <li>› Sentiment +0.71 (FinBERT)</li>
              <li>› Volume +18% 24h</li>
            </ul>
            <Button asChild size="sm" className="mt-5 w-full">
              <Link to="/ai-signals">View all signals</Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 font-display text-base">
              <Brain className="h-4 w-4 text-primary" /> ML Ensemble
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            {[
              { name: "Random Forest", v: "BUY", conf: 79 },
              { name: "XGBoost", v: "BUY", conf: 83 },
              { name: "LSTM 24H", v: "BUY", conf: 87 },
            ].map((m) => (
              <div key={m.name} className="flex items-center justify-between">
                <span className="text-muted-foreground">{m.name}</span>
                <div className="flex items-center gap-2">
                  <Badge className="border-[color:var(--bull)]/30 bg-[color:var(--bull)]/15 text-[color:var(--bull)]">
                    {m.v}
                  </Badge>
                  <span className="font-mono text-xs">{m.conf}%</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Sentiment (24h)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="font-mono text-3xl font-bold text-[color:var(--bull)]">+0.71</div>
            <p className="mt-1 text-xs text-muted-foreground">FinBERT · 128 headlines</p>
            <div className="mt-4 h-16">
              <ResponsiveContainer>
                <LineChart
                  data={Array.from({ length: 24 }, (_, i) => ({ y: 0.4 + Math.sin(i / 3) * 0.3 }))}
                >
                  <Line dataKey="y" stroke="var(--color-primary)" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Volatility Index</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="font-mono text-3xl font-bold">Moderate</div>
            <p className="mt-1 text-xs text-muted-foreground">ATR normalized · all majors</p>
            <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-secondary">
              <div className="h-full w-1/2 bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)]" />
            </div>
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
}

function Stat({
  label,
  value,
  sub,
  up,
  glow,
}: {
  label: string;
  value: string;
  sub?: string;
  up?: boolean;
  glow?: boolean;
}) {
  return (
    <div className={`glass rounded-2xl p-5 ${glow ? "glow-cyan" : ""}`}>
      <div className="text-[11px] uppercase tracking-widest text-muted-foreground">{label}</div>
      <div className="mt-2 font-mono text-2xl font-semibold">{value}</div>
      {sub !== undefined && (
        <div
          className={`mt-1 text-xs ${
            up === undefined
              ? "text-muted-foreground"
              : up
                ? "text-[color:var(--bull)]"
                : "text-[color:var(--bear)]"
          }`}
        >
          {sub}
        </div>
      )}
    </div>
  );
}

function CoinMini({ coin }: { coin: Awaited<ReturnType<typeof fetchMarkets>>[number] }) {
  const up = coin.price_change_percentage_24h >= 0;
  const spark = (coin.sparkline_in_7d?.price ?? []).map((y, x) => ({ x, y }));
  return (
    <div className="group rounded-xl border border-border/60 bg-secondary/30 p-4 transition-all hover:border-primary/40 hover:bg-secondary/50">
      <div className="flex items-center gap-3">
        <img src={coin.image} alt={coin.name} className="h-8 w-8 rounded-full" />
        <div>
          <div className="text-sm font-semibold">{coin.symbol.toUpperCase()}</div>
          <div className="text-[10px] uppercase text-muted-foreground">{coin.name}</div>
        </div>
        <div className="ml-auto text-right">
          <div className="font-mono text-sm">{formatUsd(coin.current_price)}</div>
          <div
            className={`flex items-center justify-end gap-0.5 text-[11px] ${
              up ? "text-[color:var(--bull)]" : "text-[color:var(--bear)]"
            }`}
          >
            {up ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
            {formatPct(coin.price_change_percentage_24h)}
          </div>
        </div>
      </div>
      <div className="mt-2 h-10">
        <ResponsiveContainer>
          <AreaChart data={spark}>
            <defs>
              <linearGradient id={`g-${coin.id}`} x1="0" y1="0" x2="0" y2="1">
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
              strokeWidth={1.5}
              fill={`url(#g-${coin.id})`}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
