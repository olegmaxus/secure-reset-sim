import os
from datetime import datetime
from pathlib import Path
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

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

s3_bucket = os.environ.get("S3_BUCKET", "")
s3_region = os.environ.get("AWS_REGION", "")
s3_prefix = os.environ.get("S3_PREFIX", "submissions/")
s3_client = None
if s3_bucket and s3_region and os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
    s3_client = boto3.client("s3", region_name=s3_region)
    print(f"S3 storage enabled (bucket: {s3_bucket}, prefix: {s3_prefix})")
else:
    print("S3 storage disabled; using local training_submissions.txt")


class Submission(BaseModel):
    value: str = ""


@app.post("/submit")
async def submit(submission: Submission):
    timestamp = datetime.utcnow().isoformat() + "Z"
    line = f"{timestamp}\t{submission.value}\n"
    output_path = Path.cwd() / "training_submissions.txt"
    object_key = f"{s3_prefix.rstrip('/')}/submission-{timestamp}-{submission.value}.txt"

    try:
        if s3_client:
            s3_client.put_object(Bucket=s3_bucket, Key=object_key, Body=line.encode("utf-8"))
        else:
            with output_path.open("a", encoding="utf-8") as handle:
                handle.write(line)
    except OSError as exc:
        print(f"Storage error (local): {exc}")
        raise HTTPException(status_code=500, detail="Failed to save password") from exc
    except Exception as exc:
        print(f"Storage error (s3): {exc}")
        raise HTTPException(status_code=500, detail="Failed to save password") from exc

    return {"message": "Password successfully saved"}
