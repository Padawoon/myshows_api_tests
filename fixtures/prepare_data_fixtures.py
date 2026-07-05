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
@pytest.fixture(scope='function')
def prepare_and_cleanup_test_data(request):
    inserted_rows = 0

    # Обрабатываем случай, когда атрибута request.param может не быть
    if not hasattr(request, 'param'):
        # Это старые тесты. Загружаем их привычный дефолтный пак данных
        filename = "test_data_for_insert.sql"
    else:
        filename = request.param

    with psycopg.connect(**DB_CONFIG) as conn:
        # Обрабатываем случай для 0 строк отдельно (если filename == None)
        if filename is not None:
            assert isinstance(filename, str)
            sql_script = load_sql_script(filename)

            with conn.cursor() as cur:
                cur.execute(sql_script)
                inserted_rows = cur.rowcount
                conn.commit()
        else:
            # Если filename это None, мы ничего не вставляем в базу
            inserted_rows = 0

        yield inserted_rows

        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE series RESTART IDENTITY CASCADE;")
            conn.commit()

# Фикстура для добавления одного сериала в таблицу там, где не нужно много
@pytest.fixture(scope='function')
def input_and_yield_one_show():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # Кидает в бд один сериал
            cur.execute(load_sql_script("test_one_show_insert.sql"))
            # Забирает из RETURNING айди сериала и кладёт его в show_id
            res = cur.fetchone()
            show_id = res[0]
            conn.commit()
        # Отдаём show_id
        yield show_id

        with conn.cursor() as cur:
            # Сносим этот добавленный сериал после теста
            cur.execute("DELETE FROM series WHERE id = %s;", (show_id,))
            conn.commit()