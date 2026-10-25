import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app(database_uri="sqlite:///:memory:")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_upload_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_predict_no_file(client):
    response = client.post("/predict")
    assert response.status_code == 400
