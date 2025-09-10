# S3-Compatible Storage Providers Configuration

Your MCP S3 Server now supports multiple S3-compatible storage providers! Here are configuration examples for popular services:

## 🔧 Configuration

Add these environment variables to your Claude Desktop config:

### AWS S3 (Default)
```json
{
  "mcpServers": {
    "mcp-s3-server": {
      "env": {
        "AWS_ACCESS_KEY_ID": "your_aws_access_key",
        "AWS_SECRET_ACCESS_KEY": "your_aws_secret_key",
        "AWS_DEFAULT_REGION": "us-east-1"
      }
    }
  }
}
```

### DigitalOcean Spaces
```json
{
  "mcpServers": {
    "mcp-s3-server": {
      "env": {
        "AWS_ACCESS_KEY_ID": "your_do_spaces_key",
        "AWS_SECRET_ACCESS_KEY": "your_do_spaces_secret",
        "AWS_DEFAULT_REGION": "nyc3",
        "S3_ENDPOINT_URL": "https://nyc3.digitaloceanspaces.com"
      }
    }
  }
}
```

### IBM Cloud Object Storage
```json
{
  "mcpServers": {
    "mcp-s3-server": {
      "env": {
        "AWS_ACCESS_KEY_ID": "your_ibm_access_key",
        "AWS_SECRET_ACCESS_KEY": "your_ibm_secret_key",
        "AWS_DEFAULT_REGION": "us-south",
        "S3_ENDPOINT_URL": "https://s3.us-south.cloud-object-storage.appdomain.cloud"
      }
    }
  }
}
```

### MinIO (Self-hosted)
```json
{
  "mcpServers": {
    "mcp-s3-server": {
      "env": {
        "AWS_ACCESS_KEY_ID": "your_minio_access_key",
        "AWS_SECRET_ACCESS_KEY": "your_minio_secret_key",
        "AWS_DEFAULT_REGION": "us-east-1",
        "S3_ENDPOINT_URL": "http://localhost:9000"
      }
    }
  }
}
```

### Wasabi Cloud Storage
```json
{
  "mcpServers": {
    "mcp-s3-server": {
      "env": {
        "AWS_ACCESS_KEY_ID": "your_wasabi_access_key",
        "AWS_SECRET_ACCESS_KEY": "your_wasabi_secret_key",
        "AWS_DEFAULT_REGION": "us-east-1",
        "S3_ENDPOINT_URL": "https://s3.wasabisys.com"
      }
    }
  }
}
```

### Backblaze B2 (via S3-compatible API)
```json
{
  "mcpServers": {
    "mcp-s3-server": {
      "env": {
        "AWS_ACCESS_KEY_ID": "your_b2_key_id",
        "AWS_SECRET_ACCESS_KEY": "your_b2_application_key",
        "AWS_DEFAULT_REGION": "us-west-002",
        "S3_ENDPOINT_URL": "https://s3.us-west-002.backblazeb2.com"
      }
    }
  }
}
```

## 🌐 Popular Endpoint URLs

| Provider | Endpoint URL Format | Example |
|----------|-------------------|---------|
| **AWS S3** | *Leave empty* | - |
| **DigitalOcean Spaces** | `https://{region}.digitaloceanspaces.com` | `https://nyc3.digitaloceanspaces.com` |
| **IBM Cloud** | `https://s3.{region}.cloud-object-storage.appdomain.cloud` | `https://s3.us-south.cloud-object-storage.appdomain.cloud` |
| **MinIO** | `http://localhost:9000` or your MinIO URL | `http://localhost:9000` |
| **Wasabi** | `https://s3.wasabisys.com` | `https://s3.wasabisys.com` |
| **Backblaze B2** | `https://s3.{region}.backblazeb2.com` | `https://s3.us-west-002.backblazeb2.com` |

## ✅ Features Supported

- ✅ List buckets/spaces
- ✅ Auto-detect storage provider
- ✅ Custom endpoint URLs
- ✅ Regional endpoints
- ✅ Comprehensive error handling
- ✅ Secure credential management

## 🔍 Testing Your Configuration

1. **Restart Claude Desktop** after updating configuration
2. **Use the `test_connection` tool** to verify MCP server is working
3. **Use the `list_s3_buckets` tool** to list your buckets/spaces
4. **Check the response** - it will show which storage provider is detected

The server will automatically detect your storage provider based on the endpoint URL and display it in the results!
