export type Citation = {
  source: string;
  snippet: string;
  score: number;
};

export type AskResponse = {
  answer: string;
  citations: Citation[];
};

export type AskState =
  | { tag: "idle" }
  | { tag: "loading" }
  | { tag: "success"; data: AskResponse }
  | { tag: "error"; message: string };
