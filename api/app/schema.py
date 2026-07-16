from pydantic import BaseModel

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