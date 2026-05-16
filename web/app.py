from flask import Flask, render_template
import psycopg2
import os


app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'currencies_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'pass')


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


@app.route('/')
def index():
    """Главная страница: последние курсы валют из обоих источников."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Выбираем последние курсы по каждой валюте и источнику
    cur.execute("""
        SELECT source, currency, rate, fetched_date
        FROM currencies
        ORDER BY fetched_date DESC, source
        LIMIT 20;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', rows=rows)


@app.route('/pgadmin')
def pgadmin_redirect():
    """Просто ссылка на pgAdmin (маршрутизация через Nginx)."""
    return '<html><body><h1>pgAdmin</h1><p>Доступен через Nginx: <a href="/pgadmin/">перейти</a></p></body></html>'


@app.route('/metabase')
def metabase_redirect():
    """Ссылка на Metabase."""
    return '<html><body><h1>Metabase</h1><p>Доступен через Nginx: <a href="/metabase/">перейти</a></p></body></html>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)