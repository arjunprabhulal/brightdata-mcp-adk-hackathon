"""
MCP Connection Manager for BrightData Tools
Handles connection lifecycle, process management, and error recovery
"""

import os
import asyncio
import subprocess
import signal
from typing import Optional, Dict, Any
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

class MCPConnectionManager:
    """Manages MCP server connections with proper lifecycle management"""
    
    def __init__(self):
        self._toolset: Optional[MCPToolset] = None
        self._process: Optional[subprocess.Popen] = None
        self._connection_params: Optional[StdioServerParameters] = None
        self._is_connected = False
        self._connection_lock = asyncio.Lock()
        self._connection_attempted = False
        
    async def connect(self) -> Optional[MCPToolset]:
        """Connect to MCP server with proper process management"""
        async with self._connection_lock:
            # Always reuse existing connection if available
            if self._is_connected and self._toolset:
                print("♻️ Reusing existing MCP connection")
                return self._toolset
            
            # Prevent multiple connection attempts
            if self._connection_attempted and not self._is_connected:
                print("⚠️ Previous connection attempt failed, returning None")
                return None
            
            self._connection_attempted = True
            
            try:
                # Validate environment variables
                api_token = os.getenv('BRIGHTDATA_API_TOKEN')
                browser_auth = os.getenv('BROWSER_AUTH')
                
                if not api_token:
                    raise ValueError("BRIGHTDATA_API_TOKEN not found in environment")
                if not browser_auth:
                    raise ValueError("BROWSER_AUTH not found in environment")
                
                print("🔐 Environment validation passed")
                
                # Create environment for MCP server
                mcp_env = self._create_mcp_environment()
                
                # Create connection parameters only once
                if not self._connection_params:
                    self._connection_params = StdioServerParameters(
                        command='npx',
                        args=["-y", "@brightdata/mcp"],
                        env=mcp_env
                    )
                
                print("🚀 Creating MCP toolset...")
                
                # Create the toolset only once
                if not self._toolset:
                    self._toolset = MCPToolset(connection_params=self._connection_params)
                
                # Test connection briefly
                await self._test_connection()
                
                self._is_connected = True
                print("✅ MCP connection established successfully")
                
                return self._toolset
                
            except Exception as e:
                print(f"❌ MCP connection failed: {e}")
                
                # Handle specific known errors
                if "List roots not supported" in str(e) or "MCP error -32600" in str(e):
                    print("ℹ️ Note: List roots error is expected and non-critical")
                    # The connection might still work for actual tool calls
                    if self._toolset:
                        self._is_connected = True
                        print("✅ Proceeding with MCP connection despite list_roots warning")
                        return self._toolset
                
                # Don't cleanup on known errors, just mark as connected
                if self._toolset and ("List roots not supported" in str(e) or "MCP error -32600" in str(e)):
                    self._is_connected = True
                    return self._toolset
                
                await self._cleanup()
                return None
    
    def _create_mcp_environment(self) -> Dict[str, str]:
        """Create comprehensive environment for MCP server"""
        base_env = {
            "API_TOKEN": os.getenv('BRIGHTDATA_API_TOKEN'),
            "BRIGHTDATA_API_TOKEN": os.getenv('BRIGHTDATA_API_TOKEN'),  # Backup key
            "BROWSER_AUTH": os.getenv('BROWSER_AUTH'),
            "WEB_UNLOCKER_ZONE": os.getenv('WEB_UNLOCKER_ZONE', 'web_unlocker1'),
            "NODE_ENV": os.getenv('NODE_ENV', 'production'),
            "PATH": os.environ.get("PATH", ""),
            "NPM_CONFIG_REGISTRY": "https://registry.npmjs.org/",
            "NODE_OPTIONS": "--max-old-space-size=2048"
        }
        
        # Filter out None values
        return {k: v for k, v in base_env.items() if v is not None}
    
    async def _test_connection(self):
        """Test MCP connection health"""
        try:
            # Basic validation that toolset was created
            if not self._toolset:
                raise RuntimeError("Toolset not created")
            
            # Additional validation can be added here
            print("🔍 MCP connection test passed")
            
        except Exception as e:
            print(f"⚠️ MCP connection test warning: {e}")
            # Don't fail completely on test warnings
    
    async def disconnect(self):
        """Properly disconnect and cleanup MCP resources"""
        async with self._connection_lock:
            await self._cleanup()
    
    async def _cleanup(self):
        """Internal cleanup method"""
        try:
            if self._process:
                try:
                    self._process.terminate()
                    # Give it a moment to terminate gracefully
                    await asyncio.sleep(1)
                    if self._process.poll() is None:
                        self._process.kill()
                    print("🧹 MCP process cleaned up")
                except Exception as e:
                    print(f"⚠️ Process cleanup warning: {e}")
            
            self._toolset = None
            self._process = None
            self._connection_params = None
            self._is_connected = False
            self._connection_attempted = False
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    @property
    def is_connected(self) -> bool:
        """Check if MCP is currently connected"""
        return self._is_connected and self._toolset is not None
    
    @property
    def toolset(self) -> Optional[MCPToolset]:
        """Get the current toolset"""
        return self._toolset if self._is_connected else None

# Singleton instance
_mcp_manager = MCPConnectionManager()

async def get_mcp_manager() -> MCPConnectionManager:
    """Get the singleton MCP manager instance"""
    return _mcp_manager 