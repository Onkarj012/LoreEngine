"use client";
import { useState } from "react";
import Markdown from "react-markdown";
import { useAsk } from "./use-ask";
import { CitationChip } from "./citation-chip";
import { ErrorNote } from "./error-note";
import { Skeleton } from "./skeleton";

export function AskBox() {
  const [q, setQ] = useState("");
  const { state, ask } = useAsk();
  const loading = state.tag === "loading";

  return (
    <div className="rounded-2xl glass">
      <div className="flex gap-2 p-4">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && ask(q)}
          placeholder="What is a devil fruit?"
          className="flex-1 rounded-xl bg-white/5 px-4 py-3 outline-none
                    border border-white/10 focus:border-white/30 transition-colors"
        />

        <button
          onClick={() => setQ("")}
          className="rounded-xl bg-white/5 backdrop-blur border border-white/10
                     px-4 text-white hover:bg-white/10 hover:border-white/30 transition"
        >
          Clear
        </button>

        <button
          onClick={() => ask(q)}
          disabled={loading}
          className="rounded-xl bg-white px-5 font-semibold text-black
                     hover:bg-neutral-200 disabled:opacity-50 transition"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {state.tag === "loading" && <Skeleton />}
      {state.tag === "error" && <ErrorNote msg={state.message} />}
      {state.tag === "success" && (
        <div
          className="m-4 rounded-xl border border-white/10
        bg-white/5 backdrop-blur-xl p-5"
        >
          <article className="prose prose-invert max-w-none">
            <Markdown>{state.data.answer}</Markdown>
          </article>
          <div className="mt-4 flex flex-wrap gap-2">
            {state.data.citations.map((c, i) => (
              <CitationChip
                key={i}
                index={i + 1}
                source={c.source}
                score={c.score}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
