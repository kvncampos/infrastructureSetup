import pytest

from ..web_server.app import app


@pytest.fixture
def client():
    """Fixture to provide a test client for the Flask app."""
    app.config["development"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test the index route for successful response and rendered content."""
    response = client.get("/")
    assert response.status_code == 200


def test_status_route(client):
    """Test the /status route for correct JSON response."""
    response = client.get("/status")
    assert response.status_code == 200
