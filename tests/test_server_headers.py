# tests/test_response_headers.py
import pytest
from fastapi.testclient import TestClient
from feed_aggregator.app import APIAppBuilder
from typing import Dict



HOST = "127.0.0.1"
PORT = 8000
ENDPOINT = "/v1/test"

@pytest.fixture(scope="session")
def client():
    """Create FastAPI app once for all tests"""
    app = APIAppBuilder.build_app()

    with TestClient(app) as test_client:
        yield test_client


def assert_security_headers_present(headers: Dict[str, str]) -> None:
    """
    Assert that all required security headers are present and have correct values.
    
    Args:
        headers: Response headers dictionary to check
    """
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["X-XSS-Protection"] == "1; mode=block"
    assert headers["Strict-Transport-Security"] == "max-age=31536000; includeSubDomains"


def test_successful_response_headers(client: TestClient):
    
    response = client.get(ENDPOINT)
    
    assert response.status_code == 200
    assert_security_headers_present(response.headers)

def test_resource_not_found_headers(client: TestClient):
    response = client.get("/non-existent-resource")  # Assuming this resource does not exist
    assert response.status_code == 404
    assert_security_headers_present(response.headers)

def test_not_allowed_request_headers(client: TestClient):
    response = client.post(ENDPOINT, json={})  # POST method not supported on ENDPOINT
    assert response.status_code == 405
    assert_security_headers_present(response.headers)
