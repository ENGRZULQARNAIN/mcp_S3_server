"""Basic tests for mcp-s3-server package."""

import pytest
from mcp_s3_server.config import S3Config


def test_s3_config_creation():
    """Test S3Config can be created."""
    config = S3Config()
    assert config.region == "us-east-1"
    assert config.access_key_id is None
    assert config.secret_access_key is None


def test_s3_config_from_environment():
    """Test S3Config can be created from environment."""
    config = S3Config.from_environment()
    assert isinstance(config, S3Config)


def test_s3_config_service_name():
    """Test service name detection."""
    config = S3Config()
    assert config.get_service_name() == "AWS S3"
    
    config.endpoint_url = "https://nyc3.digitaloceanspaces.com"
    assert config.get_service_name() == "DigitalOcean Spaces"


def test_s3_config_configured():
    """Test configuration check."""
    config = S3Config()
    assert not config.is_configured()
    
    config.access_key_id = "test"
    config.secret_access_key = "test"
    assert config.is_configured()
