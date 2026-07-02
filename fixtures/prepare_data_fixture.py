import pytest
import psycopg
import os
from dotenv import load_dotenv
from helpers.file_helpers import load_sql_script

load_dotenv()

DB_CONFIG = {
    "dbname": "my-shows-rating",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": "5432"
}

# Фикстурка, которая заполнит бд и снесёт таблицу после выполнения теста
@pytest.fixture(scope='session')
def prepare_and_cleanup_test_data():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # Заполняет пустую таблицу
            cur.execute(load_sql_script("test_data_for_insert.sql"))
            conn.commit()

        yield

        # Очищает таблицу перед закрытием соединения
        with conn.cursor() as cur:
            # Транкейт и рестарт автоинкрементатора с каскадным удалением
            # Оно тут не нужно, но пусть будет если мы решим ещё таблицу с сериями накинуть, где у нас ФК будут
            cur.execute("TRUNCATE TABLE series RESTART IDENTITY CASCADE;")
            conn.commit()