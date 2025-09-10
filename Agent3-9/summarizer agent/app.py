from fastapi import FastAPI
from pydantic import BaseModel
from crew.flow import run_pipeline

app = FastAPI()

class Query(BaseModel):
    prompt: str

@app.post("/run")
def run(q: Query):
    return run_pipeline(q.prompt)
