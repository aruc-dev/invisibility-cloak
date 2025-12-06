\
import os, json, uuid, threading, time
from pathlib import Path
from typing import List, Optional, Union
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import broker profiles
from .broker_profiles import (
    get_broker_profiles, 
    get_profile_by_name, 
    filter_brokers_by_profile, 
    get_profile_recommendations
)

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent.parent / "data"
STORE_DIR = APP_DIR.parent.parent / "storage"
STORE_DIR.mkdir(exist_ok=True)

BROKERS_FILE = DATA_DIR / "brokers_normalized.csv"
BROKERS_JSON = STORE_DIR / "brokers.json"
FINDINGS_JSON = STORE_DIR / "findings.json"
PROFILES_JSON = STORE_DIR / "profiles.json"
REMOVALS_JSON = STORE_DIR / "removals.json"

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

# --- Removal jobs ---

@app.post("/removals")
def start_removal(profile_id: str, brokers: List[int]):
    """Start a removal job for selected brokers"""
    removals = load_json(REMOVALS_JSON, {})
    job_id = str(uuid.uuid4())
    
    # Initialize removal job
    removals[job_id] = {
        "status": "queued",
        "profile_id": profile_id,
        "broker_ids": brokers,
        "progress": 0,
        "items": [],
        "created_at": str(time.time())
    }
    save_json(REMOVALS_JSON, removals)
    
    # Start removal process in background
    t = threading.Thread(target=_run_removal, args=(job_id, profile_id, brokers))
    t.daemon = True
    t.start()
    
    return {"job_id": job_id, "status": "queued", "broker_count": len(brokers)}

@app.get("/removals/{job_id}")
def removal_status(job_id: str):
    """Get status of a removal job"""
    removals = load_json(REMOVALS_JSON, {})
    if job_id not in removals:
        return JSONResponse({"error": "Removal job not found"}, status_code=404)
    return removals[job_id]

@app.get("/removals")
def list_removals():
    """List all removal jobs"""
    removals = load_json(REMOVALS_JSON, {})
    return {job_id: job for job_id, job in removals.items()}

@app.delete("/removals/{job_id}")
def cancel_removal(job_id: str):
    """Cancel a removal job"""
    removals = load_json(REMOVALS_JSON, {})
    if job_id not in removals:
        return JSONResponse({"error": "Removal job not found"}, status_code=404)
    
    if removals[job_id]["status"] in ["queued", "running"]:
        removals[job_id]["status"] = "cancelled"
        save_json(REMOVALS_JSON, removals)
        return {"status": "cancelled"}
    else:
        return JSONResponse({"error": "Cannot cancel completed job"}, status_code=400)

@app.get("/broker-profiles")
def get_profiles():
    """Get all available broker profiles for discovery"""
    return get_broker_profiles()

@app.post("/discovery")
def start_discovery(
    profile_id: str, 
    scope: Optional[List[int]] = None,
    broker_profile: str = "all_brokers"
):
    """Start discovery with optional broker profile filtering"""
    jobs = load_json(FINDINGS_JSON, {})
    job_id = str(uuid.uuid4())
    
    # Get profile info for metadata
    profile_info = None
    if broker_profile != "all_brokers":
        try:
            profile_info = get_profile_by_name(broker_profile)
        except ValueError:
            profile_info = None
    
    jobs[job_id] = {
        "status": "queued", 
        "progress": 0, 
        "items": [],
        "current_broker": 0,
        "total_brokers": 0,
        "current_broker_name": "",
        "broker_profile": broker_profile,
        "profile_info": profile_info
    }
    save_json(FINDINGS_JSON, jobs)
    t = threading.Thread(target=_run_discovery, args=(job_id, profile_id, scope, broker_profile))
    t.daemon = True
    t.start()
    return {"job_id": job_id}

@app.get("/discovery/{job_id}")
def discovery_status(job_id: str):
    jobs = load_json(FINDINGS_JSON, {})
    if job_id not in jobs:
        return JSONResponse({"error": "not found"}, status_code=404)
    return jobs[job_id]

@app.post("/discovery/{job_id}/mark-false-positive")
def mark_false_positive(job_id: str, request: dict):
    """Mark a broker result as a false positive"""
    print(f"Marking broker {request['broker_id']} as false positive for job {job_id}")
    
    findings_file = STORE_DIR / "findings.json"
    if findings_file.exists():
        findings = json.loads(findings_file.read_text())
        
        # Find and update the specific result
        for result in findings.get(job_id, []):
            if result.get('broker_id') == request['broker_id']:
                result['marked_false_positive'] = True
                result['confidence'] = 0.0  # Reset confidence
                break
        
        findings_file.write_text(json.dumps(findings, indent=2))
        print(f"Successfully marked broker {request['broker_id']} as false positive")
        return {"success": True}
    
    return {"success": False, "error": "Findings not found"}

@app.post("/discovery/{job_id}/verify-positive")
def verify_positive(job_id: str, request: dict):
    """Mark a discovery result as verified true positive"""
    broker_id = request.get('broker_id')
    if broker_id is None:
         return JSONResponse({"error": "broker_id required"}, status_code=400)

    print(f"Verifying broker {broker_id} as true positive for job {job_id}")

    jobs = load_json(FINDINGS_JSON, {})
    if job_id not in jobs:
        return JSONResponse({"error": "job not found"}, status_code=404)
    
    job = jobs[job_id]
    items = job.get("items", [])
    
    found = False
    # Find and update the item
    for item in items:
        if item.get("broker_id") == broker_id:
            item["verified_positive"] = True
            item["confidence"] = min(1.0, item.get("confidence", 0.5) + 0.2)  # Boost confidence
            item["notes"] = (item.get("notes", "") + " [VERIFIED_BY_USER]").strip()
            found = True
            break

    if found:
        # Save updated job
        jobs[job_id] = job
        save_json(FINDINGS_JSON, jobs)
        print(f"Successfully verified broker {broker_id} as true positive")
        return {"success": True, "message": f"Marked broker {broker_id} as verified positive"}
    
    return {"success": False, "error": "Broker result not found"}


def _run_discovery(job_id: str, profile_id: str, scope: Optional[List[int]], broker_profile: str = "all_brokers"):
    from .discovery.search_playwright import search_broker
    evidence_dir = STORE_DIR / "evidence" / job_id
    evidence_dir.mkdir(parents=True, exist_ok=True)

    # Load brokers first
    brokers = load_json(BROKERS_JSON, [])
    
    # Apply broker profile filtering
    if broker_profile != "all_brokers":
        brokers = filter_brokers_by_profile(brokers, broker_profile)
    
    # Apply scope filtering if provided
    if scope:
        brokers = [b for idx, b in enumerate(brokers) if idx in scope]

    jobs = load_json(FINDINGS_JSON, {})
    jobs[job_id]["status"] = "running"
    jobs[job_id]["total_brokers"] = len(brokers)
    save_json(FINDINGS_JSON, jobs)

    # Load PII (for now from PROFILES_JSON)
    profiles = load_json(PROFILES_JSON, [])
    profile = next((p for p in profiles if p.get("id")==profile_id), None)
    if not profile:
        profile = {"names":[], "emails":[], "phones":[], "addresses":[]}

    items = []
    total = max(1, len(brokers))
    for i, b in enumerate(brokers):
        # Update progress BEFORE starting broker search
        jobs = load_json(FINDINGS_JSON, {})
        jobs[job_id]["current_broker"] = i + 1
        jobs[job_id]["total_brokers"] = total
        jobs[job_id]["current_broker_name"] = b.get("name", "Unknown")
        jobs[job_id]["progress"] = int((i/total)*100)  # Progress based on started brokers
        save_json(FINDINGS_JSON, jobs)
        
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
            print(f"❌ Error searching {b.get('name', 'Unknown')}: {str(e)}")
            items.append({
                "broker_name": b.get("name"),
                "domain": b.get("domain"),
                "broker_id": i,
                "found": False,
                "confidence": 0.0,
                "evidence_url": None,
                "error": str(e)
            })
        
        # Update final results after broker completion
        jobs = load_json(FINDINGS_JSON, {})
        jobs[job_id]["items"] = items
        jobs[job_id]["progress"] = int(((i+1)/total)*100)  # Progress based on completed brokers
        save_json(FINDINGS_JSON, jobs)

    jobs = load_json(FINDINGS_JSON, {})
    jobs[job_id]["status"] = "completed"
    save_json(FINDINGS_JSON, jobs)


def _run_removal(job_id: str, profile_id: str, broker_ids: List[int]):
    """Execute removal process for selected brokers"""
    removals = load_json(REMOVALS_JSON, {})
    removals[job_id]["status"] = "running"
    save_json(REMOVALS_JSON, removals)

    # Load broker and profile data
    brokers = load_json(BROKERS_JSON, [])
    selected_brokers = [brokers[i] for i in broker_ids if i < len(brokers)]
    
    profiles = load_json(PROFILES_JSON, [])
    profile = next((p for p in profiles if p.get("id") == profile_id), None)
    if not profile:
        removals[job_id]["status"] = "error"
        removals[job_id]["error"] = "Profile not found"
        save_json(REMOVALS_JSON, removals)
        return

    items = []
    total = max(1, len(selected_brokers))
    
    for i, broker in enumerate(selected_brokers):
        try:
            # Create drafts directory
            drafts_dir = STORE_DIR / "drafts"
            drafts_dir.mkdir(exist_ok=True)
            
            # Determine removal method based on broker data
            method = broker.get("method", "email").lower()
            result = {"broker_name": broker.get("name"), "broker_id": broker_ids[i], "method": method}
            
            if method == "email" or not broker.get("optout_url"):
                # Use AI-powered email generation
                from .removal.connectors.email_generic import EmailGeneric
                connector = EmailGeneric(broker, profile)
                removal_result = connector.submit()
                result.update(removal_result)
            
            elif method == "form" and broker.get("optout_url"):
                # Use form automation
                from .removal.connectors.form_generic import GenericForm
                connector = GenericForm(broker, profile)
                removal_result = connector.submit()
                result.update(removal_result)
            
            else:
                # Manual process required
                result.update({
                    "status": "manual_required",
                    "transcript": f"Manual removal required for {broker.get('name')}. Check broker requirements.",
                    "evidence_path": None
                })
            
            items.append(result)
            print(f"Processed removal for {broker.get('name')}: {result.get('status')}")
            
        except Exception as e:
            print(f"Error processing removal for {broker.get('name')}: {e}")
            items.append({
                "broker_name": broker.get("name"),
                "broker_id": broker_ids[i],
                "method": "error",
                "status": "error",
                "transcript": f"Error: {str(e)}",
                "evidence_path": None
            })
        
        # Update progress
        removals = load_json(REMOVALS_JSON, {})
        removals[job_id]["items"] = items
        removals[job_id]["progress"] = int(((i + 1) / total) * 100)
        save_json(REMOVALS_JSON, removals)
    
    # Mark as completed
    removals = load_json(REMOVALS_JSON, {})
    removals[job_id]["status"] = "completed"
    save_json(REMOVALS_JSON, removals)
    print(f"Removal job {job_id} completed with {len(items)} items")
