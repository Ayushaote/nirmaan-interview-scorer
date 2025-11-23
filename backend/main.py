from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

from scoring import load_rubric, score_transcript

app = FastAPI(
    title="Nirmaan Interview Transcript Scorer API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # for local/testing; later you can restrict to your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreRequest(BaseModel):
    transcript: str
    rubric_id: Optional[str] = "default"


class ScoreResponse(BaseModel):
    rubric_id: str
    overall_score: float
    criteria_scores: Any  # you can tighten this later if you want


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/score", response_model=ScoreResponse)
def score_endpoint(payload: ScoreRequest):
    # For now we ignore rubric_id and use single JSON file.
    rubric = load_rubric("rubric_config.json")
    result = score_transcript(payload.transcript, rubric)
    return result
 
