import requests

def test_backend_root():
    # Simple smoke test for backend root endpoint
    response = requests.get('http://localhost:8000/')
    assert response.status_code == 200
