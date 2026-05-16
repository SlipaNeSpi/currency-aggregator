import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'web'))

def test_import_app():
    from app import app
    assert app is not None
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200