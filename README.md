# Invisibility Cloak 🕵️‍♂️

A privacy-focused tool for discovering and removing your personal information from data broker websites.

## 🎯 Features

- **Automated Discovery**: Search 658+ data broker websites for your personal information
- **Evidence Collection**: Screenshot and document findings for removal requests
- **Opt-out Assistance**: Generate removal requests and track progress
- **Local-First**: All data stays on your machine - no cloud uploads
- **LLM-Powered**: Uses AI to help classify findings and generate removal content

## 🏗️ Architecture

- **Backend**: FastAPI (Python) with Playwright for web scraping
- **Frontend**: React + TypeScript with Vite
- **Storage**: Local JSON files (no database required)
- **AI**: Ollama primary, OpenAI fallback for LLM features

## 🚀 Quick Start

### Prerequisites

- macOS (other platforms may work but untested)
- Python 3.9+
- Node.js 18+ (preferably managed with NVM)
- Xcode command line tools

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aruc-dev/invisibility-cloak.git
   cd invisibility-cloak
   ```

2. **Set up Python environment**
   
   The project will automatically configure a Python virtual environment when you start working with it. VS Code will detect and set this up for you.

3. **Install backend dependencies**
   ```bash
   # Dependencies will be installed automatically:
   # fastapi, uvicorn, playwright, pandas, requests, python-multipart
   ```

4. **Install frontend dependencies**
   ```bash
   cd ui/web
   npm install
   ```

5. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key if you want AI-powered email generation
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   # From the project root directory
   .venv/bin/python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 5179
   ```

2. **Start the frontend server** (in a new terminal)
   ```bash
   cd ui/web
   npm run dev
   ```

3. **Access the application**
   - **Frontend UI**: http://localhost:5173
   - **Backend API docs**: http://localhost:5179/docs
   - **Backend API**: http://localhost:5179

### Troubleshooting

- **Port conflicts**: If port 5179 or 5173 are in use, kill processes with `lsof -ti:5179 | xargs kill -9`
- **Missing dependencies**: The setup process will install required Python packages automatically
- **Node.js issues**: Ensure you have Node.js v18+ installed (check with `node --version`)
- **Discovery stuck at 0%**: If discovery doesn't start, you need to import brokers first:
  ```bash
  curl -X POST "http://localhost:5179/brokers/import"
  ```
  Verify with: `curl -s "http://localhost:5179/brokers" | python3 -c "import sys, json; print(f'Brokers: {len(json.load(sys.stdin))}')"`

## � Creating Your Profile

Before running discovery, you need to create a PII profile with your personal information. Here are three ways to do it:

### Method 1: Quick Demo Profile (Easiest)

1. Open the web interface at http://localhost:5173
2. Click **"Quick Create Dummy Profile"** button
3. Select the created profile from the dropdown
4. This creates a sample profile you can use for testing

### Method 2: Custom Profile via API (Recommended)

Create a profile with your actual information using the backend API:

```bash
curl -X POST "http://localhost:5179/pii-profiles" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "My Profile",
    "names": ["Your Full Name", "Nickname", "Maiden Name"],
    "emails": ["personal@email.com", "work@company.com"],
    "phones": ["(555) 123-4567"],
    "addresses": [
      {"street": "123 Main St", "city": "Your City", "state": "Your State", "zip": "12345"}
    ]
  }'
```

### Method 3: Browser Console

1. Open http://localhost:5173 in your browser
2. Open Developer Tools (F12) and go to Console
3. Run this JavaScript:

```javascript
fetch("http://localhost:5179/pii-profiles", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    label: "My Profile",
    names: ["Your Name"],
    emails: ["your@email.com"],
    phones: ["(555) 123-4567"],
    addresses: [{city: "Your City", state: "Your State"}]
  })
}).then(() => window.location.reload());
```

### Profile Fields

- **`label`**: Display name for your profile
- **`names`**: Array of all your names (full name, nicknames, maiden names)
- **`emails`**: Array of email addresses (personal, work, old emails)
- **`phones`**: Array of phone numbers
- **`addresses`**: Array of addresses with street, city, state, zip

### Example Profile Creation

```bash
curl -X POST "http://localhost:5179/pii-profiles" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "arun",
    "names": ["Arun Babu Chandrababu", "Arun Chandrababu", "Arun Babu C"],
    "emails": ["arunbabuc@gmail.com", "arunbabuc.dev@gmail.com"],
    "phones": ["669-544-9104"],
    "addresses": [{"city": "Brentwood", "state": "California"}]
  }'
```

## 📋 Usage

1. **Create a PII Profile**: Follow the [Creating Your Profile](#-creating-your-profile) section above to add your personal information
2. **Select Your Profile**: Choose your profile from the dropdown in the web interface
3. **Import Data Brokers**: Load the 658 data brokers from official state registries:
   ```bash
   curl -X POST "http://localhost:5179/brokers/import"
   ```
   This should return: `{"imported": 658}`
4. **Run Discovery**: Click "Run Discovery" to start automated Playwright-based search across data broker websites
5. **Review Findings**: See which brokers have your data with confidence scores and evidence screenshots
6. **Generate Removal Requests**: AI-powered email generation using Ollama (local) or OpenAI (fallback)
7. **Track Progress**: Monitor your removal requests and save drafts to `backend/storage/drafts/`

### Key Features Tested

- ✅ **FastAPI Backend**: Runs on port 5179 with auto-reload
- ✅ **React Frontend**: Vite dev server on port 5173  
- ✅ **Data Broker Database**: 658 normalized brokers with search URLs and opt-out information
- ✅ **AI Integration**: Dual LLM setup (Ollama primary, OpenAI fallback) for email generation
- ✅ **Discovery System**: Automated web scraping with Playwright
- ✅ **Local Storage**: All personal data stays on your machine

## 🤖 AI Features

### LLM Integration
- **Primary**: Ollama (local, private, free) - Default model: `llama3.1:8b`
- **Fallback**: OpenAI (requires API key) - Default model: `gpt-4o-mini`
- **Smart Fallback**: Automatically switches to OpenAI if Ollama fails

### Email Generation
- Generates CCPA/CPRA compliant opt-out emails
- Personalized content under 160 words
- Saves drafts to `backend/storage/drafts/`
- Uses template prompts for consistency

### Environment Configuration
```bash
# Optional - in your .env file
OPENAI_API_KEY=your_openai_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OPENAI_MODEL=gpt-4o-mini
```

## 🛡️ Privacy & Security

- **Local Storage**: All personal data stays on your machine
- **No Tracking**: No analytics or data collection
- **Open Source**: Fully auditable code
- **Secure**: Environment variables for API keys

## 📁 Project Structure

```
invisibility_cloak/
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── main.py      # API endpoints
│   │   ├── discovery/   # Web scraping logic
│   │   ├── removal/     # Opt-out automation
│   │   └── llm_engine.py # AI integration
│   └── requirements.txt
├── ui/web/              # React frontend
│   ├── src/
│   │   └── components/  # React components
│   └── package.json
├── data/                # Data broker information
└── storage/            # Local data (gitignored)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -am 'Add feature'`
6. Push: `git push origin feature-name`
7. Submit a pull request

## ⚖️ Legal & Ethics

This tool is designed to help individuals exercise their privacy rights. Please:

- Use responsibly and respect websites' terms of service
- Add delays between requests to avoid overwhelming servers
- Only use for legitimate privacy protection purposes
- Follow applicable laws and regulations

## 📄 License

[Add your chosen license here]

## 🆘 Support

- [GitHub Issues](https://github.com/aruc-dev/invisibility-cloak/issues)
- [Documentation](./README_macOS.md)
- [API Documentation](http://localhost:5179/docs) (when running)

## 🙏 Acknowledgments

- Data broker information compiled from state privacy registries
- Built with [Playwright](https://playwright.dev/) for web automation
- UI powered by [React](https://reactjs.org/) and [Vite](https://vitejs.dev/)

---

**Disclaimer**: This tool is for educational and privacy protection purposes. Users are responsible for complying with applicable laws and website terms of service.