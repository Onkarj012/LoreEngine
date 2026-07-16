from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from app.retrieval import Index
from generation import generate
from fastapi.middleware.cors import CORSMiddleware

state: dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    state["index"] = Index()
    yield
    state.clear()

app = FastAPI(title="Lore Engine API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   # the web/ dev origin
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    corpus: str = "demo"

class Citation(BaseModel):
    source: str
    snippet: str
    score: float

class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    hits = state['index'].top_k(req.question, k=2)
    if not hits or hits[0][0] < 0.25:
        return AskResponse(
            answer="I do not have any lore that matches that question.",
            citations=[],
        )

    answer = generate(req.question, hits)
    citations = [
        Citation(source=s.source, snippet = s.text, score=score) 
        for score, s in hits
    ]

    return AskResponse(answer=answer, citations=citations)