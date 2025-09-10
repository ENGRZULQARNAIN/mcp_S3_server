from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class S3Config:
    """S3-compatible storage configuration settings."""
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    region: str = "us-east-1"
    session_token: Optional[str] = None
    endpoint_url: Optional[str] = None  # For S3-compatible services
    
    @classmethod
    def from_environment(cls) -> "S3Config":
        """Create S3 config from environment variables."""
        return cls(
            access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            session_token=os.getenv("AWS_SESSION_TOKEN"),
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),  # Custom endpoint for S3-compatible services
        )
    
    def is_configured(self) -> bool:
        """Check if basic S3 credentials are configured."""
        return bool(self.access_key_id and self.secret_access_key)
    
    def get_service_name(self) -> str:
        """Get the service name based on endpoint URL."""
        if not self.endpoint_url:
            return "AWS S3"
        elif "digitaloceanspaces.com" in self.endpoint_url:
            return "DigitalOcean Spaces"
        elif "cloud-object-storage.appdomain.cloud" in self.endpoint_url:
            return "IBM Cloud Object Storage"
        elif "amazonaws.com" not in self.endpoint_url:
            return "S3-Compatible Storage"
        else:
            return "AWS S3"
