from fastapi import FastAPI
from pydantic import BaseModel

from src.agents.agent import Agent
from src.agents.prompts import SYSTEM_PROMPT


app = FastAPI(title="DevMind API")

agent = Agent(system_prompt=SYSTEM_PROMPT)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    answer = agent.ask(request.question)
    return AnswerResponse(answer=answer)