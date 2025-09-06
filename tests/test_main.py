"""Tests for the main module."""

from mcp_s3_server.main import main


def test_main(capsys):
    """Test the main function."""
    main()
    captured = capsys.readouterr()
    assert "Hello from mcp-s3-server!" in captured.out
