import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { COIN_META } from "@/lib/coingecko.functions";
import { Sparkles, TrendingUp, TrendingDown, Minus, Info } from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Cell,
  Tooltip,
} from "recharts";

export const Route = createFileRoute("/_authenticated/ai-signals")({
  head: () => ({
    meta: [
      { title: "AI Signals — CryptoVision AI" },
      { name: "description", content: "AI-generated BUY / SELL / HOLD signals with explanations." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: AISignals,
});

type Signal = {
  symbol: string;
  name: string;
  action: "BUY" | "SELL" | "HOLD";
  confidence: number;
  expected: number;
  risk: "Low" | "Moderate" | "Elevated" | "High";
  horizon: "1H" | "24H" | "7D";
  contributions: { key: string; value: number }[];
  reason: string;
};

const signals: Signal[] = [
  {
    symbol: "BTC",
    name: "Bitcoin",
    action: "BUY",
    confidence: 87,
    expected: 4.2,
    risk: "Moderate",
    horizon: "24H",
    reason:
      "MACD crossover on the 4H, rising RSI (62), volume +18%, and strongly positive news sentiment.",
    contributions: [
      { key: "LSTM", value: 0.31 },
      { key: "XGBoost", value: 0.24 },
      { key: "MACD", value: 0.14 },
      { key: "RSI", value: 0.11 },
      { key: "Sentiment", value: 0.12 },
      { key: "News", value: 0.08 },
    ],
  },
  {
    symbol: "ETH",
    name: "Ethereum",
    action: "BUY",
    confidence: 74,
    expected: 3.1,
    risk: "Moderate",
    horizon: "24H",
    reason: "EMA20 crossing above EMA50, healthy volume, mixed but improving sentiment.",
    contributions: [
      { key: "LSTM", value: 0.28 },
      { key: "XGBoost", value: 0.19 },
      { key: "EMA", value: 0.18 },
      { key: "RSI", value: 0.09 },
      { key: "Sentiment", value: 0.14 },
      { key: "News", value: 0.12 },
    ],
  },
  {
    symbol: "SOL",
    name: "Solana",
    action: "HOLD",
    confidence: 55,
    expected: 0.4,
    risk: "Elevated",
    horizon: "24H",
    reason: "Consolidating below resistance; RSI neutral; model conviction low.",
    contributions: [
      { key: "LSTM", value: 0.22 },
      { key: "RSI", value: 0.19 },
      { key: "MACD", value: 0.16 },
      { key: "Sentiment", value: 0.18 },
      { key: "Volume", value: 0.13 },
      { key: "XGBoost", value: 0.12 },
    ],
  },
  {
    symbol: "ADA",
    name: "Cardano",
    action: "SELL",
    confidence: 68,
    expected: -2.7,
    risk: "High",
    horizon: "24H",
    reason: "Bearish divergence on RSI, negative headline sentiment, weakening momentum.",
    contributions: [
      { key: "RSI", value: 0.22 },
      { key: "LSTM", value: 0.21 },
      { key: "Sentiment", value: 0.19 },
      { key: "MACD", value: 0.14 },
      { key: "XGBoost", value: 0.12 },
      { key: "News", value: 0.12 },
    ],
  },
  {
    symbol: "BNB",
    name: "BNB",
    action: "BUY",
    confidence: 71,
    expected: 2.4,
    risk: "Moderate",
    horizon: "24H",
    reason: "Breakout above Bollinger midline, volume expansion, neutral-to-positive sentiment.",
    contributions: [
      { key: "Bollinger", value: 0.22 },
      { key: "Volume", value: 0.18 },
      { key: "LSTM", value: 0.24 },
      { key: "Sentiment", value: 0.12 },
      { key: "MACD", value: 0.12 },
      { key: "News", value: 0.12 },
    ],
  },
  {
    symbol: "XRP",
    name: "XRP",
    action: "HOLD",
    confidence: 58,
    expected: 0.9,
    risk: "Moderate",
    horizon: "24H",
    reason: "Range-bound; awaits catalyst; ensemble split.",
    contributions: [
      { key: "LSTM", value: 0.19 },
      { key: "XGBoost", value: 0.18 },
      { key: "Sentiment", value: 0.17 },
      { key: "RSI", value: 0.15 },
      { key: "News", value: 0.16 },
      { key: "MACD", value: 0.15 },
    ],
  },
];

const actionMeta: Record<Signal["action"], { cls: string; icon: typeof TrendingUp }> = {
  BUY: { cls: "text-[color:var(--bull)] bg-[color:var(--bull)]/15 border-[color:var(--bull)]/30", icon: TrendingUp },
  SELL: { cls: "text-[color:var(--bear)] bg-[color:var(--bear)]/15 border-[color:var(--bear)]/30", icon: TrendingDown },
  HOLD: { cls: "text-primary bg-primary/15 border-primary/30", icon: Minus },
};

function AISignals() {
  return (
    <PageShell
      title="AI Signals"
      subtitle="Ensemble of Random Forest + XGBoost + LSTM. Every call comes with SHAP feature contributions."
    >
      <div className="mb-4 flex items-start gap-2 rounded-lg border border-primary/30 bg-primary/5 p-3 text-xs text-muted-foreground">
        <Info className="mt-0.5 h-4 w-4 flex-shrink-0 text-primary" />
        Signals shown here are demo output from the ML contract. Wire the ML Evaluation page to
        your FastAPI service to replace with live model output.
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {signals.map((s) => {
          const meta = actionMeta[s.action];
          const Icon = meta.icon;
          const coin = COIN_META[s.symbol];
          return (
            <Card key={s.symbol} className="glass overflow-hidden border-border/60">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <div>
                  <div className="flex items-center gap-2">
                    <CardTitle className="font-display">{s.symbol}</CardTitle>
                    <span className="text-xs text-muted-foreground">{coin?.name ?? s.name}</span>
                  </div>
                  <div className="mt-0.5 text-[10px] uppercase tracking-widest text-muted-foreground">
                    Horizon · {s.horizon}
                  </div>
                </div>
                <Badge className={`gap-1 border ${meta.cls}`}>
                  <Icon className="h-3 w-3" />
                  {s.action}
                </Badge>
              </CardHeader>
              <CardContent>
                <div className="flex items-end justify-between">
                  <div>
                    <div className="text-[10px] uppercase text-muted-foreground">Confidence</div>
                    <div className="font-mono text-3xl font-bold">{s.confidence}%</div>
                  </div>
                  <div className="text-right">
                    <div className="text-[10px] uppercase text-muted-foreground">Expected</div>
                    <div
                      className={`font-mono text-lg font-semibold ${
                        s.expected >= 0 ? "text-[color:var(--bull)]" : "text-[color:var(--bear)]"
                      }`}
                    >
                      {s.expected >= 0 ? "+" : ""}
                      {s.expected.toFixed(2)}%
                    </div>
                    <Badge variant="outline" className="mt-1 text-[10px]">
                      Risk · {s.risk}
                    </Badge>
                  </div>
                </div>

                <Progress value={s.confidence} className="mt-4" />

                <p className="mt-4 rounded-lg bg-secondary/40 p-3 text-xs leading-relaxed text-muted-foreground">
                  <Sparkles className="mr-1.5 inline h-3 w-3 text-primary" />
                  {s.reason}
                </p>

                <div className="mt-4">
                  <div className="mb-2 text-[10px] uppercase tracking-widest text-muted-foreground">
                    Feature contribution (SHAP)
                  </div>
                  <div className="h-32">
                    <ResponsiveContainer>
                      <BarChart data={s.contributions} layout="vertical" margin={{ left: 6 }}>
                        <XAxis type="number" hide />
                        <YAxis
                          dataKey="key"
                          type="category"
                          width={72}
                          axisLine={false}
                          tickLine={false}
                          tick={{ fill: "var(--muted-foreground)", fontSize: 10 }}
                        />
                        <Tooltip
                          contentStyle={{
                            background: "var(--popover)",
                            border: "1px solid var(--border)",
                            borderRadius: 8,
                            fontSize: 12,
                          }}
                        />
                        <Bar dataKey="value" radius={[4, 4, 4, 4]}>
                          {s.contributions.map((_, i) => (
                            <Cell
                              key={i}
                              fill={
                                s.action === "SELL" ? "var(--bear)" : "var(--color-primary)"
                              }
                            />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </PageShell>
  );
}
