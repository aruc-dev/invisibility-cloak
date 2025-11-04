\
import os, json, uuid, threading, time
from pathlib import Path
from typing import List, Optional, Union
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent.parent / "data"
STORE_DIR = APP_DIR.parent.parent / "storage"
STORE_DIR.mkdir(exist_ok=True)

BROKERS_FILE = DATA_DIR / "brokers_normalized.csv"
BROKERS_JSON = STORE_DIR / "brokers.json"
FINDINGS_JSON = STORE_DIR / "findings.json"
PROFILES_JSON = STORE_DIR / "profiles.json"

app = FastAPI(title="Local Data Removal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default

def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2))

class PIIProfile(BaseModel):
    label: str
    names: Optional[List[str]] = []
    emails: Optional[List[str]] = []
    phones: Optional[List[str]] = []
    addresses: Optional[List[dict]] = []

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/unlock")
def unlock(passphrase: str = Form(...)):
    # Placeholder for local vault unlock; in starter repo we acknowledge and proceed.
    return {"token": str(uuid.uuid4())}

@app.post("/brokers/import")
async def brokers_import(file: Union[UploadFile, None] = File(default=None)):
    import pandas as pd
    if file is not None:
        content = await file.read()
        (DATA_DIR / "brokers_upload.csv").write_bytes(content)
        src = DATA_DIR / "brokers_upload.csv"
    else:
        src = BROKERS_FILE
    if not src.exists():
        return JSONResponse({"error": "No CSV found. Upload a file or place data/brokers_normalized.csv"}, status_code=400)
    try:
        df = pd.read_csv(src)
    except Exception as e:
        return JSONResponse({"error": f"CSV parse failed: {e}"}, status_code=400)
    # Normalize minimal columns
    cols = ['name','domain','search_url','optout_url','country','method','requirements','notes','search_pattern','result_selector','detail_selector']
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    recs = df[cols].fillna("").to_dict(orient="records")
    save_json(BROKERS_JSON, recs)
    return {"imported": len(recs)}

@app.get("/brokers")
def brokers_list():
    return load_json(BROKERS_JSON, [])

@app.post("/pii-profiles")
def create_profile(p: PIIProfile):
    profiles = load_json(PROFILES_JSON, [])
    new = p.dict()
    new["id"] = str(uuid.uuid4())
    profiles.append(new)
    save_json(PROFILES_JSON, profiles)
    return {"id": new["id"]}

@app.get("/pii-profiles")
def list_profiles():
    return load_json(PROFILES_JSON, [])

# --- Discovery jobs ---

@app.post("/discovery")
def start_discovery(profile_id: str, scope: Optional[List[int]] = None):
    jobs = load_json(FINDINGS_JSON, {})
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "progress": 0, "items": []}
    save_json(FINDINGS_JSON, jobs)
    t = threading.Thread(target=_run_discovery, args=(job_id, profile_id, scope))
    t.daemon = True
    t.start()
    return {"job_id": job_id}

@app.get("/discovery/{job_id}")
def discovery_status(job_id: str):
    jobs = load_json(FINDINGS_JSON, {})
    if job_id not in jobs:
        return JSONResponse({"error": "not found"}, status_code=404)
    return jobs[job_id]


def _run_discovery(job_id: str, profile_id: str, scope: Optional[List[int]]):
    from .discovery.search_playwright import search_broker
    evidence_dir = STORE_DIR / "evidence" / job_id
    evidence_dir.mkdir(parents=True, exist_ok=True)

    jobs = load_json(FINDINGS_JSON, {})
    jobs[job_id]["status"] = "running"
    save_json(FINDINGS_JSON, jobs)

    brokers = load_json(BROKERS_JSON, [])
    if scope:
        brokers = [b for idx, b in enumerate(brokers) if idx in scope]

    # Load PII (for now from PROFILES_JSON)
    profiles = load_json(PROFILES_JSON, [])
    profile = next((p for p in profiles if p.get("id")==profile_id), None)
    if not profile:
        profile = {"names":[], "emails":[], "phones":[], "addresses":[]}

    items = []
    total = max(1, len(brokers))
    for i, b in enumerate(brokers):
        try:
            res = search_broker(b, profile, str(evidence_dir))
            items.append({
                "broker_name": b.get("name"),
                "domain": b.get("domain"),
                "broker_id": i,
                "found": bool(res.get("found")),
                "confidence": float(res.get("confidence") or 0.0),
                "evidence_url": res.get("evidence_url"),
                "screenshot_path": res.get("screenshot")
            })
        except Exception as e:
            items.append({
                "broker_name": b.get("name"),
                "domain": b.get("domain"),
                "broker_id": i,
                "found": False,
                "confidence": 0.0,
                "evidence_url": None,
                "error": str(e)
            })
        jobs = load_json(FINDINGS_JSON, {})
        jobs[job_id]["items"] = items
        jobs[job_id]["progress"] = int(((i+1)/total)*100)
        save_json(FINDINGS_JSON, jobs)

    jobs = load_json(FINDINGS_JSON, {})
    jobs[job_id]["status"] = "completed"
    save_json(FINDINGS_JSON, jobs)
