import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";

const InSchema = z.object({
  messages: z
    .array(
      z.object({
        role: z.enum(["system", "user", "assistant"]),
        content: z.string().max(6000),
      }),
    )
    .min(1)
    .max(40),
});

const SYSTEM_PROMPT = `You are CryptoVision AI's on-platform trading assistant.

Rules:
- Speak like a calm, senior quant analyst. Concise, structured, no fluff.
- When asked about a coin, discuss recent price action, momentum (RSI/MACD/EMA), sentiment, and risk. Give a clear directional bias (bullish / bearish / neutral) and a confidence hint.
- Never give financial advice. Always end recommendations with a short risk caveat.
- Prefer bullet points and short paragraphs. Use markdown.
- If asked a general question about an indicator, explain it plainly with a mini example.
- You have no live browsing tools; reason from general market knowledge and the user's message.`;

export const askAssistant = createServerFn({ method: "POST" })
  .inputValidator((d: unknown) => InSchema.parse(d))
  .handler(async ({ data }): Promise<{ text: string }> => {
    const key = process.env.LOVABLE_API_KEY;
    if (!key) throw new Error("Missing LOVABLE_API_KEY");

    // Use AbortController for timeout — prevents hanging requests
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30_000);

    try {
      // Trim message history to last 20 messages to reduce payload size and latency
      const trimmedMessages = data.messages.slice(-20);

      const res = await fetch("https://ai.gateway.lovable.dev/v1/chat/completions", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "Lovable-API-Key": key,
        },
        body: JSON.stringify({
          model: "openai/gpt-5.6-sol",
          reasoning_effort: "none",
          messages: [{ role: "system", content: SYSTEM_PROMPT }, ...trimmedMessages],
        }),
        signal: controller.signal,
      });

      if (res.status === 429)
        throw new Error("Rate limit reached. Please wait a moment and try again.");
      if (res.status === 402)
        throw new Error("AI credits exhausted. Please add credits to continue.");
      if (!res.ok) throw new Error(`AI gateway error ${res.status}`);

      const j = (await res.json()) as {
        choices: { message: { content: string } }[];
      };
      return { text: j.choices?.[0]?.message?.content ?? "" };
    } finally {
      clearTimeout(timeout);
    }
  });
