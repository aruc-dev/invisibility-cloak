# Invisibility Cloak 🕵️‍♂️

A privacy-focused tool for discovering and removing your personal information from data broker websites.

## 🎯 Features

- **Broker Profile System**: Intelligent grouping of data brokers into targeted profiles for faster, more efficient discovery
- **Quick Essential Scan**: Discover your data in just 15 minutes across 15 high-priority brokers
- **Smart Profile Selection**: 8 specialized broker profiles (People Search, Financial, Healthcare, etc.) for targeted discovery
- **Automated Discovery**: Search 658+ data broker websites with real-time progress tracking and broker-by-broker updates
- **Performance Optimized**: Reduced discovery time from 10+ hours to 15 minutes-3 hours depending on selected profile
- **Real-time Progress**: Live updates showing current broker being scanned and percentage completion
- **Evidence Collection**: Screenshot and document findings for removal requests
- **AI-Powered Removal**: Generate CCPA/CPRA compliant opt-out emails with dual LLM support (Ollama + OpenAI)
- **Comprehensive Removal Workflow**: End-to-end process from discovery to email generation with job tracking
- **Local-First**: All data stays on your machine - no cloud uploads
- **Enhanced UI**: Modern React interface with broker profile selection and real-time updates

## 🏗️ Architecture

- **Backend**: FastAPI (Python) with Playwright for web scraping and comprehensive broker profile API endpoints
- **Frontend**: React + TypeScript with Vite, featuring broker profile selector and real-time progress tracking
- **Broker Profile System**: 8 intelligent broker groupings optimized for different privacy concerns and time constraints
- **Discovery Engine**: Enhanced with broker-specific ordering, timeout optimization, and reliable progress tracking
- **Removal System**: Complete workflow with AI-powered email generation and job monitoring
- **Storage**: Local JSON files (no database required) with organized evidence collection
- **AI Integration**: Dual LLM setup (Ollama primary, OpenAI fallback) with smart error handling

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
- **Discovery not starting**: If discovery appears stuck or doesn't show progress:
  1. Import brokers first: `curl -X POST "http://localhost:5179/brokers/import"`
  2. Verify broker count: `curl -s "http://localhost:5179/brokers" | python3 -c "import sys, json; print(f'Brokers: {len(json.load(sys.stdin))}')"`
  3. Check backend logs for any UnboundLocalError or threading issues
- **Frontend not updating**: Hard refresh (Cmd+Shift+R) or restart frontend if broker names don't appear
- **Backend crashes**: Check for proper virtual environment activation and missing environment variables

## 🎯 Broker Profile System

The discovery process has been revolutionized with intelligent broker profiles that dramatically reduce discovery time while maintaining comprehensive coverage.

### Available Profiles

| Profile | Brokers | Time | Best For |
|---------|---------|------|----------|
| **⚡ Quick Essential Scan** | 15 | ~15 min | First-time users, immediate results |
| **👥 People Search Focus** | 28 | ~30 min | Public directory exposure |
| **💳 Financial & Credit** | 45 | ~45 min | Financial privacy concerns |
| **🏠 Real Estate & Property** | 35 | ~35 min | Property record privacy |
| **🏥 Healthcare & Medical** | 42 | ~40 min | Medical data privacy |
| **💼 Professional & B2B** | 55 | ~55 min | Professional networking data |
| **📊 Tech & Analytics** | 48 | ~50 min | Tech platform data tracking |
| **📢 Marketing & Advertising** | 62 | ~1 hour | Marketing database removal |

### Smart Recommendations

- **Start with Quick Essential Scan** for immediate results and high-impact brokers
- **People Search** covers the most visible public exposure
- **Financial & Healthcare** profiles have the highest privacy impact
- **Run multiple targeted profiles** instead of scanning all 658+ brokers
- **Progressive discovery**: Start small, then expand based on findings

### Performance Improvement

- **Before**: 658+ brokers taking 10+ hours
- **After**: Targeted scans from 15 minutes to 3 hours maximum
- **Optimization**: Brokers ordered by reliability and speed
- **Smart timeouts**: Reduced from 30s to 10s per broker for faster processing

## 👤 Creating Your Profile

Before running discovery, you need to create a PII profile with your personal information. You can now create profiles directly from the web interface or via API:

### Method 1: Create Profile in Web UI (Recommended)

1. Open the web interface at http://localhost:5173
2. **Custom Profile**: Fill out the profile form with your personal information:
   - **Label**: Display name for your profile (e.g., "My Profile", "John Smith")
   - **Names**: Add all variations of your name (full name, nicknames, maiden names)
   - **Emails**: Add all your email addresses (personal, work, old emails)
   - **Phones**: Add your phone numbers
   - **Addresses**: Add current and previous addresses
3. **Quick Demo**: Alternatively, click **"Quick Create Dummy Profile"** for testing
4. Select your created profile from the dropdown to use for discovery

### Method 2: Custom Profile via API

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

### Method 3: Browser Console (Advanced)

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

1. **Create a PII Profile**: Use the web interface profile form at http://localhost:5173 to add your personal information, or follow the [Creating Your Profile](#-creating-your-profile) section for other methods

2. **Select Your Profile**: Choose your created profile from the dropdown in the web interface

3. **Choose Broker Profile**: Select from 8 optimized broker profiles:
   - **⚡ Quick Essential Scan** (recommended for first-time users)
   - **👥 People Search Focus** for public directory exposure
   - **💳 Financial & Credit** for financial data privacy
   - **🏠 Real Estate & Property** for property records
   - And 4 additional specialized profiles

4. **Import Data Brokers**: Load the 658 data brokers from official state registries:
   ```bash
   curl -X POST "http://localhost:5179/brokers/import"
   ```
   This should return: `{"imported": 658}`

5. **Run Discovery**: Click "Run Discovery" to start automated search with:
   - **Real-time progress tracking** with current broker name
   - **Optimized broker ordering** starting with fastest, most reliable sites
   - **Smart timeouts** (10s per broker) for faster completion
   - **Live updates** showing "🔍 X/Y brokers" progress

6. **Review Findings**: Examine results with confidence scores and evidence screenshots
6. **Generate Removal Requests**: Use the Removal tab for AI-powered email generation:
   - Select findings to create removal requests
   - AI generates CCPA/CPRA compliant emails
   - Track removal job progress with real-time updates
7. **Monitor Progress**: Track removal jobs and save email drafts to `backend/storage/drafts/`

### Enhanced Discovery Features

- **Real-time Progress**: Live updates showing current broker being scanned
- **Broker Count Display**: Visual progress indicator (e.g., "🔍 1/658 brokers")
- **State Persistence**: Discovery progress maintained when navigating between tabs
- **Comprehensive Tracking**: Current broker name, total progress, and job status

### Removal Workflow

- **Intelligent Selection**: Choose specific findings for removal requests
- **AI Email Generation**: Automated CCPA/CPRA compliant email creation
- **Job Monitoring**: Real-time status updates for removal requests
- **Draft Management**: Organized storage of generated emails in local directories

### Key Features Tested

- ✅ **Broker Profile System**: 8 intelligent profiles reducing discovery time from 10+ hours to 15 minutes-3 hours
- ✅ **Quick Essential Scan**: 15-minute discovery across 15 high-priority brokers
- ✅ **Smart Broker Ordering**: Optimized sequence starting with fastest, most reliable brokers
- ✅ **Real-time Progress**: Never gets stuck at 0% with reliable broker-by-broker updates
- ✅ **FastAPI Backend**: Enhanced with broker-profiles endpoint and optimized filtering
- ✅ **React Frontend**: Modern UI with always-visible broker profile selector
- ✅ **Performance Optimization**: Reduced timeouts (10s) and improved error recovery
- ✅ **Complete Removal Workflow**: End-to-end process from findings selection to AI email generation
- ✅ **Data Broker Database**: 658 normalized brokers with verified domain matching
- ✅ **Dual AI Integration**: Ollama (local) + OpenAI (fallback) with intelligent error handling
- ✅ **Job Tracking**: Comprehensive monitoring for both discovery and removal operations
- ✅ **Local Storage**: All personal data stays on your machine with organized file structure

## 🤖 AI Features

### LLM Integration
- **Primary**: Ollama (local, private, free) - Default model: `llama3.1:8b`
- **Fallback**: OpenAI (requires API key) - Default model: `gpt-4o-mini`
- **Smart Fallback**: Automatically switches to OpenAI if Ollama fails

### Email Generation
- Generates CCPA/CPRA compliant opt-out emails with legal accuracy
- Personalized content under 160 words for optimal deliverability
- Saves drafts to `backend/storage/drafts/` with organized file structure
- Uses optimized template prompts for consistency and effectiveness
- Intelligent job tracking with real-time status updates
- Comprehensive error handling with detailed logging

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
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── main.py         # Enhanced API with broker profile endpoints
│   │   ├── broker_profiles.py  # 8 intelligent broker profile configurations
│   │   ├── discovery/      # Optimized web scraping with progress tracking
│   │   ├── removal/        # Complete opt-out automation with AI integration
│   │   └── llm_engine.py   # Dual LLM system (Ollama + OpenAI)
│   ├── storage/
│   │   ├── drafts/         # Generated removal emails
│   │   └── evidence/       # Discovery screenshots and data
│   └── requirements.txt
├── ui/web/                 # Modern React frontend
│   ├── src/
│   │   ├── components/     # Enhanced React components
│   │   │   ├── BrokerProfileSelector.tsx  # Broker profile selection UI
│   │   │   ├── DiscoveryPanel.tsx         # Real-time progress tracking
│   │   │   ├── RemovalPanel.tsx           # Complete removal workflow
│   │   │   └── FindingsTable.tsx          # Results display with actions
│   │   └── App.tsx         # Global state management and tab navigation
│   └── package.json
├── data/                   # Normalized data broker information
│   └── brokers_normalized.csv
└── storage/               # Local runtime data (gitignored)
    ├── brokers.json       # Loaded broker database
    ├── findings.json      # Discovery results
    └── profiles.json      # User PII profiles
```

## 🆕 Recent Updates

### v3.0 - Broker Profile System (November 2025)

**🚀 Revolutionary Performance Improvement:**
- **Broker Profile System**: 8 intelligent broker groupings for targeted discovery
- **Massive Time Savings**: Reduced discovery from 10+ hours to 15 minutes-3 hours
- **Quick Essential Scan**: Get results in just 15 minutes with 15 high-priority brokers
- **Smart Profile Selection**: Specialized profiles for different privacy concerns

**⚡ Speed & Reliability Optimizations:**
- **Optimized Broker Ordering**: Start with fastest, most reliable brokers (Spokeo, WhitePages)
- **Smart Timeout Reduction**: Reduced timeouts from 30s to 10s per broker
- **Fixed Progress Tracking**: Real-time updates that never get stuck at 0%
- **Order Preservation**: Broker profiles maintain intended sequence for optimal performance

**🎯 Enhanced User Experience:**
- **Always-Visible Profile Selector**: Choose broker profiles before starting discovery
- **Real-time Broker Names**: See exactly which broker is being scanned
- **Progressive Discovery Workflow**: Start small with Quick Scan, expand as needed
- **Performance Indicators**: Each profile shows estimated time and broker count

**🔧 Technical Improvements:**
- **Fixed Broker Filtering**: Maintains profile-specified order instead of database order
- **Improved Error Recovery**: Better handling of problematic broker sites
- **Enhanced API Endpoints**: New broker-profiles endpoint with comprehensive metadata
- **Reliable Progress Updates**: Progress tracking updates before each broker starts

### v2.0 - Major Enhancement (November 2025)

**🐛 Critical Bug Fixes:**
- Fixed `UnboundLocalError` in discovery engine that prevented discovery from running
- Resolved variable ordering issues in broker loading process
- Enhanced error handling and logging throughout the application

**✨ Discovery Improvements:**
- **Real-time Progress Tracking**: Live broker count display (e.g., "🔍 1/658 brokers")
- **Current Broker Display**: Shows the name of the broker currently being scanned
- **State Persistence**: Discovery progress maintained when switching between tabs
- **Enhanced API**: Added `current_broker`, `total_brokers`, and `current_broker_name` fields

**🎨 UI/UX Enhancements:**
- **Global State Management**: Lifted discovery state to App level for cross-tab persistence
- **Tab Navigation**: Seamless switching between Discovery and Removal panels
- **Profile Creation UI**: Complete profile creation form directly in the web interface
- **Modern Interface**: Enhanced progress displays with real-time updates
- **Improved Feedback**: Better visual indicators and status messages

**🔧 Removal System Overhaul:**
- **Complete Workflow**: End-to-end process from findings selection to email generation
- **AI-Powered Generation**: Dual LLM support with intelligent fallback mechanisms
- **Job Tracking**: Real-time monitoring of removal request progress
- **Enhanced Email Templates**: CCPA/CPRA compliant with optimized prompts

**🏗️ Backend Architecture:**
- **Comprehensive API**: Full CRUD operations for profiles, discoveries, and removals
- **Job Management**: Robust background job processing with status tracking
- **Error Recovery**: Improved resilience and error handling
- **Performance**: Optimized broker loading and processing

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