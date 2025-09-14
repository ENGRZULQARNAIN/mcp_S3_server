 # MCP S3 Server

[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/engrzulqarnain-mcp-server-s3-download-files-badge.png)](https://mseep.ai/app/engrzulqarnain-mcp-server-s3-download-files)

A Model Context Protocol (MCP) server for S3-compatible storage services. Enables AI models to securely interact with AWS S3, DigitalOcean Spaces, IBM Cloud Object Storage, and other S3-compatible services.

## 🚀 Features

- **List S3 Buckets**: Retrieve all accessible buckets with creation dates
- **List Objects**: Browse objects in specific buckets with prefix filtering
- **Download Files**: Download files from S3 storage directly to local Downloads folder
- **Multi-Provider Support**: Works with AWS S3, DigitalOcean Spaces, IBM Cloud, MinIO, Wasabi, Backblaze B2
- **Secure Integration**: Standardized interface for AI models to access cloud storage
- **Prefix Filtering**: Navigate folder-like structures with prefix parameters
- **Comprehensive Error Handling**: Clear error messages for common issues

## 📦 Installation

### Using uv (Recommended)

```bash
# Install globally
uv tool install mcp-s3-server

# Or run directly without installing
uvx mcp-s3-server
```

### Using pip

```bash
pip install mcp-s3-server
```

### Development Installation

```bash
git clone https://github.com/ENGRZULQARNAIN/mcp_s3_server.git
cd mcp_s3_server
uv pip install -e .
```

## ⚙️ Configuration

### Claude Desktop Setup

Add this to your `claude_desktop_config.json`:

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

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | ✅ | Your access key | `YOUR_ACCESS_KEY_HERE` |
| `AWS_SECRET_ACCESS_KEY` | ✅ | Your secret key | `YOUR_SECRET_KEY_HERE` |
| `AWS_DEFAULT_REGION` | ⚠️ | Region (default: us-east-1) | `nyc3` |
| `S3_ENDPOINT_URL` | ⚠️ | Custom endpoint for S3-compatible services | `https://nyc3.digitaloceanspaces.com` |

## 🛠️ Available Tools

### 1. test_connection
Test MCP S3 server connection.

**Parameters:** None

**Example:**
```json
{
  "tool": "test_connection",
  "parameters": {}
}
```

### 2. list_s3_buckets
List all accessible S3 buckets with creation dates.

**Parameters:** None

**Example:**
```json
{
  "tool": "list_s3_buckets",
  "parameters": {}
}
```

### 3. list_s3_objects
List objects in a specific S3 bucket with optional filtering.

**Parameters:**
- `bucket_name` (required): Name of the S3 bucket
- `prefix` (optional): Filter objects by prefix (e.g., "folder/subfolder/")
- `max_keys` (optional): Maximum objects to return (default: 100, max: 1000)

**Examples:**
```json
// List all objects in a bucket
{
  "tool": "list_s3_objects",
  "parameters": {
    "bucket_name": "my-bucket"
  }
}

// List objects in a specific folder
{
  "tool": "list_s3_objects",
  "parameters": {
    "bucket_name": "my-bucket",
    "prefix": "documents/",
    "max_keys": 50
  }
}
```

### 4. download_s3_file
Download a file from S3 storage to the local Downloads folder.

**Parameters:**
- `bucket_name` (required): Name of the S3 bucket containing the file
- `object_key` (required): Key/path of the object in the bucket (e.g., "folder/file.pdf")
- `local_filename` (optional): Custom filename for the downloaded file (defaults to object key basename)

**Examples:**
```json
// Download a file with default filename
{
  "tool": "download_s3_file",
  "parameters": {
    "bucket_name": "my-bucket",
    "object_key": "documents/report.pdf"
  }
}

// Download a file with custom filename
{
  "tool": "download_s3_file",
  "parameters": {
    "bucket_name": "my-bucket",
    "object_key": "documents/report.pdf",
    "local_filename": "monthly_report.pdf"
  }
}
```

## 🌐 S3-Compatible Storage Providers

### AWS S3 (Default)
```json
{
  "env": {
    "AWS_ACCESS_KEY_ID": "your_aws_access_key",
    "AWS_SECRET_ACCESS_KEY": "your_aws_secret_key",
    "AWS_DEFAULT_REGION": "us-east-1"
  }
}
```

### DigitalOcean Spaces
```json
{
  "env": {
    "AWS_ACCESS_KEY_ID": "your_do_spaces_key",
    "AWS_SECRET_ACCESS_KEY": "your_do_spaces_secret",
    "AWS_DEFAULT_REGION": "nyc3",
    "S3_ENDPOINT_URL": "https://nyc3.digitaloceanspaces.com"
  }
}
```

### IBM Cloud Object Storage
```json
{
  "env": {
    "AWS_ACCESS_KEY_ID": "your_ibm_access_key",
    "AWS_SECRET_ACCESS_KEY": "your_ibm_secret_key",
    "AWS_DEFAULT_REGION": "us-south",
    "S3_ENDPOINT_URL": "https://s3.us-south.cloud-object-storage.appdomain.cloud"
  }
}
```

### MinIO (Self-hosted)
```json
{
  "env": {
    "AWS_ACCESS_KEY_ID": "your_minio_access_key",
    "AWS_SECRET_ACCESS_KEY": "your_minio_secret_key",
    "AWS_DEFAULT_REGION": "us-east-1",
    "S3_ENDPOINT_URL": "http://localhost:9000"
  }
}
```

### Wasabi Cloud Storage
```json
{
  "env": {
    "AWS_ACCESS_KEY_ID": "your_wasabi_access_key",
    "AWS_SECRET_ACCESS_KEY": "your_wasabi_secret_key",
    "AWS_DEFAULT_REGION": "us-east-1",
    "S3_ENDPOINT_URL": "https://s3.wasabisys.com"
  }
}
```

### Backblaze B2
```json
{
  "env": {
    "AWS_ACCESS_KEY_ID": "your_b2_key_id",
    "AWS_SECRET_ACCESS_KEY": "your_b2_application_key",
    "AWS_DEFAULT_REGION": "us-west-002",
    "S3_ENDPOINT_URL": "https://s3.us-west-002.backblazeb2.com"
  }
}
```

## 🔍 Testing Your Setup

### 1. Test Server Connection
```bash
# Set environment variables
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key_here"
export AWS_DEFAULT_REGION="us-east-1"
export S3_ENDPOINT_URL="https://nyc3.digitaloceanspaces.com"

# Run the server
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

## 🔐 Security Best Practices

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

## 🐛 Troubleshooting

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

4. **"spawn uvx ENOENT" (macOS/Linux)**
   - Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Restart terminal and try again

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
uvx mcp-s3-server
```

## 📋 Prerequisites

- Python 3.10 or higher
- Configured S3-compatible storage credentials
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip
- Familiarity with the [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)

## 🎯 Use Cases

- **Data Analysis**: Access and analyze data stored in S3 buckets for AI-driven applications
- **Document Retrieval**: Retrieve and download specific files (e.g., PDFs) for processing by AI models
- **File Management**: Download files from cloud storage directly to local machine for offline access
- **Automation**: Automate S3 bucket management tasks via natural language queries with LLMs
- **AI Development**: Support development of AI models requiring access to external data sources
- **Content Distribution**: Download files from cloud storage for local processing or distribution

## 🤝 Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on submitting issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/ENGRZULQARNAIN/mcp_s3_server)
- [PyPI Package](https://pypi.org/project/mcp-s3-server/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop Configuration Guide](https://docs.anthropic.com/claude/desktop/configure)
