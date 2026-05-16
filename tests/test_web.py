import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'web'))

def test_import_app():
    import app as app_module          # импортируем модуль app
    assert app_module.app is not None, "Flask app not found"
    # проверяем, что отвечает на главной странице
    with app_module.app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200