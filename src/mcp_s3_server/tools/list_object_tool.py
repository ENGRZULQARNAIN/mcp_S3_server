import sys
import logging
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


async def list_objects_tool(s3_config: S3Config, bucket_name: str, prefix: str = "", max_keys: int = 100) -> List[types.TextContent]:
    """
    List objects in a specific S3 bucket.
    
    Args:
        s3_config: S3 configuration
        bucket_name: Name of the bucket to list objects from
        prefix: Optional prefix to filter objects (default: "")
        max_keys: Maximum number of objects to return (default: 100)
    """
    try:
        # Check if S3 credentials are configured
        if not s3_config.is_configured():
            return [types.TextContent(
                type="text",
                text="❌ S3 credentials not configured!\n\nPlease set the following environment variables in your Claude Desktop config:\n• AWS_ACCESS_KEY_ID (your access key)\n• AWS_SECRET_ACCESS_KEY (your secret key)\n• AWS_DEFAULT_REGION (optional, defaults to us-east-1)\n• S3_ENDPOINT_URL (optional, for S3-compatible services like DigitalOcean Spaces)\n\nExamples:\n• AWS S3: Leave S3_ENDPOINT_URL empty\n• DigitalOcean Spaces: S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com\n• IBM Cloud: S3_ENDPOINT_URL=https://s3.us-south.cloud-object-storage.appdomain.cloud"
            )]

        service_name = s3_config.get_service_name()
        logger.info(f"Attempting to list objects from bucket '{bucket_name}' in {service_name}...")
        logger.info(f"Using endpoint: {s3_config.endpoint_url or 'AWS S3 default'}")
        logger.info(f"Using region: {s3_config.region}")
        logger.info(f"Prefix filter: '{prefix}' (empty means all objects)")
        logger.info(f"Max objects: {max_keys}")
        
        session = await get_s3_session()
        
        # Create S3 client with custom endpoint if specified
        client_kwargs = {}
        if s3_config.endpoint_url:
            client_kwargs['endpoint_url'] = s3_config.endpoint_url
            logger.info(f"Using custom endpoint: {s3_config.endpoint_url}")
        
        async with session.client('s3', **client_kwargs) as s3_client:
            logger.info("S3 client created, calling list_objects_v2...")
            
            # Prepare list_objects_v2 parameters
            list_params = {
                'Bucket': bucket_name,
                'MaxKeys': min(max_keys, 1000)  # AWS limit is 1000
            }
            if prefix:
                list_params['Prefix'] = prefix
            
            response = await s3_client.list_objects_v2(**list_params)
            
            objects = response.get('Contents', [])
            logger.info(f"Found {len(objects)} objects")
            
            if not objects:
                prefix_msg = f" with prefix '{prefix}'" if prefix else ""
                return [types.TextContent(
                    type="text",
                    text=f"📁 No objects found in bucket '{bucket_name}'{prefix_msg}.\n\nThis could mean:\n• The bucket is empty\n• No objects match the prefix filter\n• Your credentials don't have ListBucket permission for this bucket\n• The bucket doesn't exist or you're connected to the wrong region/endpoint"
                )]
            
            # Format object information
            object_list = [f"📁 **Found {len(objects)} object(s) in bucket '{bucket_name}':**\n"]
            
            for i, obj in enumerate(objects, 1):
                key = obj['Key']
                size = obj['Size']
                last_modified = obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S UTC')
                
                # Format size in human-readable format
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                elif size < 1024 * 1024 * 1024:
                    size_str = f"{size / (1024 * 1024):.1f} MB"
                else:
                    size_str = f"{size / (1024 * 1024 * 1024):.1f} GB"
                
                object_list.append(f"{i}. **{key}**")
                object_list.append(f"   Size: {size_str}")
                object_list.append(f"   Modified: {last_modified}")
                object_list.append("")  # Empty line for spacing
            
            # Add pagination info if there are more objects
            if response.get('IsTruncated', False):
                object_list.append(f"⚠️  **Note:** Results are truncated. There may be more objects in this bucket.")
                object_list.append(f"   Use a more specific prefix or increase max_keys to see more results.")
            
            result_text = "\n".join(object_list)
            
            return [types.TextContent(
                type="text",
                text=result_text
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
        elif error_code == 'AccessDenied':
            return [types.TextContent(
                type="text",
                text=f"❌ Access denied to bucket '{bucket_name}'!\n\nPlease check that your credentials have the 'ListBucket' permission for this bucket in {s3_config.get_service_name()}."
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
    
    except Exception as e:
        logger.error(f"Unexpected error listing S3 objects: {e}", exc_info=True)
        return [types.TextContent(
            type="text",
            text=f"❌ Unexpected error: {str(e)}\n\nPlease check the server logs for more details."
        )]
