import pytest
from fastapi.testclient import TestClient

from app.main import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
def client(app):
    return TestClient(app)