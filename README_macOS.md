# Invisibility Cloak - Data Privacy & Removal Tool

This is a **local-first** privacy tool: FastAPI backend + React UI with endpoints for importing data brokers, creating PII profiles, running **automated discovery**, and planning removals. It is configured for **Ollama primary** with **OpenAI fallback** for LLM-powered assistance.

## 🚀 Quick Start

### Prerequisites (macOS)
```bash
# Install Xcode command line tools
xcode-select --install

# Install Node.js (for UI)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.zshrc
nvm install --lts
```

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers for web scraping
python -m playwright install

# Set up environment variables (optional)
cp ../.env.example .env
# Edit .env with your OpenAI API key if desired

# Start the API server
uvicorn app.main:app --reload --port 5179
```

### Frontend Setup
```bash
# Navigate to UI directory
cd ui/web

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📊 Data Setup

The project includes 658 real data broker records. To import them:
```

API will be on http://127.0.0.1:5179

## Data

- Brokers CSV lives at `data/brokers_normalized.csv` (copied from your upload). You can re-import via `POST /brokers/import` or replace the file.

## Minimal API usage

- `GET /health` → sanity check
- `POST /brokers/import` (multipart file optional) → imports CSV into `storage/brokers.json`
- `GET /brokers` → list brokers
- `POST /pii-profiles` → create a PII profile (names/emails/phones/addresses)
- `POST /discovery?profile_id=...` → starts a discovery job (skeleton logic)
- `GET /discovery/{job_id}` → progress + items
- `POST /removals` → returns a draft plan for selected brokers

## Wiring Playwright discovery

Open `backend/app/discovery/search_playwright.py` and implement the Playwright logic per your policy. Then, replace `_run_discovery` in `main.py` to call your function for each broker, capture screenshots into a local `evidence/` folder, and populate the `items` list with real results.

## LLM integration

Create `backend/app/llm_engine.py` with Ollama-first + OpenAI-fallback (as shown in canvas). Call it from your Playwright parser to classify matches or extract form selectors. Set `OPENAI_API_KEY` in your shell to enable fallback.

## Security

This starter keeps everything on disk under `storage/`. For production, use SQLCipher + a proper vault (see canvas).

## UI

A React/Electron skeleton can be added next; for now, you can drive the backend with curl or a simple front-end. If you want, I can generate the Electron + React shell wired to these endpoints.


## Enable real Playwright discovery
- Ensure: `python -m playwright install`
- Create a profile via `POST /pii-profiles` (the UI has a 'Quick Create Dummy Profile' button for testing).
- Start discovery from UI (or via API). Screenshots will be stored under `backend/storage/evidence/<job_id>/`.

## Generic Form + Email connectors
- Form connector opens a headful browser window (CAPTCHA-friendly) and attempts to prefill name/email/phone then submit.
- Email connector drafts an opt-out email using **Ollama first** with **OpenAI fallback** into `backend/storage/drafts/*.txt`. You can paste this into your mail client.

### OpenAI fallback
Set `OPENAI_API_KEY` in your shell before running the backend to allow fallback.
