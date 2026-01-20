"""
Test suite for the Wikipedia Outline API.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_outline_endpoint_success():
    """Test fetching outline for a valid country."""
    response = client.get("/api/outline?country=India")
    assert response.status_code == 200
    assert "India" in response.text
    assert "#" in response.text  # Should contain markdown headings

def test_outline_endpoint_multiple_countries():
    """Test fetching outlines for multiple countries."""
    countries = ["Vanuatu", "Japan", "Canada"]
    for country in countries:
        response = client.get(f"/api/outline?country={country}")
        assert response.status_code == 200
        assert country in response.text

def test_outline_endpoint_missing_parameter():
    """Test error handling when country parameter is missing."""
    response = client.get("/api/outline")
    assert response.status_code == 422  # Validation error

def test_outline_endpoint_empty_parameter():
    """Test error handling when country parameter is empty."""
    response = client.get("/api/outline?country=")
    assert response.status_code == 400

def test_cors_headers():
    """Test that CORS headers are properly set."""
    response = client.get("/api/outline?country=India")
    assert "access-control-allow-origin" in response.headers