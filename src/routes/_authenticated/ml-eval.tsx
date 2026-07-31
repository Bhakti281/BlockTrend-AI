import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  LineChart,
  Line,
  CartesianGrid,
  Tooltip,
  Cell,
  ReferenceLine,
} from "recharts";
import { Info, Brain } from "lucide-react";

export const Route = createFileRoute("/_authenticated/ml-eval")({
  head: () => ({
    meta: [
      { title: "ML Evaluation — CryptoVision AI" },
      { name: "description", content: "Random Forest, XGBoost, LSTM model evaluation with SHAP." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: MLEval,
});

const models = [
  { name: "Random Forest", accuracy: 0.79, precision: 0.77, recall: 0.75, f1: 0.76, rocAuc: 0.83, train: 12.4, infer: 8 },
  { name: "XGBoost", accuracy: 0.83, precision: 0.82, recall: 0.79, f1: 0.80, rocAuc: 0.87, train: 18.1, infer: 12 },
  { name: "LSTM (24h)", accuracy: 0.87, precision: 0.85, recall: 0.84, f1: 0.84, rocAuc: 0.91, train: 92.6, infer: 35 },
];

const featureImportance = [
  { name: "LSTM output", v: 0.24 },
  { name: "MACD", v: 0.16 },
  { name: "RSI", v: 0.14 },
  { name: "News sentiment", v: 0.13 },
  { name: "Volume 24h", v: 0.10 },
  { name: "EMA20/50 cross", v: 0.09 },
  { name: "Bollinger position", v: 0.07 },
  { name: "ATR", v: 0.04 },
  { name: "Volatility 7d", v: 0.03 },
];

const confusion = [
  { row: "Actual BUY", buy: 412, sell: 22, hold: 51 },
  { row: "Actual SELL", buy: 18, sell: 386, hold: 41 },
  { row: "Actual HOLD", buy: 39, sell: 34, hold: 297 },
];

const rocPoints = Array.from({ length: 20 }, (_, i) => {
  const fpr = i / 19;
  return { fpr, lstm: Math.min(1, Math.pow(fpr, 0.35)), xgb: Math.min(1, Math.pow(fpr, 0.45)), rf: Math.min(1, Math.pow(fpr, 0.55)) };
});

const prCurve = Array.from({ length: 20 }, (_, i) => {
  const recall = i / 19;
  return { recall, precision: Math.max(0.55, 0.98 - recall * 0.4) };
});

function MLEval() {
  return (
    <PageShell
      title="ML Evaluation"
      subtitle="Comparison of Random Forest, XGBoost, and LSTM. Wire to your FastAPI /metrics endpoint to replace."
    >
      <div className="mb-4 flex items-start gap-2 rounded-lg border border-primary/30 bg-primary/5 p-3 text-xs text-muted-foreground">
        <Info className="mt-0.5 h-4 w-4 flex-shrink-0 text-primary" />
        Values below are demo evaluation output. Contract: GET /api/ml/metrics returns
        <span className="font-mono"> {`{ models[], featureImportance[], confusion[], roc[], pr[] }`}</span>.
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {models.map((m) => (
          <Card key={m.name} className="glass border-border/60">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2 font-display text-base">
                  <Brain className="h-4 w-4 text-primary" /> {m.name}
                </CardTitle>
                <Badge className="border-primary/30 bg-primary/15 text-primary">Ensemble</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="font-mono text-4xl font-bold">{(m.accuracy * 100).toFixed(0)}%</div>
              <div className="text-xs text-muted-foreground">Accuracy</div>
              <div className="mt-4 grid grid-cols-2 gap-y-2 text-xs">
                {[
                  ["Precision", m.precision],
                  ["Recall", m.recall],
                  ["F1", m.f1],
                  ["ROC-AUC", m.rocAuc],
                ].map(([l, v]) => (
                  <div key={l as string} className="flex justify-between">
                    <span className="text-muted-foreground">{l}</span>
                    <span className="font-mono">{(v as number).toFixed(2)}</span>
                  </div>
                ))}
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Train</span>
                  <span className="font-mono">{m.train}s</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Predict</span>
                  <span className="font-mono">{m.infer}ms</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Feature importance (SHAP)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer>
                <BarChart data={featureImportance} layout="vertical" margin={{ left: 12 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" width={140} tick={{ fill: "var(--muted-foreground)", fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8, fontSize: 12 }} />
                  <Bar dataKey="v" radius={[4, 4, 4, 4]}>
                    {featureImportance.map((_, i) => (
                      <Cell key={i} fill="var(--color-primary)" />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">ROC curves</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer>
                <LineChart data={rocPoints}>
                  <CartesianGrid stroke="var(--border)" strokeOpacity={0.4} />
                  <XAxis dataKey="fpr" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickFormatter={(v) => (v as number).toFixed(1)} />
                  <YAxis tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8, fontSize: 12 }} />
                  <ReferenceLine segment={[{ x: 0, y: 0 }, { x: 1, y: 1 }]} stroke="var(--muted-foreground)" strokeDasharray="3 3" />
                  <Line dataKey="lstm" name="LSTM" stroke="var(--chart-1)" strokeWidth={2} dot={false} />
                  <Line dataKey="xgb" name="XGBoost" stroke="var(--chart-2)" strokeWidth={2} dot={false} />
                  <Line dataKey="rf" name="Random Forest" stroke="var(--chart-3)" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Confusion matrix (LSTM)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-4 gap-2 text-center text-sm">
              <div />
              <div className="text-xs text-muted-foreground">Pred BUY</div>
              <div className="text-xs text-muted-foreground">Pred SELL</div>
              <div className="text-xs text-muted-foreground">Pred HOLD</div>
              {confusion.map((r) => (
                <>
                  <div key={r.row} className="text-xs text-muted-foreground text-right pr-2 py-3">{r.row}</div>
                  <Cellish v={r.buy} row={r.row === "Actual BUY"} />
                  <Cellish v={r.sell} row={r.row === "Actual SELL"} />
                  <Cellish v={r.hold} row={r.row === "Actual HOLD"} />
                </>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Precision-Recall curve</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer>
                <LineChart data={prCurve}>
                  <CartesianGrid stroke="var(--border)" strokeOpacity={0.4} />
                  <XAxis dataKey="recall" tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} tickFormatter={(v) => (v as number).toFixed(1)} />
                  <YAxis domain={[0, 1]} tick={{ fill: "var(--muted-foreground)", fontSize: 10 }} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 8, fontSize: 12 }} />
                  <Line dataKey="precision" stroke="var(--color-primary)" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
}

function Cellish({ v, row }: { v: number; row: boolean }) {
  return (
    <div
      className={`rounded-md py-3 font-mono text-sm ${
        row ? "bg-primary/25 text-foreground" : "bg-secondary/50 text-muted-foreground"
      }`}
    >
      {v}
    </div>
  );
}
