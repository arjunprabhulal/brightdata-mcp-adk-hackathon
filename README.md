# 🌐 BrightData MCP × Google ADK Platform

Professional Web Scraping & Data Extraction Platform powered by BrightData's Model Context Protocol (MCP) and Google's Agent Development Kit (ADK).

## 🌟 Live Demo

**🚀 Try it now**: https://brightdata-mcp.aicloudlab.dev/

**📝 Featured Article**: [BrightData MCP × Google ADK Platform](https://dev.to/arjun_prabhulal/brightdata-mcp-google-adk-professional-web-scraping-platform-2f5d) on DEV Community

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

## 🛠️ Tech Stack

### **🤖 AI & Machine Learning**
- **Google Gemini 2.0 Flash** - Primary LLM for intelligent query processing
- **Google Agent Development Kit (ADK)** - Agent framework and infrastructure
- **Model Context Protocol (MCP)** - Standardized protocol for AI-tool integration
- **BrightData MCP Server** - 50+ specialized web scraping tools

### **🔧 Backend Technologies**
- **Python 3.11+** - Primary backend language
- **FastAPI** - High-performance web framework
- **Uvicorn** - ASGI server for FastAPI
- **Pydantic** - Data validation and settings management
- **Asyncio** - Asynchronous programming support

### **🌐 Frontend Technologies**
- **React** - Frontend JavaScript library
- **HTML5/CSS3** - Web standards
- **JavaScript/TypeScript** - Frontend scripting
- **Responsive Design** - Mobile-first approach

### **🐳 Infrastructure & Deployment**
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and load balancer
- **Let's Encrypt** - SSL certificate management
- **Google Cloud Platform (GCP)** - Cloud infrastructure
- **Compute Engine** - Virtual machine hosting

### **🔒 Security & Networking**
- **SSL/TLS** - HTTPS encryption
- **HSTS** - HTTP Strict Transport Security
- **CSP** - Content Security Policy headers
- **CORS** - Cross-Origin Resource Sharing
- **Rate Limiting** - API protection
- **Environment Variables** - Secure credential storage

### **🌍 Web Scraping & Data**
- **BrightData Proxy Network** - Enterprise proxy infrastructure
- **SerpAPI** - Search engine results API
- **REST APIs** - Various data source integrations
- **JSON** - Data interchange format

### **🔧 Development Tools**
- **Git** - Version control
- **GitHub** - Repository hosting
- **VS Code/Cursor** - Development environment
- **npm/pip** - Package management

### **📊 Monitoring & Health**
- **Health Check Endpoints** - Service monitoring
- **Docker Health Checks** - Container monitoring
- **Structured Logging** - Application logging
- **Error Handling** - Graceful degradation

### **🔌 Integration Protocols**
- **HTTP/HTTPS** - Web protocols
- **WebSocket** - Real-time communication
- **stdio** - MCP server communication
- **JSON-RPC** - Remote procedure calls

### **📦 Key Dependencies**

**Backend (Python):**
```python
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
google-adk>=0.1.0
pydantic>=2.0.0
python-dotenv>=1.0.0
google-generativeai>=0.8.0
```

**Frontend (Node.js):**
```json
{
  "react": "^18.0.0",
  "typescript": "^5.0.0",
  "vite": "^5.0.0"
}
```

### **🏗️ Architecture Patterns**
- **Microservices** - Containerized services
- **Client-Server** - Frontend-backend separation
- **MCP Protocol** - Standardized AI-tool communication
- **Proxy Pattern** - Nginx reverse proxy
- **Event-Driven** - Asynchronous processing

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

**Local Development:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

**Live Platform:**
- Frontend: https://brightdata-mcp.aicloudlab.dev/
- Backend API: https://brightdata-mcp.aicloudlab.dev/api/
- API Docs: https://brightdata-mcp.aicloudlab.dev/docs

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

**Live Production Instance:**
- **URL**: https://brightdata-mcp.aicloudlab.dev/
- **Infrastructure**: GCP Compute Engine with Docker
- **SSL**: Let's Encrypt certificates with auto-renewal
- **Security**: HTTPS, HSTS, CSP headers, rate limiting

**Local Production Build:**
```bash
# Build and deploy
docker compose -f docker-compose.yml up -d

# Scale services
docker compose up -d --scale backend=2
```

### Cloud Deployment
- **AWS**: ECS, EKS, or EC2 with Docker
- **GCP**: Cloud Run, GKE, or Compute Engine ✅ (Currently deployed)
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