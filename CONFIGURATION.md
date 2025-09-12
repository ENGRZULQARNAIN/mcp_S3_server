# MCP S3 Server Configuration Guide

This guide shows how to configure and connect the MCP S3 Server with clients using environment variables.

## Installation

Install the MCP S3 Server using uv:

```bash
# Install globally
uv tool install mcp-s3-server

# Or run directly without installing
uvx mcp-s3-server
```

## Environment Variables

### AWS Configuration

Set these environment variables for AWS access:

```bash
# Required: AWS Credentials
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key_here"
export AWS_DEFAULT_REGION="us-east-1"

# Optional: For temporary credentials (STS)
export AWS_SESSION_TOKEN="your_session_token_here"

# Optional: For S3-compatible services (DigitalOcean Spaces, IBM Cloud, etc.)
export S3_ENDPOINT_URL="https://nyc3.digitaloceanspaces.com"
```

## Client Configuration Examples

### 1. Claude Desktop Configuration

Add this to your Claude Desktop config file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mcp-s3-server": {
      "command": "uvx",
      "args": ["mcp-s3-server"],
      "env": {
        "AWS_ACCESS_KEY_ID": "your_access_key_here",
        "AWS_SECRET_ACCESS_KEY": "your_secret_access_key_here",
        "AWS_DEFAULT_REGION": "us-east-1",
        "S3_ENDPOINT_URL": "https://nyc3.digitaloceanspaces.com"
      }
    }
  }
}
```

### 2. Using with MCP Client Library

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Environment variables for the server process
    env = {
        "AWS_ACCESS_KEY_ID": "your_access_key_here",
        "AWS_SECRET_ACCESS_KEY": "your_secret_access_key_here", 
        "AWS_DEFAULT_REGION": "us-east-1",
        "S3_ENDPOINT_URL": "https://nyc3.digitaloceanspaces.com"
    }
    
    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-s3-server"],
        env=env
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])
            
            # Call the list_s3_buckets tool
            result = await session.call_tool("list_s3_buckets", {})
            print("Buckets:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Credentials Priority

The server will attempt to find AWS credentials in this order:

1. **Environment variables** (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
2. **AWS credentials file** (~/.aws/credentials)
3. **AWS config file** (~/.aws/config)
4. **IAM roles** (for EC2 instances)
5. **ECS container credentials**
6. **Default credential providers**

## Testing the Connection

### 1. Test Server Startup

```bash
# Set environment variables
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key_here"
export AWS_DEFAULT_REGION="us-east-1"
export S3_ENDPOINT_URL="https://nyc3.digitaloceanspaces.com"

# Run the server (it will wait for client connection)
uvx mcp-s3-server
```

### 2. Test with MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Test the server
mcp-inspector uvx mcp-s3-server
```

### 3. Verify AWS Access

Before running the server, test your AWS credentials:

```bash
# Using AWS CLI
aws s3 ls

# Or using Python
python3 -c "
import boto3
try:
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    print(f'Found {len(buckets[\"Buckets\"])} buckets')
except Exception as e:
    print(f'Error: {e}')
"
```

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use IAM roles** when possible (especially on AWS infrastructure)
3. **Use temporary credentials** (STS) for enhanced security
4. **Limit IAM permissions** to only required S3 actions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:ListAllMyBuckets",
           "s3:ListBucket",
           "s3:GetObject"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

## Troubleshooting

### Common Issues

1. **"AWS credentials not found"**
   - Verify environment variables are set correctly
   - Check AWS credentials file permissions

2. **"Access denied"**
   - Verify IAM permissions for S3 operations
   - Check if MFA is required

3. **"Invalid region"**
   - Ensure AWS_DEFAULT_REGION is set to a valid region
   - Some buckets may be in different regions

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
uvx mcp-s3-server
```

## Available Tools

The server currently provides:

- **test_connection**: Test MCP S3 server connection
- **list_s3_buckets**: Lists all accessible S3 buckets with creation dates
- **list_s3_objects**: Lists objects in a specific S3 bucket with optional prefix filtering

### Tool Parameters

#### list_s3_objects
- **bucket_name** (required): Name of the S3 bucket to list objects from
- **prefix** (optional): Prefix to filter objects (e.g., 'folder/subfolder/')
- **max_keys** (optional): Maximum number of objects to return (default: 100, max: 1000)

Example usage:
```json
{
  "tool": "list_s3_objects",
  "parameters": {
    "bucket_name": "my-bucket",
    "prefix": "documents/",
    "max_keys": 50
  }
}
```

Additional tools can be easily added to the server architecture.
