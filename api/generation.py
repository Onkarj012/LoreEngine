import os
from openai import OpenAI
from app.retrieval import Index, Snippet
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL")

SYSTEM = (
    "You are the Lore Engine, a careful One Piece lore assistant. "
    "Answer using ONLY the numbered context passages. "
    "Format the answer in clean Markdown: a short bold lead line, "
    "then concise paragraphs or bullet points where useful. "
    "Cite passages inline with bracketed numbers like [1]. "
    "If the context lacks the answer, reply exactly: "
    "'I do not have any lore that matches that question.'"
)

_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate(question: str, hits: list[tuple[float, Snippet]]) -> str:
    context = " ".join(
        f"[{i + 1}] ({s.source}) {s.text}"
        for i, (_score, s) in enumerate(hits)
    )

    completion = _client.chat.completions.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
             {"role": "system", "content": SYSTEM},
            {"role": "user",
             "content": f"Question: {question}\n\nContext:\n{context}"},
        ],
    )

    return completion.choices[0].message.content
    