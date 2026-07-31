import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Newspaper, Sparkles } from "lucide-react";

export const Route = createFileRoute("/_authenticated/news")({
  head: () => ({
    meta: [
      { title: "News — CryptoVision AI" },
      { name: "description", content: "Latest crypto news with AI summaries and sentiment." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: News,
});

const items = [
  {
    title: "Bitcoin ETF inflows hit record high as institutions rotate in",
    src: "CoinDesk",
    time: "2h ago",
    summary: "Spot BTC ETFs pulled a record $1.2B in a single session, driven by institutional rotation from equities.",
    sent: "Positive",
    coins: ["BTC"],
  },
  {
    title: "Solana network processes 5B transactions milestone",
    src: "The Block",
    time: "4h ago",
    summary: "Solana crossed 5B cumulative transactions with sustained sub-second finality — the fastest of any L1.",
    sent: "Positive",
    coins: ["SOL"],
  },
  {
    title: "Regulator delays ETH staking approval, markets react",
    src: "Bloomberg",
    time: "6h ago",
    summary: "SEC pushes ETH staking-ETF decision, market pricing in additional 3-month delay.",
    sent: "Negative",
    coins: ["ETH"],
  },
  {
    title: "BNB Chain launches new developer grant program",
    src: "CryptoSlate",
    time: "9h ago",
    summary: "$100M developer fund targets DeFi and AI-integrated apps on BNB Chain.",
    sent: "Positive",
    coins: ["BNB"],
  },
  {
    title: "XRP lawsuit ruling reopens speculation on retail flows",
    src: "Decrypt",
    time: "12h ago",
    summary: "Latest ruling adds nuance to institutional vs retail sales distinction; market reaction muted.",
    sent: "Neutral",
    coins: ["XRP"],
  },
  {
    title: "Cardano ecosystem TVL declines month-over-month",
    src: "Messari",
    time: "14h ago",
    summary: "ADA DeFi TVL slips 12% MoM as capital rotates into higher-throughput ecosystems.",
    sent: "Negative",
    coins: ["ADA"],
  },
];

const cls = (s: string) =>
  s === "Positive"
    ? "border-[color:var(--bull)]/30 bg-[color:var(--bull)]/15 text-[color:var(--bull)]"
    : s === "Negative"
      ? "border-[color:var(--bear)]/30 bg-[color:var(--bear)]/15 text-[color:var(--bear)]"
      : "border-border text-muted-foreground";

function News() {
  return (
    <PageShell
      title="News feed"
      subtitle="Curated crypto headlines with AI-generated summaries and sentiment tagging."
    >
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((n) => (
          <Card key={n.title} className="glass group border-border/60 transition-all hover:-translate-y-0.5 hover:border-primary/40">
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Newspaper className="h-3.5 w-3.5 text-primary" /> {n.src} · {n.time}
              </div>
              <CardTitle className="mt-2 font-display text-base leading-snug">{n.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="rounded-lg bg-secondary/40 p-3 text-xs text-muted-foreground">
                <Sparkles className="mr-1 inline h-3 w-3 text-primary" />
                {n.summary}
              </p>
              <div className="mt-3 flex flex-wrap items-center gap-2">
                <Badge className={`border ${cls(n.sent)}`}>{n.sent}</Badge>
                {n.coins.map((c) => (
                  <Badge key={c} variant="outline">
                    {c}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </PageShell>
  );
}
