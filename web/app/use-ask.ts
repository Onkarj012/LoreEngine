import { useState } from "react";
import type { AskResponse, AskState } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function useAsk() {
  const [state, setState] = useState<AskState>({ tag: "idle" });

  async function ask(question: string) {
    if (!question.trim()) return;

    setState({ tag: "loading" });

    try {
      const res = await fetch(`${API}/ask`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) throw new Error("Failed to ask");

      const data: AskResponse = await res.json();
      setState({ tag: "success", data });
    } catch (e) {
      const message = e instanceof Error ? e.message : "Request failed";
      setState({ tag: "error", message });
    }
  }

  return { state, ask };
}
