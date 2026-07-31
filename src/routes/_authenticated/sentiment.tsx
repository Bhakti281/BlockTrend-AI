import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, RadialBarChart, RadialBar, PolarAngleAxis } from "recharts";
import { Badge } from "@/components/ui/badge";
import { Sparkles } from "lucide-react";

export const Route = createFileRoute("/_authenticated/sentiment")({
  head: () => ({
    meta: [
      { title: "Sentiment Analysis — CryptoVision AI" },
      { name: "description", content: "FinBERT sentiment across crypto headlines." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Sentiment,
});

const distribution = [
  { name: "Positive", value: 58, color: "var(--bull)" },
  { name: "Neutral", value: 27, color: "var(--muted-foreground)" },
  { name: "Negative", value: 15, color: "var(--bear)" },
];

const gauge = [{ name: "score", value: 71, fill: "var(--color-primary)" }];

const headlines = [
  { title: "Bitcoin ETF inflows hit record high as institutions rotate in", src: "CoinDesk", sent: "Positive", score: 0.92, coin: "BTC" },
  { title: "Solana network processes 5B transactions milestone", src: "The Block", sent: "Positive", score: 0.81, coin: "SOL" },
  { title: "Regulator delays ETH staking approval, market reacts cautiously", src: "Bloomberg", sent: "Negative", score: -0.44, coin: "ETH" },
  { title: "BNB Chain launches new developer grant program", src: "CryptoSlate", sent: "Positive", score: 0.62, coin: "BNB" },
  { title: "XRP lawsuit ruling reopens speculation on retail flows", src: "Decrypt", sent: "Neutral", score: 0.05, coin: "XRP" },
  { title: "Cardano ecosystem TVL declines month-over-month", src: "Messari", sent: "Negative", score: -0.31, coin: "ADA" },
];

function Sentiment() {
  return (
    <PageShell
      title="Sentiment analysis"
      subtitle="FinBERT-scored crypto headlines fused into the AI signal engine."
    >
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Sentiment distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-56">
              <ResponsiveContainer>
                <PieChart>
                  <Pie data={distribution} innerRadius={60} outerRadius={80} paddingAngle={4} dataKey="value">
                    {distribution.map((d, i) => (
                      <Cell key={i} fill={d.color} stroke="transparent" />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-3 space-y-2 text-xs">
              {distribution.map((d) => (
                <div key={d.name} className="flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full" style={{ background: d.color }} /> {d.name}
                  </span>
                  <span className="font-mono">{d.value}%</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Aggregate score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-56">
              <ResponsiveContainer>
                <RadialBarChart innerRadius="70%" outerRadius="100%" data={gauge} startAngle={210} endAngle={-30}>
                  <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
                  <RadialBar dataKey="value" cornerRadius={10} background={{ fill: "var(--secondary)" }} />
                </RadialBarChart>
              </ResponsiveContainer>
            </div>
            <div className="text-center">
              <div className="font-mono text-3xl font-bold text-[color:var(--bull)]">+0.71</div>
              <div className="text-xs text-muted-foreground">128 headlines · last 24h</div>
            </div>
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 font-display text-base">
              <Sparkles className="h-4 w-4 text-primary" /> AI summary
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm leading-relaxed text-muted-foreground">
            Overall sentiment across major crypto assets is <b className="text-foreground">strongly positive</b>,
            driven by record BTC ETF inflows and Solana's transaction milestone. Some caution around
            ETH staking regulation and Cardano TVL decline is keeping the neutral bucket meaningful.
            Combined with rising volume and MACD crossover on BTC, the model reads this as a
            <b className="text-[color:var(--bull)]"> bullish 24h backdrop</b>.
          </CardContent>
        </Card>
      </div>

      <Card className="glass mt-6 border-border/60">
        <CardHeader>
          <CardTitle className="font-display text-base">Latest headlines</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {headlines.map((h) => (
            <div
              key={h.title}
              className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-border/50 bg-secondary/20 p-3 text-sm"
            >
              <div className="flex-1 min-w-[240px]">
                <div className="font-medium">{h.title}</div>
                <div className="mt-0.5 text-xs text-muted-foreground">
                  {h.src} · <span className="font-mono">{h.coin}</span>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`font-mono text-sm ${
                    h.score > 0.2
                      ? "text-[color:var(--bull)]"
                      : h.score < -0.2
                        ? "text-[color:var(--bear)]"
                        : "text-muted-foreground"
                  }`}
                >
                  {h.score > 0 ? "+" : ""}
                  {h.score.toFixed(2)}
                </span>
                <Badge
                  variant="outline"
                  className={
                    h.sent === "Positive"
                      ? "border-[color:var(--bull)]/30 text-[color:var(--bull)]"
                      : h.sent === "Negative"
                        ? "border-[color:var(--bear)]/30 text-[color:var(--bear)]"
                        : ""
                  }
                >
                  {h.sent}
                </Badge>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </PageShell>
  );
}
