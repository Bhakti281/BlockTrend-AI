import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Sparkles, ArrowLeft } from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/auth")({
  head: () => ({
    meta: [
      { title: "Sign in — CryptoVision AI" },
      { name: "description", content: "Sign in or create a CryptoVision AI account." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: AuthPage,
});

function AuthPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => {
      if (data.user) navigate({ to: "/dashboard", replace: true });
    });
  }, [navigate]);

  async function signIn(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    setLoading(false);
    if (error) return toast.error(error.message);
    toast.success("Welcome back");
    navigate({ to: "/dashboard", replace: true });
  }

  async function signUp(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: { emailRedirectTo: window.location.origin + "/dashboard" },
    });
    setLoading(false);
    if (error) return toast.error(error.message);
    toast.success("Check your inbox to confirm your account");
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center px-4">
      <div className="pointer-events-none absolute inset-0 grid-bg opacity-30" aria-hidden />
      <div className="pointer-events-none absolute -top-24 left-1/2 h-96 w-[900px] -translate-x-1/2 rounded-full bg-primary/20 blur-3xl" aria-hidden />

      <Link
        to="/"
        className="absolute left-6 top-6 flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-3.5 w-3.5" /> Back
      </Link>

      <div className="relative w-full max-w-md">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary text-primary-foreground glow-cyan">
            <Sparkles className="h-6 w-6" />
          </div>
          <h1 className="mt-4 font-display text-2xl font-bold tracking-tight">
            CryptoVision <span className="text-gradient">AI</span>
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Sign in to access the AI-powered trading terminal.
          </p>
        </div>

        <div className="glass-strong rounded-2xl p-6">
          <Tabs defaultValue="signin">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="signin">Sign in</TabsTrigger>
              <TabsTrigger value="signup">Create account</TabsTrigger>
            </TabsList>

            <TabsContent value="signin" className="mt-6">
              <form onSubmit={signIn} className="space-y-4">
                <Field label="Email" type="email" value={email} onChange={setEmail} />
                <Field label="Password" type="password" value={password} onChange={setPassword} />
                <Button
                  disabled={loading}
                  type="submit"
                  className="w-full bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)] text-primary-foreground"
                >
                  {loading ? "Signing in…" : "Sign in"}
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="signup" className="mt-6">
              <form onSubmit={signUp} className="space-y-4">
                <Field label="Email" type="email" value={email} onChange={setEmail} />
                <Field
                  label="Password"
                  type="password"
                  value={password}
                  onChange={setPassword}
                  hint="At least 6 characters"
                />
                <Button
                  disabled={loading}
                  type="submit"
                  className="w-full bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)] text-primary-foreground"
                >
                  {loading ? "Creating…" : "Create account"}
                </Button>
              </form>
            </TabsContent>
          </Tabs>
        </div>

        <p className="mt-4 text-center text-xs text-muted-foreground">
          By continuing you agree to our terms. This is a research tool, not financial advice.
        </p>
      </div>
    </div>
  );
}

function Field({
  label,
  type,
  value,
  onChange,
  hint,
}: {
  label: string;
  type: string;
  value: string;
  onChange: (v: string) => void;
  hint?: string;
}) {
  return (
    <div className="space-y-1.5">
      <Label className="text-xs">{label}</Label>
      <Input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required
        className="h-10"
      />
      {hint && <p className="text-[11px] text-muted-foreground">{hint}</p>}
    </div>
  );
}
