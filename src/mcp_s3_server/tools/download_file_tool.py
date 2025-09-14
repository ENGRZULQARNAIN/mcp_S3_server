import sys
import logging
import os
from pathlib import Path
from typing import List

# Initialize logger before any use
logger = logging.getLogger(__name__)

try:
    from mcp import types
    import aioboto3
    from botocore.exceptions import ClientError, NoCredentialsError
    logger.info("MCP and AWS imports successful")
except ImportError as e:
    logger.error(f"Import failed: {e}")
    sys.exit(1)

from mcp_s3_server.config import S3Config
from mcp_s3_server.utils.utils import get_s3_session


async def download_file_tool(s3_config: S3Config, bucket_name: str, object_key: str, local_filename: str = None) -> List[types.TextContent]:
    """
    Download a file from S3 storage to the local downloads folder.
    
    Args:
        s3_config: S3 configuration
        bucket_name: Name of the S3 bucket
        object_key: Key/path of the object in the bucket
        local_filename: Optional custom filename (defaults to object key basename)
    """
    try:
        # Check if S3 credentials are configured
        if not s3_config.is_configured():
            return [types.TextContent(
                type="text",
                text="❌ S3 credentials not configured!\n\nPlease set the following environment variables in your Claude Desktop config:\n• AWS_ACCESS_KEY_ID (your access key)\n• AWS_SECRET_ACCESS_KEY (your secret key)\n• AWS_DEFAULT_REGION (optional, defaults to us-east-1)\n• S3_ENDPOINT_URL (optional, for S3-compatible services like DigitalOcean Spaces)\n\nExamples:\n• AWS S3: Leave S3_ENDPOINT_URL empty\n• DigitalOcean Spaces: S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com\n• IBM Cloud: S3_ENDPOINT_URL=https://s3.us-south.cloud-object-storage.appdomain.cloud"
            )]

        service_name = s3_config.get_service_name()
        logger.info(f"Attempting to download '{object_key}' from bucket '{bucket_name}' in {service_name}...")
        logger.info(f"Using endpoint: {s3_config.endpoint_url or 'AWS S3 default'}")
        logger.info(f"Using region: {s3_config.region}")
        
        # Determine local filename
        if not local_filename:
            local_filename = os.path.basename(object_key)
            if not local_filename:
                local_filename = "downloaded_file"
        
        # Get downloads folder path
        downloads_folder = get_downloads_folder()
        local_file_path = os.path.join(downloads_folder, local_filename)
        
        # Ensure downloads folder exists
        os.makedirs(downloads_folder, exist_ok=True)
        
        logger.info(f"Downloading to: {local_file_path}")
        
        session = await get_s3_session()
        
        # Create S3 client with custom endpoint if specified
        client_kwargs = {}
        if s3_config.endpoint_url:
            client_kwargs['endpoint_url'] = s3_config.endpoint_url
            logger.info(f"Using custom endpoint: {s3_config.endpoint_url}")
        
        async with session.client('s3', **client_kwargs) as s3_client:
            logger.info("S3 client created, calling download_file...")
            
            # Download the file
            await s3_client.download_file(bucket_name, object_key, local_file_path)
            
            # Get file size for confirmation
            file_size = os.path.getsize(local_file_path)
            
            # Format file size in human-readable format
            if file_size < 1024:
                size_str = f"{file_size} B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            elif file_size < 1024 * 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            else:
                size_str = f"{file_size / (1024 * 1024 * 1024):.1f} GB"
            
            logger.info(f"Successfully downloaded {size_str} file")
            
            return [types.TextContent(
                type="text",
                text=f"✅ **File downloaded successfully!**\n\n"
                     f"📁 **Source:** `{bucket_name}/{object_key}`\n"
                     f"💾 **Destination:** `{local_file_path}`\n"
                     f"📊 **Size:** {size_str}\n"
                     f"🌐 **Storage:** {service_name}\n\n"
                     f"The file has been saved to your Downloads folder and is ready to use."
            )]
            
    except NoCredentialsError:
        logger.error("S3 credentials not found")
        return [types.TextContent(
            type="text",
            text="❌ S3 credentials not found!\n\nPlease configure your credentials:\n1. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in Claude Desktop config\n2. For S3-compatible services, also set S3_ENDPOINT_URL\n3. Or configure ~/.aws/credentials (for AWS S3 only)"
        )]
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        logger.error(f"AWS ClientError: {error_code} - {error_message}")
        
        if error_code == 'NoSuchBucket':
            return [types.TextContent(
                type="text",
                text=f"❌ Bucket '{bucket_name}' not found!\n\nPlease check:\n• The bucket name is correct\n• The bucket exists in the specified region\n• You're connected to the correct endpoint for {s3_config.get_service_name()}"
            )]
        elif error_code == 'NoSuchKey':
            return [types.TextContent(
                type="text",
                text=f"❌ Object '{object_key}' not found in bucket '{bucket_name}'!\n\nPlease check:\n• The object key/path is correct\n• The file exists in the bucket\n• You have the correct permissions to access this object"
            )]
        elif error_code == 'AccessDenied':
            return [types.TextContent(
                type="text",
                text=f"❌ Access denied to '{bucket_name}/{object_key}'!\n\nPlease check that your credentials have the 'GetObject' permission for this object in {s3_config.get_service_name()}."
            )]
        elif error_code in ['InvalidAccessKeyId', 'SignatureDoesNotMatch']:
            return [types.TextContent(
                type="text",
                text=f"❌ Invalid credentials: {error_message}\n\nPlease check your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for {s3_config.get_service_name()}."
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ {s3_config.get_service_name()} Error ({error_code}): {error_message}\n\nPlease check your configuration and try again."
            )]
    
    except PermissionError as e:
        logger.error(f"Permission error writing to downloads folder: {e}")
        return [types.TextContent(
            type="text",
            text=f"❌ Permission denied writing to Downloads folder!\n\nPlease check:\n• You have write permissions to the Downloads folder\n• The Downloads folder is not read-only\n• No other application is using the file\n\nError: {str(e)}"
        )]
    
    except OSError as e:
        logger.error(f"OS error during download: {e}")
        return [types.TextContent(
            type="text",
            text=f"❌ File system error during download!\n\nPlease check:\n• There's enough disk space available\n• The Downloads folder path is valid\n• You have proper file system permissions\n\nError: {str(e)}"
        )]
    
    except Exception as e:
        logger.error(f"Unexpected error downloading file: {e}", exc_info=True)
        return [types.TextContent(
            type="text",
            text=f"❌ Unexpected error: {str(e)}\n\nPlease check the server logs for more details."
        )]


def get_downloads_folder() -> str:
    """
    Get the Downloads folder path for the current platform.
    
    Returns:
        str: Path to the Downloads folder
    """
    home = Path.home()
    
    # Platform-specific Downloads folder paths
    if sys.platform == "win32":
        # Windows
        downloads = home / "Downloads"
    elif sys.platform == "darwin":
        # macOS
        downloads = home / "Downloads"
    else:
        # Linux and other Unix-like systems
        downloads = home / "Downloads"
    
    return str(downloads)
