#!/usr/bin/env python3
"""
Entry point for the MCP S3 Server when installed as a package.
Provides an MCP stdio server for S3-compatible operations.
"""

import asyncio
import sys
import logging
from typing import Any, Dict, List

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
    logger.info("MCP imports successful")
except ImportError as e:
    logger.error(f"Import failed: {e}")
    sys.exit(1)

from mcp_s3_server.tools.list_buckets_tool import list_buckets_tool
from mcp_s3_server.tools.list_object_tool import list_objects_tool
from mcp_s3_server.config import S3Config


# Create server instance
app = Server("mcp-s3-server")


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available tools."""
    logger.info("Listing tools...")
    return [
        types.Tool(
            name="test_connection",
            description="Test MCP S3 server connection",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="list_s3_buckets",
            description=(
                "List all S3 buckets in your storage account (supports AWS S3, "
                "DigitalOcean Spaces, IBM Cloud Object Storage, and other "
                "S3-compatible services)"
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="list_s3_objects",
            description=(
                "List objects in a specific S3 bucket with optional prefix filtering. "
                "Supports AWS S3, DigitalOcean Spaces, IBM Cloud Object Storage, and other "
                "S3-compatible services."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the S3 bucket to list objects from"
                    },
                    "prefix": {
                        "type": "string",
                        "description": "Optional prefix to filter objects (e.g., 'folder/subfolder/')",
                        "default": ""
                    },
                    "max_keys": {
                        "type": "integer",
                        "description": "Maximum number of objects to return (default: 100, max: 1000)",
                        "default": 100,
                        "minimum": 1,
                        "maximum": 1000
                    }
                },
                "required": ["bucket_name"]
            },
        ),
    ]


s3_config = S3Config.from_environment()


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool called: {name}")

    if name == "test_connection":
        return [
            types.TextContent(
                type="text",
                text=(
                    "✅ SUCCESS! MCP S3 Server is working!\n\n"
                    "Connection established successfully. The server is ready for S3 operations."
                ),
            )
        ]

    if name == "list_s3_buckets":
        return await list_buckets_tool(s3_config)
    
    if name == "list_s3_objects":
        bucket_name = arguments.get("bucket_name")
        if not bucket_name:
            return [
                types.TextContent(
                    type="text",
                    text="❌ Missing required parameter: bucket_name\n\nPlease provide the name of the bucket to list objects from."
                )
            ]
        
        prefix = arguments.get("prefix", "")
        max_keys = arguments.get("max_keys", 100)
        
        return await list_objects_tool(s3_config, bucket_name, prefix, max_keys)

    return [
        types.TextContent(
            type="text",
            text=(
                "❌ Unknown tool: {name}\n\nAvailable tools: test_connection, list_s3_buckets, list_s3_objects"
            ).format(name=name),
        )
    ]


async def _main_async() -> None:
    """Run the stdio MCP server."""
    logger.info("Starting MCP S3 Server (package entry point)...")
    async with stdio_server() as (read_stream, write_stream):
        logger.info("STDIO server established, running...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def main() -> None:
    try:
        asyncio.run(_main_async())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:  # noqa: BLE001 - log and exit non-zero
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()


