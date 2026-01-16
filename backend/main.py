from datetime import datetime
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

allowed_origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://revel8.cloud",
]
extra_origins = os.environ.get("ALLOWED_ORIGINS", "")
for origin in [o.strip() for o in extra_origins.split(",") if o.strip()]:
    allowed_origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


class Submission(BaseModel):
    value: str = ""


@app.post("/submit")
async def submit(submission: Submission):
    timestamp = datetime.utcnow().isoformat() + "Z"
    line = f"{timestamp}\t{submission.value}\n"
    output_path = Path.cwd() / "training_submissions.txt"

    try:
        with output_path.open("a", encoding="utf-8") as handle:
            handle.write(line)
    except OSError as exc:
        raise HTTPException(status_code=500, detail="Failed to save password") from exc

    return {"message": "Password successfully saved"}
