def normalize(raw_data):
    """
    Принимает список словарей с данными из источников.
    Убирает записи с отсутствующими полями.
    Возвращает очищенный список.
    """
    cleaned = []
    for item in raw_data:
        if all(k in item for k in ('source', 'currency', 'rate', 'fetched_date')):
            cleaned.append(item)
    return cleaned
