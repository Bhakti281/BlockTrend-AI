import { createFileRoute, Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Brain,
  LineChart as LineChartIcon,
  Sparkles,
  Bot,
  Gauge,
  ShieldCheck,
  Zap,
  BarChart3,
  ArrowRight,
} from "lucide-react";
import { LineChart, Line, ResponsiveContainer, Area, AreaChart } from "recharts";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "CryptoVision AI — Predict Crypto With Explainable ML + Live Data" },
      {
        name: "description",
        content:
          "The AI-first crypto intelligence platform: ML predictions, LSTM forecasts, SHAP-explained signals, sentiment analysis, live prices, and a Gemini-powered trading assistant.",
      },
      { property: "og:title", content: "CryptoVision AI" },
      {
        property: "og:description",
        content: "AI-powered crypto predictions with explainable ML, live prices, and sentiment.",
      },
    ],
  }),
  component: Landing,
});

const demoSeries = Array.from({ length: 40 }, (_, i) => ({
  x: i,
  y: 40 + 12 * Math.sin(i / 4) + i * 0.4 + Math.random() * 3,
}));

function Landing() {
  return (
    <div className="min-h-screen">
      <Nav />
      <Hero />
      <Marquee />
      <Features />
      <AIDemo />
      <MLBlock />
      <FAQ />
      <Footer />
    </div>
  );
}

function Nav() {
  return (
    <header className="sticky top-0 z-40 border-b border-border/50 bg-background/60 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground glow-cyan">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="font-display text-lg font-bold tracking-tight">
            CryptoVision <span className="text-gradient">AI</span>
          </span>
        </Link>
        <nav className="hidden items-center gap-8 md:flex text-sm text-muted-foreground">
          <a href="#features" className="hover:text-foreground transition-colors">Features</a>
          <a href="#ai" className="hover:text-foreground transition-colors">AI</a>
          <a href="#ml" className="hover:text-foreground transition-colors">ML Models</a>
          <a href="#faq" className="hover:text-foreground transition-colors">FAQ</a>
        </nav>
        <div className="flex items-center gap-2">
          <Button variant="ghost" asChild size="sm">
            <Link to="/auth">Sign in</Link>
          </Button>
          <Button asChild size="sm" className="bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)] text-primary-foreground">
            <Link to="/auth">
              Launch app <ArrowRight className="ml-1 h-3.5 w-3.5" />
            </Link>
          </Button>
        </div>
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 grid-bg opacity-40" aria-hidden />
      <div className="pointer-events-none absolute -top-24 left-1/2 h-96 w-[900px] -translate-x-1/2 rounded-full bg-primary/20 blur-3xl" aria-hidden />
      <div className="relative mx-auto max-w-7xl px-6 pb-24 pt-20 md:pt-28">
        <div className="mx-auto max-w-3xl text-center">
          <Badge variant="outline" className="glass gap-1.5 border-primary/30 px-3 py-1 text-xs">
            <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
            Now with LSTM + Explainable AI
          </Badge>
          <h1 className="mt-6 font-display text-5xl font-bold leading-[1.05] tracking-tight md:text-7xl">
            The AI-first crypto <br />
            <span className="text-gradient">intelligence platform</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
            Predict market moves with Random Forest, XGBoost, and LSTM. Understand every call
            with SHAP explanations. All wrapped in a beautiful trading terminal.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Button asChild size="lg" className="bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)] text-primary-foreground glow-cyan">
              <Link to="/auth">Start predicting free</Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="glass">
              <a href="#ai">See the AI in action</a>
            </Button>
          </div>
          <p className="mt-4 text-xs text-muted-foreground">
            No credit card. Powered by Lovable Cloud + Lovable AI.
          </p>
        </div>

        <div className="mx-auto mt-16 max-w-5xl">
          <div className="glass rounded-2xl p-6 shadow-2xl">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border/60 pb-4">
              <div>
                <div className="text-xs text-muted-foreground">BTC/USD · LSTM 24H prediction</div>
                <div className="mt-1 font-mono text-3xl font-semibold">$67,842.10</div>
              </div>
              <div className="flex items-center gap-2">
                <Badge className="bg-[color:var(--bull)]/20 text-[color:var(--bull)] border-[color:var(--bull)]/30">
                  BUY · 87% confidence
                </Badge>
                <Badge variant="outline">+4.2% expected</Badge>
              </div>
            </div>
            <div className="h-56 w-full pt-4">
              <ResponsiveContainer>
                <AreaChart data={demoSeries}>
                  <defs>
                    <linearGradient id="hg" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="var(--color-primary)" stopOpacity={0.5} />
                      <stop offset="100%" stopColor="var(--color-primary)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <Area
                    type="monotone"
                    dataKey="y"
                    stroke="var(--color-primary)"
                    strokeWidth={2}
                    fill="url(#hg)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-2 grid grid-cols-2 gap-3 border-t border-border/60 pt-4 md:grid-cols-4">
              {[
                ["RSI", "62.4", "Bullish"],
                ["MACD", "+0.34", "Crossover"],
                ["Sentiment", "0.71", "Positive"],
                ["Volume", "+18%", "Rising"],
              ].map(([l, v, t]) => (
                <div key={l}>
                  <div className="text-[10px] uppercase tracking-widest text-muted-foreground">
                    {l}
                  </div>
                  <div className="mt-1 font-mono text-lg">{v}</div>
                  <div className="text-xs text-[color:var(--bull)]">{t}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Marquee() {
  const coins = ["BTC", "ETH", "SOL", "ADA", "BNB", "XRP"];
  return (
    <div className="border-y border-border/50 bg-secondary/30">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-around gap-6 px-6 py-6 text-xs uppercase tracking-widest text-muted-foreground">
        <span>Tracking</span>
        {coins.map((c) => (
          <span key={c} className="font-mono text-sm text-foreground">{c}/USD</span>
        ))}
      </div>
    </div>
  );
}

const features = [
  { icon: Brain, title: "Ensemble ML", desc: "Random Forest + XGBoost + LSTM voting on every prediction." },
  { icon: ShieldCheck, title: "Explainable AI", desc: "SHAP values expose exactly which features drove each call." },
  { icon: Gauge, title: "Sentiment engine", desc: "FinBERT-scored headlines fused into the signal in real time." },
  { icon: LineChartIcon, title: "Live indicators", desc: "RSI, MACD, EMA, Bollinger, VWAP — all streamed and charted." },
  { icon: Bot, title: "AI assistant", desc: "Ask why the model bought BTC. Get a plain-language answer." },
  { icon: Zap, title: "Multi-coin", desc: "Compare BTC, ETH, SOL, ADA, BNB, XRP side-by-side." },
];

function Features() {
  return (
    <section id="features" className="relative py-24">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mx-auto max-w-2xl text-center">
          <div className="text-xs uppercase tracking-widest text-primary">Platform</div>
          <h2 className="mt-3 font-display text-3xl font-bold md:text-5xl">
            Every tool a quant desk uses — <span className="text-gradient">on one screen</span>.
          </h2>
        </div>
        <div className="mt-14 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => (
            <div
              key={f.title}
              className="group glass rounded-2xl p-6 transition-all hover:-translate-y-0.5 hover:shadow-2xl hover:border-primary/40"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/15 text-primary">
                <f.icon className="h-5 w-5" />
              </div>
              <h3 className="mt-4 font-display text-lg font-semibold">{f.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function AIDemo() {
  return (
    <section id="ai" className="relative py-24">
      <div className="mx-auto grid max-w-7xl gap-10 px-6 lg:grid-cols-2 lg:items-center">
        <div>
          <div className="text-xs uppercase tracking-widest text-primary">AI Assistant</div>
          <h2 className="mt-3 font-display text-3xl font-bold md:text-5xl">
            Ask your portfolio anything.
          </h2>
          <p className="mt-4 text-muted-foreground">
            The CryptoVision assistant reasons over live prices, indicators, sentiment, and
            model output — and answers in plain English. No black boxes.
          </p>
          <ul className="mt-6 space-y-3 text-sm">
            {[
              "Should I buy BTC right now?",
              "Explain today's MACD crossover on SOL",
              "Summarise crypto news for the past 24h",
              "Compare risk between ETH and ADA",
            ].map((q) => (
              <li key={q} className="glass rounded-lg px-3 py-2 font-mono text-xs">
                › {q}
              </li>
            ))}
          </ul>
        </div>
        <div className="glass rounded-2xl p-6">
          <div className="mb-4 flex items-center gap-2 text-xs text-muted-foreground">
            <Bot className="h-4 w-4 text-primary" /> CryptoVision AI
          </div>
          <div className="space-y-3 text-sm leading-relaxed">
            <p className="rounded-lg bg-secondary/60 p-3 font-mono text-xs">
              User: Why did the model just say BUY on BTC?
            </p>
            <div className="rounded-lg border border-primary/30 bg-primary/5 p-4">
              BTC is showing <b>bullish momentum</b> — MACD just completed a positive
              crossover, RSI is climbing through 60, and 24h volume is up 18%. Sentiment on
              major headlines is <b>+0.71</b>. LSTM predicts <b>+4.2% in 24h</b> with 87%
              confidence. Position sizing suggestion: standard. Risk: still watch the
              $65.2k support.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function MLBlock() {
  const perf = [
    { name: "Random Forest", acc: 0.79, roc: 0.83 },
    { name: "XGBoost", acc: 0.83, roc: 0.87 },
    { name: "LSTM (24h)", acc: 0.87, roc: 0.91 },
  ];
  return (
    <section id="ml" className="relative border-y border-border/50 bg-secondary/20 py-24">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mx-auto max-w-2xl text-center">
          <div className="text-xs uppercase tracking-widest text-primary">ML Engine</div>
          <h2 className="mt-3 font-display text-3xl font-bold md:text-5xl">
            Three models. One vote. <span className="text-gradient">Every signal explained.</span>
          </h2>
        </div>
        <div className="mt-14 grid gap-4 md:grid-cols-3">
          {perf.map((p) => (
            <div key={p.name} className="glass rounded-2xl p-6">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <BarChart3 className="h-4 w-4 text-primary" /> {p.name}
              </div>
              <div className="mt-4 font-mono text-4xl font-bold">
                {(p.acc * 100).toFixed(0)}<span className="text-lg text-muted-foreground">%</span>
              </div>
              <div className="text-xs text-muted-foreground">Accuracy</div>
              <div className="mt-4 h-24 w-full">
                <ResponsiveContainer>
                  <LineChart data={demoSeries}>
                    <Line
                      dataKey="y"
                      stroke="var(--color-primary)"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span className="text-muted-foreground">ROC-AUC</span>
                <span className="font-mono text-foreground">{p.roc.toFixed(2)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

const faqs = [
  {
    q: "Is CryptoVision AI a live trading platform?",
    a: "No. CryptoVision AI is an analytics & prediction platform — no order execution. Signals are informational.",
  },
  {
    q: "How accurate are the predictions?",
    a: "Historical validation ranges from ~79% (Random Forest) to ~87% (LSTM 24h) accuracy on major pairs. Real performance varies with market regime.",
  },
  {
    q: "Where does live data come from?",
    a: "Live spot data is pulled from CoinGecko. News sentiment is scored with FinBERT. AI assistant is powered by Lovable AI.",
  },
  {
    q: "Do you provide financial advice?",
    a: "Never. CryptoVision AI is a research tool. Always do your own due diligence.",
  },
];

function FAQ() {
  return (
    <section id="faq" className="py-24">
      <div className="mx-auto max-w-3xl px-6">
        <div className="text-center">
          <div className="text-xs uppercase tracking-widest text-primary">FAQ</div>
          <h2 className="mt-3 font-display text-3xl font-bold md:text-4xl">
            Questions, answered.
          </h2>
        </div>
        <div className="mt-10 space-y-3">
          {faqs.map((f) => (
            <details key={f.q} className="glass group rounded-xl p-5 open:border-primary/40">
              <summary className="flex cursor-pointer items-center justify-between font-medium">
                {f.q}
                <span className="text-primary transition-transform group-open:rotate-45">+</span>
              </summary>
              <p className="mt-3 text-sm text-muted-foreground">{f.a}</p>
            </details>
          ))}
        </div>
        <div className="mt-14 text-center">
          <Button asChild size="lg" className="bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)] text-primary-foreground glow-cyan">
            <Link to="/auth">Get started free</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="border-t border-border/50 py-10">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-6 text-xs text-muted-foreground">
        <div className="flex items-center gap-2">
          <div className="flex h-6 w-6 items-center justify-center rounded bg-primary text-primary-foreground">
            <Sparkles className="h-3 w-3" />
          </div>
          © {new Date().getFullYear()} CryptoVision AI · Built for research, not advice.
        </div>
        <div className="flex items-center gap-6">
          <a href="#features" className="hover:text-foreground">Features</a>
          <a href="#faq" className="hover:text-foreground">FAQ</a>
          <Link to="/auth" className="hover:text-foreground">Sign in</Link>
        </div>
      </div>
    </footer>
  );
}
