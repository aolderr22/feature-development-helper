from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import answer_question

app = FastAPI(
    title="Feature Development Helper",
    description="A simple RAG application for software feature development.",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Feature Development Helper API is running."
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    """
    Ask a question about feature development.
    """

    result = answer_question(request.question)

    return result