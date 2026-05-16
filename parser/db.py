import psycopg2
import os

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'currencies_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'pass')


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


def insert_rates(data):
    """Вставляет записи в таблицу currencies, пропуская дубликаты."""
    if not data:
        print("Нет данных для вставки.")
        return
    conn = get_connection()
    cur = conn.cursor()
    insert_query = """
    INSERT INTO currencies (source, currency, rate, fetched_date)
    VALUES (%(source)s, %(currency)s, %(rate)s, %(fetched_date)s)
    ON CONFLICT (source, currency, fetched_date) DO NOTHING;
    """
    try:
        cur.executemany(insert_query, data)
        conn.commit()
        print(f"Вставлено записей: {cur.rowcount}")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при вставке данных: {e}")
    finally:
        cur.close()
        conn.close()
