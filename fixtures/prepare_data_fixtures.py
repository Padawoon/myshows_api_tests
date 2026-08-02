import allure
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
    "host": os.getenv("DB_HOST"),
    "port": "5432"
}


@allure.title("Наполнение БД тестовыми данными")
@pytest.fixture(scope='function')
def prepare_and_cleanup_test_data(request):
    inserted_rows = 0

    with allure.step("Определение файла с тестовыми данными"):
        if not hasattr(request, 'param'):
            filename = "test_data_for_insert.sql"
            allure.attach("Параметр отсутствует. Используем дефолтный файл.", name="Инфо")
        else:
            filename = request.param

        allure.attach(f"Выбранный файл: {filename}", name="Целевой SQL-скрипт")

    with psycopg.connect(**DB_CONFIG) as conn:
        with allure.step("Применение SQL-скрипта к базе данных"):
            if filename is not None:
                assert isinstance(filename, str)
                sql_script = load_sql_script(filename)

                with conn.cursor() as cur:
                    cur.execute(sql_script)
                    inserted_rows = cur.rowcount
                    conn.commit()

                allure.attach(str(inserted_rows), name="Успешно вставлено строк")
            else:
                allure.attach("Файл пустой (None). Пропускаем вставку.", name="Инфо")
                inserted_rows = 0

        yield inserted_rows

        with allure.step("Очистка базы данных (Teardown)"):
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE series RESTART IDENTITY CASCADE;")
                conn.commit()
            allure.attach("Таблица series успешно очищена (TRUNCATE)", name="Результат очистки")


@allure.title("Наполнение БД одним сериалом")
@pytest.fixture(scope='function')
def input_and_yield_one_show():
    with psycopg.connect(**DB_CONFIG) as conn:
        with allure.step("Добавление тестового сериала в БД"):
            with conn.cursor() as cur:
                cur.execute(load_sql_script("test_one_show_insert.sql"))
                # Забирает из RETURNING айди сериала и кладёт его в show_id
                res = cur.fetchone()
                show_id = res[0]
                conn.commit()

            # Прикрепляет ID к отчету
            allure.attach(str(show_id), name="Создан сериал с ID")

        # Отдаём show_id в тест
        yield show_id

        # Очистка после выполнения теста (Teardown)
        with allure.step(f"Удаление тестового сериала с ID {show_id}"):
            with conn.cursor() as cur:
                cur.execute("DELETE FROM series WHERE id = %s;", (show_id,))
                conn.commit()