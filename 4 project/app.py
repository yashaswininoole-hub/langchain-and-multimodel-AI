from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from rag_pipeline import ask

app = FastAPI()

class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_api(request: QueryRequest):
    result = ask(request.question)
    return result


# Serve HTML
@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()