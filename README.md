# 🌐 BrightData MCP × Google ADK Platform

Professional Web Scraping & Data Extraction Platform powered by BrightData's Model Context Protocol (MCP) and Google's Agent Development Kit (ADK).

**Repository**: https://github.com/arjunprabhulal/brightdata-mcp-adk-hackathon

## 🚀 Features

- **50+ Specialized Tools** - E-commerce, social media, news, business data
- **AI-Powered Agent** - Google Gemini 2.0 Flash with intelligent tool selection
- **Real-time Scraping** - BrightData proxy network with anti-bot protection
- **Professional UI** - React-based interface with responsive design
- **Production Ready** - Docker deployment with health checks and monitoring

## 🏗️ Architecture

```
Frontend (React) ← → Backend (FastAPI) ← → Google ADK Agent ← → MCP Tools ← → BrightData Network
```

## 📁 Project Structure

```
brightdata-mcp-adk-hackathon/
├── frontend/                 # React frontend application
│   ├── public/
│   │   └── index.html       # Main web interface
│   ├── Dockerfile           # Frontend container
│   └── package.json         # Frontend dependencies
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py         # FastAPI application
│   ├── config/
│   │   ├── __init__.py
│   │   ├── .env.example    # Environment template
│   │   └── settings.py     # Configuration management
│   ├── utils/
│   │   ├── __init__.py
│   │   └── mcp_manager.py  # MCP connection management
│   ├── Dockerfile          # Backend container
│   └── requirements.txt    # Python dependencies
├── nginx/                  # Reverse proxy configuration
├── docker-compose.yml      # Multi-container deployment
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- BrightData API credentials
- Google AI API key

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/arjunprabhulal/brightdata-mcp-adk-hackathon.git
cd brightdata-mcp-adk-hackathon
```

2. **Configure environment:**
```bash
cp backend/config/.env.example backend/config/.env
# Edit .env with your API credentials
```

3. **Start with Docker:**
```bash
docker compose up -d
```

4. **Access the platform:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

### Environment Configuration

Configure your credentials in `backend/config/.env`:

```bash
# Required API Keys
GEMINI_API_KEY=your_google_ai_api_key
BRIGHTDATA_API_TOKEN=your_brightdata_token
BROWSER_AUTH=your_browser_auth_credentials
API_TOKEN=your_api_token

# Optional Settings
HOST=0.0.0.0
PORT=8001
DEBUG=false
```

### Development Setup

**Backend Development:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001
```

**Frontend Development:**
```bash
cd frontend
# Install dependencies and start dev server
# (See frontend/package.json for specific commands)
```

## 📊 API Endpoints

### Core Endpoints

- `GET /` - API information and status
- `GET /health` - Health check with detailed status
- `POST /chat` - Main chat interface (90s timeout)
- `POST /quick-compare` - Fast comparison queries (30s timeout)
- `GET /mcp/status` - MCP connection diagnostics

### Query Types

1. **🔍 Web Search** - Multi-engine search results
2. **🌐 Website Scraping** - Extract data from specific URLs
3. **🛒 E-commerce Data** - Product info, prices, reviews
4. **📱 Social Media** - Trending content and metrics
5. **📰 News & Articles** - Latest news from multiple sources
6. **📊 Data Comparison** - Compare across platforms

## 🛠️ Available Tools

### Search & Scraping
- `search_engine` - Google, Bing, Yandex
- `scrape_as_markdown` - Clean webpage extraction
- `scraping_browser_*` - Interactive automation

### E-commerce Platforms
- Amazon, Walmart, eBay, Best Buy
- Home Depot, Zara, Etsy
- Google Shopping, App Stores

### Social Media
- LinkedIn, Instagram, Facebook
- TikTok, YouTube, Reddit, X

### Business Data
- Crunchbase, ZoomInfo
- Yahoo Finance, GitHub
- Google Maps, Zillow

## 🔧 Configuration

### Backend Settings

Configure via `backend/config/settings.py`:

- **Timeouts**: Request and quick query timeouts
- **CORS**: Cross-origin request settings
- **Model**: AI model and agent configuration
- **Server**: Host, port, and debug settings

### Frontend Configuration

- **API Endpoint**: Update in frontend configuration
- **UI Settings**: Modify React components as needed

## 🔒 Security

- **Environment Variables** - Secure credential storage
- **CORS Configuration** - Controlled cross-origin access
- **Input Validation** - Pydantic data models
- **Proxy Authentication** - Secure BrightData access
- **Container Security** - Non-root user execution

## 📈 Monitoring

### Health Checks

- **Backend**: `/health` endpoint with MCP status
- **Frontend**: HTTP availability check
- **Docker**: Built-in health check commands

### Logging

- **Application Logs** - Structured logging with levels
- **Request Tracking** - Query processing and timing
- **Error Handling** - Graceful degradation and reporting

## 🚀 Deployment

### Local Development
```bash
# Backend only
cd backend && python -m uvicorn app.main:app --reload

# Full stack with Docker
docker compose up -d
```

### Production
```bash
# Build and deploy
docker compose -f docker-compose.yml up -d

# Scale services
docker compose up -d --scale backend=2
```

### Cloud Deployment
- **AWS**: ECS, EKS, or EC2 with Docker
- **GCP**: Cloud Run, GKE, or Compute Engine
- **Azure**: Container Instances or AKS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: Check API docs at `/docs`
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions

---

**Built with ❤️ using BrightData MCP and Google ADK** 