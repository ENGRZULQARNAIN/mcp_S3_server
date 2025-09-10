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

from src.mcp_s3_server.config import S3Config
from src.mcp_s3_server.utils.utils import get_s3_session

async def list_buckets_tool(s3_config: S3Config) -> List[types.TextContent]:
    try:
        # Check if S3 credentials are configured
        if not s3_config.is_configured():
            return [types.TextContent(
                type="text",
                text="❌ S3 credentials not configured!\n\nPlease set the following environment variables in your Claude Desktop config:\n• AWS_ACCESS_KEY_ID (your access key)\n• AWS_SECRET_ACCESS_KEY (your secret key)\n• AWS_DEFAULT_REGION (optional, defaults to us-east-1)\n• S3_ENDPOINT_URL (optional, for S3-compatible services like DigitalOcean Spaces)\n\nExamples:\n• AWS S3: Leave S3_ENDPOINT_URL empty\n• DigitalOcean Spaces: S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com\n• IBM Cloud: S3_ENDPOINT_URL=https://s3.us-south.cloud-object-storage.appdomain.cloud"
            )]

        service_name = s3_config.get_service_name()
        logger.info(f"Attempting to list buckets from {service_name}...")
        logger.info(f"Using endpoint: {s3_config.endpoint_url or 'AWS S3 default'}")
        logger.info(f"Using region: {s3_config.region}")
        logger.info(f"Access key ID: {s3_config.access_key_id[:8]}...")
        session = await get_s3_session()

        # Create S3 client with custom endpoint if specified
        client_kwargs = {}
        if s3_config.endpoint_url:
            client_kwargs['endpoint_url'] = s3_config.endpoint_url
            logger.info(f"Using custom endpoint: {s3_config.endpoint_url}")

        async with session.client('s3', **client_kwargs) as s3_client:
            logger.info("S3 client created, calling list_buckets...")
            response = await s3_client.list_buckets()

            buckets = response.get('Buckets', [])
            logger.info(f"Found {len(buckets)} buckets")

            if not buckets:
                return [types.TextContent(
                    type="text",
                    text=f"📦 No buckets found in your {service_name} account.\n\nThis could mean:\n• Your account has no buckets\n• Your credentials don't have ListBuckets permission\n• You're connected to the wrong region or endpoint"
                )]

            # Format bucket information
            bucket_list = [f"📦 **Found {len(buckets)} bucket(s) in {service_name}:**\n"]

            for i, bucket in enumerate(buckets, 1):
                name = bucket['Name']
                creation_date = bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S UTC')
                bucket_list.append(f"{i}. **{name}**")
                bucket_list.append(f"   Created: {creation_date}")
                bucket_list.append("")

            result_text = "\n".join(bucket_list)

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

        if error_code == 'AccessDenied':
            return [types.TextContent(
                type="text",
                text=f"❌ Access denied: {error_message}\n\nPlease check that your credentials have the 'ListBuckets' permission for {s3_config.get_service_name()}."
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
        logger.error(f"Unexpected error listing S3 buckets: {e}", exc_info=True)
        return [types.TextContent(
            type="text",
            text=f"❌ Unexpected error: {str(e)}\n\nPlease check the server logs for more details."
        )]