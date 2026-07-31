import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/page-shell";
import { useState, useRef, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import { askAssistant } from "@/lib/assistant.functions";
import { useServerFn } from "@tanstack/react-start";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Bot, Send, Sparkles, User } from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/_authenticated/assistant")({
  head: () => ({
    meta: [
      { title: "AI Assistant — CryptoVision AI" },
      { name: "description", content: "Ask the AI trading assistant anything about the market." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: Assistant,
});

type Msg = { role: "user" | "assistant"; content: string };

const suggestions = [
  "Should I buy BTC?",
  "Explain the RSI indicator",
  "Summarise today's crypto market",
  "Compare BTC vs ETH momentum",
  "Explain MACD in one paragraph",
  "Give me a short-term SOL forecast",
];

function Assistant() {
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "assistant",
      content:
        "Hi — I'm the CryptoVision AI assistant. Ask me about a coin, an indicator, market conditions, or a signal. I'll answer with structured reasoning.",
    },
  ]);
  const [input, setInput] = useState("");
  const scroll = useRef<HTMLDivElement>(null);
  const ask = useServerFn(askAssistant);

  const m = useMutation({
    mutationFn: (history: Msg[]) => ask({ data: { messages: history } }),
    onSuccess: (res) => setMessages((cur) => [...cur, { role: "assistant", content: res.text }]),
    onError: (e: Error) => toast.error(e.message),
  });

  useEffect(() => {
    scroll.current?.scrollTo({ top: scroll.current.scrollHeight, behavior: "smooth" });
  }, [messages, m.isPending]);

  function send(text: string) {
    const t = text.trim();
    if (!t || m.isPending) return;
    const next: Msg[] = [...messages, { role: "user", content: t }];
    setMessages(next);
    setInput("");
    m.mutate(next);
  }

  return (
    <PageShell
      title="AI Trading Assistant"
      subtitle="Live reasoning powered by Lovable AI. No financial advice."
    >
      <div className="grid gap-4 lg:grid-cols-[1fr_260px]">
        <Card className="glass flex h-[70vh] flex-col border-border/60">
          <div ref={scroll} className="flex-1 space-y-4 overflow-y-auto p-6">
            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                <div
                  className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full ${
                    msg.role === "user" ? "bg-secondary" : "bg-primary text-primary-foreground"
                  }`}
                >
                  {msg.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                </div>
                <div
                  className={`max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                    msg.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-secondary/60"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {m.isPending && (
              <div className="flex gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="rounded-2xl bg-secondary/60 px-4 py-3 text-sm">
                  <span className="inline-flex gap-1">
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary [animation-delay:-.3s]" />
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary [animation-delay:-.15s]" />
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary" />
                  </span>
                </div>
              </div>
            )}
          </div>

          <div className="border-t border-border/60 p-4">
            <div className="flex gap-2">
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about coins, indicators, sentiment, or a signal…"
                rows={2}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    send(input);
                  }
                }}
                className="min-h-[52px] resize-none bg-secondary/40"
              />
              <Button
                onClick={() => send(input)}
                disabled={m.isPending || !input.trim()}
                className="bg-gradient-to-r from-primary to-[oklch(0.7_0.19_260)] text-primary-foreground"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </Card>

        <div className="space-y-2">
          <div className="text-xs uppercase tracking-widest text-muted-foreground flex items-center gap-1.5">
            <Sparkles className="h-3 w-3 text-primary" /> Try asking
          </div>
          {suggestions.map((s) => (
            <button
              key={s}
              onClick={() => send(s)}
              disabled={m.isPending}
              className="glass w-full rounded-lg p-3 text-left text-xs transition-all hover:border-primary/40 disabled:opacity-50"
            >
              {s}
            </button>
          ))}
        </div>
      </div>
    </PageShell>
  );
}
