import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from "recharts";
import { formatUsd, formatPct } from "@/lib/format";
import { Plus, Wallet } from "lucide-react";

export const Route = createFileRoute("/_authenticated/portfolio")({
  head: () => ({
    meta: [
      { title: "Portfolio — CryptoVision AI" },
      { name: "description", content: "Track holdings, ROI, and AI prediction impact on your portfolio." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Portfolio,
});

const holdings = [
  { symbol: "BTC", qty: 0.42, cost: 58200, price: 67842, color: "var(--chart-1)" },
  { symbol: "ETH", qty: 5.1, cost: 2900, price: 3241, color: "var(--chart-2)" },
  { symbol: "SOL", qty: 88, cost: 128, price: 152, color: "var(--chart-3)" },
  { symbol: "BNB", qty: 12, cost: 520, price: 594, color: "var(--chart-4)" },
];

function Portfolio() {
  const rows = holdings.map((h) => {
    const value = h.qty * h.price;
    const invested = h.qty * h.cost;
    const pnl = value - invested;
    const roi = (pnl / invested) * 100;
    return { ...h, value, invested, pnl, roi };
  });
  const total = rows.reduce((a, r) => a + r.value, 0);
  const invested = rows.reduce((a, r) => a + r.invested, 0);
  const pnl = total - invested;
  const roi = (pnl / invested) * 100;

  const pie = rows.map((r) => ({ name: r.symbol, value: r.value, color: r.color }));

  return (
    <PageShell
      title="Portfolio"
      subtitle="Virtual portfolio with ROI, allocation, and AI prediction impact."
      actions={
        <Button size="sm" className="bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)] text-primary-foreground">
          <Plus className="mr-1 h-3.5 w-3.5" /> Add holding
        </Button>
      }
    >
      <div className="grid gap-4 md:grid-cols-4">
        <Stat label="Total value" value={formatUsd(total)} />
        <Stat label="Invested" value={formatUsd(invested)} />
        <Stat label="P&L" value={formatUsd(pnl)} bull={pnl >= 0} />
        <Stat label="ROI" value={formatPct(roi)} bull={roi >= 0} />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <Card className="glass border-border/60 lg:col-span-2">
          <CardHeader>
            <CardTitle className="font-display text-base">Holdings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {rows.map((r) => (
              <div key={r.symbol} className="flex flex-wrap items-center gap-3 rounded-lg border border-border/50 bg-secondary/20 p-3">
                <div className="flex items-center gap-2 w-24">
                  <span className="h-2 w-2 rounded-full" style={{ background: r.color }} />
                  <span className="font-semibold">{r.symbol}</span>
                </div>
                <div className="text-xs text-muted-foreground w-28">{r.qty} coins</div>
                <div className="font-mono text-sm flex-1 min-w-[100px]">{formatUsd(r.value)}</div>
                <div className={`font-mono text-sm ${r.pnl >= 0 ? "text-[color:var(--bull)]" : "text-[color:var(--bear)]"}`}>
                  {formatPct(r.roi)}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 font-display text-base">
              <Wallet className="h-4 w-4 text-primary" /> Allocation
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-56">
              <ResponsiveContainer>
                <PieChart>
                  <Pie data={pie} innerRadius={50} outerRadius={80} paddingAngle={4} dataKey="value">
                    {pie.map((d, i) => (
                      <Cell key={i} fill={d.color} stroke="transparent" />
                    ))}
                  </Pie>
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="glass mt-6 border-border/60">
        <CardHeader>
          <CardTitle className="font-display text-base">AI Prediction Impact</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            If you executed all current AI signals (BUY BTC/ETH/BNB, HOLD SOL, SELL ADA, HOLD XRP), the
            LSTM model projects a <b className="text-[color:var(--bull)]">+3.4%</b> portfolio move
            over the next 24 hours with 78% confidence.
          </p>
        </CardContent>
      </Card>
    </PageShell>
  );
}

function Stat({ label, value, bull }: { label: string; value: string; bull?: boolean }) {
  return (
    <div className="glass rounded-2xl p-5">
      <div className="text-[10px] uppercase tracking-widest text-muted-foreground">{label}</div>
      <div
        className={`mt-2 font-mono text-2xl font-semibold ${
          bull === undefined ? "" : bull ? "text-[color:var(--bull)]" : "text-[color:var(--bear)]"
        }`}
      >
        {value}
      </div>
    </div>
  );
}
