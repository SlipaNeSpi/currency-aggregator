CREATE TABLE IF NOT EXISTS currencies (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    rate DECIMAL(12,4) NOT NULL,
    fetched_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, currency, fetched_date)  -- предотвращает дубликаты
);