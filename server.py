#!/usr/bin/env python3
"""
MCP S3 Server - A Model Context Protocol server for AWS S3 operations.

This server enables AI models to interact with AWS S3 buckets securely,
providing tools to list buckets, list objects, and download file contents.
"""

import asyncio
import sys
import logging
import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

# Configure logging to stderr to avoid interfering with JSON-RPC
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
    force=True
)
logger = logging.getLogger(__name__)

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp import types
    import aioboto3
    from botocore.exceptions import ClientError, NoCredentialsError
    logger.info("MCP and AWS imports successful")
except ImportError as e:
    logger.error(f"Import failed: {e}")
    sys.exit(1)


# Create server instance
app = Server("mcp-s3-server")


from src.mcp_s3_server.tools.list_buckets_tool import list_buckets_tool
from src.mcp_s3_server.config import S3Config

@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available tools."""
    logger.info("Listing tools...")
    return [
        types.Tool(
            name="test_connection",
            description="Test MCP S3 server connection",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="list_s3_buckets",
            description="List all S3 buckets in your storage account (supports AWS S3, DigitalOcean Spaces, IBM Cloud Object Storage, and other S3-compatible services)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

s3_config = S3Config.from_environment()

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool called: {name}")

    if name == "test_connection":
        return [types.TextContent(
            type="text",
            text="✅ SUCCESS! MCP S3 Server is working!\n\nConnection established successfully. The server is ready for S3 operations."
        )]
    
    elif name == "list_s3_buckets":
       return await list_buckets_tool(s3_config)
    
    else:
        return [types.TextContent(
            type="text",
            text=f"❌ Unknown tool: {name}\n\nAvailable tools: test_connection, list_s3_buckets"
        )]

async def main():
    """Main server function."""
    logger.info("Starting MCP S3 Server...")
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("STDIO server established, running...")
            await app.run(
                read_stream, 
                write_stream, 
                app.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("MCP S3 Server starting...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
