import aioboto3
from mcp_s3_server.config import S3Config

# Global S3 config
s3_config = S3Config.from_environment()


async def get_s3_session() -> aioboto3.Session:
    """Create S3 session with credentials from global config."""
    return aioboto3.Session(
        aws_access_key_id=s3_config.access_key_id,
        aws_secret_access_key=s3_config.secret_access_key,
        region_name=s3_config.region,
        aws_session_token=s3_config.session_token
    )
