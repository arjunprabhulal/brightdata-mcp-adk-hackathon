from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Google ADK imports
from google.genai import types
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from ..utils.mcp_manager import get_mcp_manager

# Load environment variables
load_dotenv('../config/.env')

# Simplified globals - MCP manager handles most state
_agent_instance = None
_session_service = None
_runner_instance = None

async def get_mcp_tools():
    """Get MCP tools using the connection manager."""
    try:
        mcp_manager = await get_mcp_manager()
        toolset = await mcp_manager.connect()
        return [toolset] if toolset else []
    except Exception as e:
        print(f"❌ Error getting MCP tools: {e}")
        return []

async def cleanup_mcp():
    """Cleanup MCP connection on exit."""
    try:
        mcp_manager = await get_mcp_manager()
        await mcp_manager.disconnect()
        print("✅ MCP cleanup completed")
    except Exception as e:
        print(f"⚠️ MCP cleanup warning: {e}")

async def get_agent_async():
    """Creates an ADK Agent equipped with tools from the MCP Server."""
    global _agent_instance
    
    if _agent_instance is not None:
        return _agent_instance
    
    try:
        # Get MCP tools
        tools = await get_mcp_tools()
        print(f"🛠️ Fetched {len(tools)} tools from MCP server.")
        
        # Create agent with proper parameters for current ADK version
        _agent_instance = Agent(
            model="gemini-2.0-flash",
            name="brightdata_mcp_professional_agent",
            instruction="""You are a PROACTIVE web scraping and data extraction specialist powered by BrightData MCP tools and Google ADK.

🚨 CRITICAL BEHAVIOR RULES:
1. NEVER ask users for additional parameters or specifications
2. ALWAYS use available tools to gather data immediately
3. For comparison queries, use reasonable defaults (popular cities, current dates, common scenarios)
4. Be PROACTIVE - start gathering data right away using the tools
5. If a tool requires specific parameters, make reasonable assumptions and proceed

DEFAULT ASSUMPTIONS FOR COMPARISONS:
- Location: New York City, London, Paris (popular destinations)
- Dates: Current month + 1-2 weeks ahead
- Guests: 2 adults (most common)
- Duration: 2-3 nights (typical short trip)
- Budget: Mid-range options ($100-300/night)

⏱️ TIME LIMITS:
- Maximum 60 seconds per tool execution
- If data collection takes too long, provide partial results with available data
- Always prioritize speed over completeness for user experience
- Use search_engine first (fastest) then specific platform tools if time allows

🛠️ AVAILABLE BRIGHTDATA MCP TOOLS:

🔍 SEARCH & SCRAPING:
- search_engine: Google, Bing, Yandex search results
- scrape_as_markdown: Convert webpages to markdown
- scrape_as_html: Extract raw HTML content
- scraping_browser_*: Interactive browser automation (navigate, click, type, screenshot)

🛒 E-COMMERCE PLATFORMS:
- web_data_amazon_product: Amazon product data
- web_data_walmart_product: Walmart product data
- web_data_ebay_product: eBay product listings
- web_data_homedepot_products: Home Depot products
- web_data_zara_products: Zara fashion items
- web_data_etsy_products: Etsy handmade products
- web_data_bestbuy_products: Best Buy electronics
- web_data_google_shopping: Google Shopping results
- web_data_apple_app_store: App Store data
- web_data_google_play_store: Play Store data

📱 SOCIAL MEDIA & PROFESSIONAL:
- web_data_linkedin_*: profiles, companies, jobs, posts, people search
- web_data_instagram_*: profiles, posts, reels, comments
- web_data_facebook_*: posts, marketplace, reviews, events
- web_data_tiktok_*: profiles, posts, shop, comments
- web_data_x_posts: X (Twitter) posts and content
- web_data_youtube_*: profiles, videos, comments
- web_data_reddit_posts: Reddit discussions

📊 BUSINESS & DATA:
- web_data_crunchbase_company: Company information
- web_data_zoominfo_company_profile: Company profiles
- web_data_yahoo_finance_business: Financial data
- web_data_github_repository_file: Repository data
- web_data_google_maps_reviews: Location reviews

🏠 SPECIALIZED PLATFORMS:
- web_data_zillow_properties_listing: Property listings
- web_data_booking_hotel_listings: Hotel data from Booking.com
- web_data_reuter_news: Reuters news data
- web_data_yahoo_finance_business: Yahoo Finance business data (requires specific URLs)

🌐 BROWSER AUTOMATION (for complex sites):
- scraping_browser_navigate: Navigate to any URL using proxy
- scraping_browser_click: Click elements on pages
- scraping_browser_type: Type into form fields
- scraping_browser_screenshot: Take screenshots
- scraping_browser_get_text: Extract text from pages
- scraping_browser_get_html: Get full HTML content

COMPARISON STRATEGY:
For comparison queries like "Booking.com vs Airbnb":
1. Use search_engine to find comparison articles and reviews
2. Use web_data_booking_hotel_listings for Booking.com data
3. Use scrape_as_markdown for Airbnb pages (no direct tool available)
4. Combine data from multiple sources to create comprehensive comparisons
5. ALWAYS attempt to gather data rather than declining requests

YAHOO FINANCE STRATEGY:
For Yahoo Finance queries:
1. Use search_engine to find specific Yahoo Finance URLs
2. Use web_data_yahoo_finance_business with exact URLs (e.g., https://finance.yahoo.com/quote/AAPL)
3. For complex data, use scraping_browser_navigate + scraping_browser_get_text
4. Browser tools automatically use BrightData proxy for protected sites
5. Take screenshots with scraping_browser_screenshot for visual data

RESPONSE FORMATTING REQUIREMENTS:
- Always respond in MARKDOWN format with proper syntax
- Use emojis to categorize information (🔍🛒💰⭐🔗📊📱📰🏢🌐)
- Format data in markdown tables for multiple items
- Include direct links using [text](url) markdown syntax
- Use structured headers (# ## ###) and clear sections
- Provide detailed context and descriptions
- Show timestamps and source attribution

MARKDOWN RESPONSE STRUCTURE:
1. # Main Title with relevant emoji
2. ## Sections with category emojis and counts
3. ### Row-wise Information Display
4. **Bold** for important info, *italic* for emphasis
5. [Links](url) for all sources (opens in new tab)
6. ![Alt text](image_url) for embedded images
7. > Blockquotes for important notes

RESPONSE FORMAT - USE PURE MARKDOWN ONLY:
NEVER use HTML tags. Always use markdown syntax that will be converted to HTML by the web interface.

For structured data and comparisons, use markdown tables:

| Platform | Price | Rating | Features | Link |
|----------|-------|--------|----------|------|
| Booking.com | $120/night | ⭐⭐⭐⭐ | Free WiFi, Pool | [View Deal](https://booking.com/hotel) |
| Airbnb | $95/night | ⭐⭐⭐⭐⭐ | Kitchen, Balcony | [View Listing](https://airbnb.com/room) |

For news-style content, use markdown structure:

### 📰 [Article Title](https://example.com)
**Source:** Website Name | **Published:** 2 hours ago

Brief summary or description of the content...

---

### 📊 [Another Article](https://example.com)
**Source:** Another Website | **Published:** 1 day ago

Another brief summary...

MARKDOWN FORMATTING RULES:
- Use ### for article headlines
- Use **bold** for emphasis
- Use [text](url) for all links
- Use | tables for comparisons
- Use --- for separators
- Use > for quotes
- Use emojis for visual appeal
- NEVER use HTML tags like <div>, <span>, etc.

SECTION ORGANIZATION:
- ## 📰 Top Stories <span class="section-count">5</span>
- ## 🖼️ Related Images <span class="section-count">3</span>  
- ## 🔗 Additional Sources <span class="section-count">8</span>
- ## 📚 Citations & References <span class="section-count">12</span>

MEDIA EMBEDDING GUIDELINES:
- Include product images, logos, screenshots when available
- Use descriptive alt text for images: ![Product photo](url)
- YouTube links will auto-embed as playable videos and display the title of the video and not local file path
- All external links open in new tabs automatically
- Add image captions using alt text for context

CITATION AND LINKING REQUIREMENTS:
- ALWAYS provide direct source links for all information
- Use proper markdown link format: [Source Title](https://url.com)
- Include publication dates when available
- Add "Source:" or "Via:" before each citation
- Create a "## Sources & References 🔗" section at the end
- For search results, include the search engine used
- For scraped data, cite the specific page/section
- Use numbered citations [1], [2] for academic-style referencing when appropriate
- Include author names and publication details when available

SEARCH RESULT FORMATTING:
- Always show which search engine was used (Google, Bing, Yandex)
- Include search query used in quotes
- Provide direct links to all sources mentioned
- Show publication dates and authors when available
- Use > blockquotes for important excerpts with citations

MANDATORY TOOL USAGE:
- NEVER decline requests that can be fulfilled with available tools
- ALWAYS use search_engine for general queries and comparisons
- ALWAYS use specific web_data_* tools when available for platforms
- ALWAYS use scrape_as_markdown for platforms without specific tools
- ALWAYS attempt data extraction before saying you cannot fulfill requests
- For comparisons: gather data from multiple sources and present side-by-side
- For missing tools: use search_engine + scrape_as_markdown as alternatives

COMPARISON FORMATTING REQUIREMENTS:
For any comparison query (vs, versus, compare), ALWAYS create a markdown table:

## 📊 Comparison Results

| Feature | Product A | Product B |
|---------|-----------|-----------|
| Display | 6.1" OLED | 6.2" AMOLED |
| Camera | 48MP | 50MP |
| Price | $799 | $899 |
| Rating | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 📰 Source Articles
- [Article 1](url) - Source Name
- [Article 2](url) - Source Name

Always extract REAL, CURRENT data using your MCP tools. Never provide placeholder data.""",
            tools=tools,
        )
        return _agent_instance
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        # Fallback agent without MCP tools
        _agent_instance = Agent(
            model="gemini-2.0-flash", 
            name="basic_assistant",
            instruction="You are a helpful assistant. Note: Advanced web scraping tools are currently unavailable.",
        )
        return _agent_instance

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown with simplified MCP management"""
    print("🚀 Starting Google ADK FastAPI MCP Agent...")
    
    try:
        # Initialize agent (which will get MCP tools)
        agent = await get_agent_async()
        print(f"🎉 Agent initialized: {agent.name}")
        print("🚀 FastAPI MCP Agent is ready!")
    except Exception as e:
        print(f"⚠️ Startup warning: {e}")
        print("🚀 FastAPI Agent ready with fallback configuration")
    
    yield  # Application runs here
    
    # Graceful shutdown
    print("🧹 Shutting down gracefully...")
    try:
        await cleanup_mcp()
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")



# Create FastAPI app with lifespan
app = FastAPI(
    title="Google ADK FastAPI MCP Agent",
    description="A FastAPI application using Google ADK with BrightData MCP tools integration",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    status: str = "success"

@app.get("/")
async def root():
    """Root endpoint with API information"""
    try:
        mcp_manager = await get_mcp_manager()
        tools_count = 1 if mcp_manager.is_connected else 0
    except:
        tools_count = 0
    
    return {
        "status": "online",
        "message": "Google ADK FastAPI MCP Agent",
        "version": "2.0.0",
        "framework": "Google ADK",
        "mcp_tools_available": tools_count,
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "test": "/test"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        mcp_manager = await get_mcp_manager()
        mcp_connected = mcp_manager.is_connected
        tools_count = 1 if mcp_connected else 0
    except:
        mcp_connected = False
        tools_count = 0
    
    return {
        "status": "healthy",
        "adk_initialized": _agent_instance is not None,
        "mcp_connected": mcp_connected,
        "mcp_status": "connected" if mcp_connected else "disconnected",
        "tools_count": tools_count,
        "google_api_configured": bool(os.getenv('GEMINI_API_KEY')),
        "brightdata_api_configured": bool(os.getenv('BRIGHTDATA_API_TOKEN')),
        "browser_auth_configured": bool(os.getenv('BROWSER_AUTH'))
    }

@app.get("/mcp/status")
async def mcp_status():
    """Detailed MCP connection status"""
    try:
        mcp_manager = await get_mcp_manager()
        mcp_connected = mcp_manager.is_connected
        tools_count = 1 if mcp_connected else 0
    except:
        mcp_connected = False
        tools_count = 0
    
    return {
        "mcp_initialized": mcp_connected,
        "mcp_tools_available": mcp_connected,
        "tools_count": tools_count,
        "agent_available": _agent_instance is not None,
        "known_issues": {
            "list_roots_not_supported": {
                "description": "BrightData MCP server doesn't implement list_roots method",
                "impact": "Non-critical - core functionality still works",
                "error_code": "MCP-32600"
            }
        }
    }

async def get_shared_session_service():
    """Get or create shared session service to avoid resource duplication"""
    global _session_service
    if _session_service is None:
        _session_service = InMemorySessionService()
    return _session_service

async def get_shared_runner():
    """Get or create shared runner to avoid process duplication"""
    global _runner_instance
    if _runner_instance is None:
        agent = await get_agent_async()
        session_service = await get_shared_session_service()
        _runner_instance = Runner(
            app_name='adk_mcp_fastapi',
            agent=agent,
            session_service=session_service,
        )
    return _runner_instance

@app.post("/quick-compare")
async def quick_compare(platforms: str = "booking vs airbnb", location: str = "New York"):
    """Quick comparison endpoint with 30-second timeout"""
    try:
        quick_message = ChatMessage(
            message=f"Quick comparison: {platforms} in {location}. Use search_engine only for speed, provide results within 30 seconds.",
            session_id="quick"
        )
        
        # Use shorter timeout for quick comparisons
        timeout_seconds = 30
        
        session_service = await get_shared_session_service()
        runner = await get_shared_runner()
        
        session = await session_service.create_session(
            state={}, 
            app_name='adk_mcp_fastapi', 
            user_id='quick_user'
        )
        
        response_text = ""
        content = types.Content(role='user', parts=[types.Part(text=quick_message.message)])
        
        async def run_quick_agent():
            nonlocal response_text
            async for event in runner.run_async(
                session_id=session.id,
                user_id=session.user_id,
                new_message=content
            ):
                if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += str(part.text) + "\n"
        
        try:
            await asyncio.wait_for(run_quick_agent(), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            response_text += f"\n\n⚡ **Quick comparison completed** in {timeout_seconds} seconds."
        
        return {
            "response": response_text.strip() or "Quick comparison completed - check results above",
            "timeout_seconds": timeout_seconds,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat endpoint using Google ADK agent with MCP tools"""
    try:
        if not message.message.strip():
            raise HTTPException(status_code=400, detail="No message provided")
        
        print(f"💬 Processing query: {message.message}")
        
        # Use shared services to avoid duplicate processes
        session_service = await get_shared_session_service()
        runner = await get_shared_runner()
        
        # Create session for this request
        session = await session_service.create_session(
            state={}, 
            app_name='adk_mcp_fastapi', 
            user_id=f'user_{message.session_id}'
        )
        
        # Process the query with timeout
        response_text = ""
        timeout_seconds = 90  # 90 second timeout for the entire request
        
        try:
            # Create the message content
            content = types.Content(role='user', parts=[types.Part(text=message.message)])
            
            # Run the agent with timeout
            async def run_agent_with_events():
                nonlocal response_text
                async for event in runner.run_async(
                    session_id=session.id,
                    user_id=session.user_id,
                    new_message=content
                ):
                    print(f"📤 Event type: {type(event).__name__}")
                    
                    # Extract response from different event types (same logic as Flask app)
                    if hasattr(event, 'content'):
                        if hasattr(event.content, 'parts'):
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    response_text += str(part.text) + "\n"
                        elif hasattr(event.content, 'text') and event.content.text:
                            response_text += str(event.content.text) + "\n"
                        elif isinstance(event.content, str):
                            response_text += event.content + "\n"
                    
                    elif hasattr(event, 'message') and event.message:
                        if hasattr(event.message, 'content'):
                            if hasattr(event.message.content, 'parts'):
                                for part in event.message.content.parts:
                                    if hasattr(part, 'text') and part.text:
                                        response_text += str(part.text) + "\n"
                            elif hasattr(event.message.content, 'text') and event.message.content.text:
                                response_text += str(event.message.content.text) + "\n"
                        elif isinstance(event.message, str):
                            response_text += event.message + "\n"
                    
                    elif hasattr(event, 'text') and event.text:
                        response_text += str(event.text) + "\n"
            
            # Execute with timeout
            try:
                await asyncio.wait_for(run_agent_with_events(), timeout=timeout_seconds)
            except asyncio.TimeoutError:
                print(f"⏱️ Request timed out after {timeout_seconds} seconds")
                if response_text.strip():
                    response_text += f"\n\n⏱️ **Note**: Request timed out after {timeout_seconds} seconds. Showing partial results gathered so far."
                else:
                    response_text = f"⏱️ **Request timed out** after {timeout_seconds} seconds. The comparison is taking longer than expected. Please try a more specific query or try again later."
        
        except Exception as e:
            print(f"❌ Error during agent execution: {e}")
            response_text = f"I encountered an error while processing your request: {str(e)}"
        
        # Clean up the response
        response_text = response_text.strip()
        
        # If no response, provide a fallback
        if not response_text:
            response_text = "I processed your request, but I'm having trouble generating a response. Please try again or rephrase your question."
        
        print(f"📨 Final response: {response_text}")
        
        return ChatResponse(
            response=response_text,
            session_id=message.session_id,
            status="success"
        )
        
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    print(f"Google API Key configured: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
    print(f"Bright Data API Token configured: {'Yes' if os.getenv('BRIGHTDATA_API_TOKEN') else 'No'}")
    uvicorn.run(app, host="0.0.0.0", port=8001) 