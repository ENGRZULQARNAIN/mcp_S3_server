[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/engrzulqarnain-mcp-server-s3-download-files-badge.png)](https://mseep.ai/app/engrzulqarnain-mcp-server-s3-download-files)

## Model Context Protocol (MCP) Server for AWS S3

This repository provides an implementation of a Model Context Protocol (MCP) server for AWS S3, enabling AI models, particularly Large Language Models (LLMs), to securely interact with S3 buckets. The server offers a standardized interface to list S3 buckets, list objects within buckets, and download file contents. It facilitates seamless integration between AI applications and AWS S3 storage for efficient data retrieval and management.

### Key Features
- **List S3 Buckets**: Retrieve a list of available buckets in an AWS account.
- **List Objects**: Display objects within a specified bucket.
- **File Download**: Fetch the contents of specific objects, such as documents or other files.
- **Secure Interaction**: Provides a standardized, secure interface for AI models to interact with S3.
- **MCP Ecosystem**: Part of the Model Context Protocol ecosystem, supporting AI model integration with various data sources.

### Use Cases
- **Data Analysis**: Access and analyze data stored in S3 buckets for AI-driven applications.
- **Document Retrieval**: Retrieve specific files (e.g., PDFs) for processing by AI models.
- **Automation**: Automate S3 bucket management tasks via natural language queries with LLMs.
- **AI Development**: Support development of AI models requiring access to external data sources.

### Prerequisites
To use this server, developers need:
- Python 3.10 or higher
- Configured AWS credentials (Access Key ID, Secret Access Key, and Region)
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip
- Familiarity with the [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) for AI application integration

### Limitations
Some implementations may:
- Support only specific file types (e.g., PDFs in certain versions).
- Have limits on the number of retrieved objects (e.g., up to 1000 objects).
- Require specific configurations, such as the maximum number of buckets to return.

### Installation and Usage

#### Option 1: Install from PyPI (Recommended)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh  # Unix/macOS
# or for Windows: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install the MCP S3 server
uv add mcp-s3-server

# Or using pip
pip install mcp-s3-server
```

#### Option 2: Development Installation
```bash
# Clone the repository
git clone https://github.com/ENGRZULQARNAIN/mcp_s3_server.git
cd mcp_s3_server

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

#### Configuration and Usage
1. **Configure AWS credentials** using one of these methods:
   - AWS credentials file (`~/.aws/credentials`)
   - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`)
   - IAM roles (for EC2 instances)

2. **Start the server**:
   ```bash
   mcp-s3-server
   ```

3. **Integrate with an AI model** or application using the MCP interface.

Refer to the repository's documentation for detailed setup instructions and API usage.

### Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on submitting issues, feature requests, or pull requests.

### License
This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.
