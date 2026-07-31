import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import { fetchMarkets, COIN_META } from "@/lib/coingecko.functions";
import { useServerFn } from "@tanstack/react-start";
import { formatUsd, formatPct } from "@/lib/format";
import { Star, StarOff, Bell } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

export const Route = createFileRoute("/_authenticated/watchlist")({
  head: () => ({
    meta: [
      { title: "Watchlist — CryptoVision AI" },
      { name: "description", content: "Bookmarked coins with prediction, sentiment, and alerts." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Watchlist,
});

const ids = Object.values(COIN_META).map((c) => c.id);

function Watchlist() {
  const fetch = useServerFn(fetchMarkets);
  const { data = [] } = useQuery({
    queryKey: ["wl", ids.join(",")],
    queryFn: () => fetch({ data: { ids } }),
    refetchInterval: 30_000,
  });
  const [starred, setStarred] = useState<Record<string, boolean>>({ bitcoin: true, ethereum: true, solana: true });

  return (
    <PageShell title="Watchlist" subtitle="Bookmark coins and track prediction / sentiment / alerts.">
      <Card className="glass border-border/60">
        <CardHeader>
          <CardTitle className="font-display text-base">Tracked coins</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {data.map((c, i) => {
            const on = !!starred[c.id];
            const sig = ["BUY", "BUY", "HOLD", "SELL", "BUY", "HOLD"][i % 6];
            return (
              <div
                key={c.id}
                className="flex flex-wrap items-center gap-3 rounded-lg border border-border/50 bg-secondary/20 p-3 text-sm"
              >
                <button
                  onClick={() => setStarred((s) => ({ ...s, [c.id]: !s[c.id] }))}
                  className={`h-8 w-8 rounded-md ${on ? "text-primary" : "text-muted-foreground"} hover:bg-secondary`}
                >
                  {on ? <Star className="mx-auto h-4 w-4 fill-current" /> : <StarOff className="mx-auto h-4 w-4" />}
                </button>
                <img src={c.image} alt="" className="h-7 w-7 rounded-full" />
                <div className="w-20">
                  <div className="font-semibold">{c.symbol.toUpperCase()}</div>
                  <div className="text-[10px] text-muted-foreground">{c.name}</div>
                </div>
                <div className="font-mono flex-1 min-w-[100px]">{formatUsd(c.current_price)}</div>
                <div
                  className={`font-mono w-20 text-right ${
                    c.price_change_percentage_24h >= 0 ? "text-[color:var(--bull)]" : "text-[color:var(--bear)]"
                  }`}
                >
                  {formatPct(c.price_change_percentage_24h)}
                </div>
                <div className="w-16 text-center">
                  <span
                    className={`rounded-md px-2 py-0.5 text-xs ${
                      sig === "BUY"
                        ? "bg-[color:var(--bull)]/15 text-[color:var(--bull)]"
                        : sig === "SELL"
                          ? "bg-[color:var(--bear)]/15 text-[color:var(--bear)]"
                          : "bg-primary/15 text-primary"
                    }`}
                  >
                    {sig}
                  </span>
                </div>
                <Button size="sm" variant="ghost">
                  <Bell className="h-3.5 w-3.5" />
                </Button>
              </div>
            );
          })}
        </CardContent>
      </Card>
    </PageShell>
  );
}
