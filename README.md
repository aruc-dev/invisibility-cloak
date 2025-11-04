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
- Node.js 18+
- Xcode command line tools

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/invisibility_cloak.git
   cd invisibility_cloak
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python -m playwright install
   ```

3. **Set up the frontend**
   ```bash
   cd ../ui/web
   npm install
   ```

4. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key if you want LLM features
   ```

### Running the Application

1. **Start the backend**
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn app.main:app --reload --port 5179
   ```

2. **Start the frontend** (in a new terminal)
   ```bash
   cd ui/web
   npm run dev
   ```

3. **Open your browser**
   - Frontend: http://localhost:5173
   - API docs: http://127.0.0.1:5179/docs

## 📋 Usage

1. **Create a PII Profile**: Add your personal information (name, email, phone, address)
2. **Run Discovery**: Search data brokers for your information
3. **Review Findings**: See which brokers have your data with confidence scores
4. **Plan Removals**: Generate opt-out requests for selected brokers
5. **Track Progress**: Monitor your removal requests

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

- [GitHub Issues](https://github.com/yourusername/invisibility_cloak/issues)
- [Documentation](./README_macOS.md)

## 🙏 Acknowledgments

- Data broker information compiled from state privacy registries
- Built with [Playwright](https://playwright.dev/) for web automation
- UI powered by [React](https://reactjs.org/) and [Vite](https://vitejs.dev/)

---

**Disclaimer**: This tool is for educational and privacy protection purposes. Users are responsible for complying with applicable laws and website terms of service.