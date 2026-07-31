import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";
import { useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

export const Route = createFileRoute("/_authenticated/settings")({
  head: () => ({
    meta: [
      { title: "Settings — CryptoVision AI" },
      { name: "description", content: "Manage account, notifications, and preferences." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Settings,
});

function Settings() {
  const [email, setEmail] = useState("");
  const nav = useNavigate();
  const qc = useQueryClient();

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => setEmail(data.user?.email ?? ""));
  }, []);

  async function signOut() {
    await qc.cancelQueries();
    qc.clear();
    await supabase.auth.signOut();
    toast.success("Signed out");
    nav({ to: "/auth", replace: true });
  }

  return (
    <PageShell title="Settings" subtitle="Account, notifications, API keys, and preferences.">
      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Account</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <Label className="text-xs">Email</Label>
              <Input value={email} disabled className="mt-1" />
            </div>
            <Button variant="destructive" onClick={signOut}>
              Sign out
            </Button>
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Notifications</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            {[
              ["AI signal alerts", true],
              ["Price alerts", true],
              ["Daily market briefing", false],
              ["News digest", true],
            ].map(([l, on]) => (
              <div key={l as string} className="flex items-center justify-between">
                <span>{l as string}</span>
                <Switch defaultChecked={on as boolean} />
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">Preferences</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            {[
              ["Default horizon", "24H"],
              ["Base currency", "USD"],
              ["Risk tolerance", "Moderate"],
            ].map(([l, v]) => (
              <div key={l} className="flex items-center justify-between">
                <span className="text-muted-foreground">{l}</span>
                <span className="font-mono">{v}</span>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="glass border-border/60">
          <CardHeader>
            <CardTitle className="font-display text-base">API keys</CardTitle>
          </CardHeader>
          <CardContent className="text-xs text-muted-foreground">
            Bring your own model API keys for private inference. Coming soon.
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
}
