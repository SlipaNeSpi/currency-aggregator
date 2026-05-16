import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'parser'))

def test_import_parser():
    try:
        from parser import fetch_cbr_rates, fetch_tinkoff_rates
        assert callable(fetch_cbr_rates)
        assert callable(fetch_tinkoff_rates)
        print("Parser imports OK")
    except Exception as e:
        print(f"Parser import failed: {e}")
        raise

def test_import_normalizer():
    from normalizer import normalize
    data = [{'source': 'test', 'currency': 'USD', 'rate': 10.0, 'fetched_date': '2026-01-01'}]
    cleaned = normalize(data)
    assert len(cleaned) == 1

def test_import_db():
    # без реального подключения к БД просто проверяем наличие функции
    from db import insert_rates
    assert callable(insert_rates)