import pytest
import allure
from http import HTTPStatus
from config.api_config import BASE_URL
from data.api_endpoints import SERIES
from helpers.file_helpers import load_schema
from jsonschema import validate
from pytest_check import check
from deepdiff import DeepDiff

@allure.suite("API MyShows/Series: Получение сериалов")
@pytest.mark.usefixtures("prepare_and_cleanup_test_data")
class TestGetSeries:
    @allure.title("Успешное получение списка сериалов")
    @pytest.mark.positive
    def test_get_all_series_success(self, api_client):
        with allure.step("Отправка GET-запроса на получение списка сериалов"):
            response = api_client.get(f"{BASE_URL}{SERIES}")

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK
            response_body = response.json()

        with allure.step("Валидация ответа по схеме"):
            template = load_schema("series.yml")
            validate(instance=response_body, schema=template)

    @allure.title("Успешное получение списка сериалов с указанным рейтингом")
    @pytest.mark.positive
    def test_get_series_with_rating_success(self, api_client):
        with allure.step("Отправка GET-запроса на получение списка сериалов"):
            response = api_client.get(
                f"{BASE_URL}{SERIES}",
            params=({"rating": 7}))
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("Сверка результата с ожидаемым ответом"):
            response_body = response.json()
            expected_response = [
                {
                    'id': 5,
                    'name': 'Паук-Нуар',
                    'photo': 'https://avatars.mds.yandex.net/get-kinopoisk-image/10893610/3fba8635-74c6-49ba-84f3-761af8d4ae25/300x450',
                    'rating': 7,
                    'status': 'watched',
                    'review': 'Нью-Йорк, 1930-е. Частный детектив Бен Райлли, который переживает не лучшие времена, сталкивается со своим прошлым. Бену, единственному супергерою в городе, приходится бороться с внутренними демонами и снова стать Человеком-пауком, чтобы спасти мегаполис и себя.'
                }

            ]
            compare = DeepDiff(expected_response, response_body, ignore_order=True)
            assert not compare, compare

    @allure.title("Успешное получение списка сериалов, отфильтрованных по статусу")
    @pytest.mark.positive
    def test_get_series_filter_by_status_success(self, api_client):
        with allure.step("Отправка GET-запроса на получение списка сериалов с фильтрацией по статусу"):
            response = api_client.get(
                f"{BASE_URL}{SERIES}",
                params={"status": "watched"}
            )
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK
            response_body = response.json()

        expected_response = [
            {
                'id': 4,
                'name': 'Черные паруса',
                'photo': 'https://avatars.mds.yandex.net/get-kinopoisk-image/1629390/8d80273e-30df-4a07-95c9-8c7c75a49f72/300x450',
                'rating': 9,
                'status': 'watched',
                'review': 'У клада на Острове сокровищ есть своя предыстория. Пиратская сага о капитане Флинте и молодом Джоне Сильвере'
            },
            {
                'id': 5,
                'name': 'Паук-Нуар',
                'photo': 'https://avatars.mds.yandex.net/get-kinopoisk-image/10893610/3fba8635-74c6-49ba-84f3-761af8d4ae25/300x450',
                'rating': 7,
                'status': 'watched',
                'review': 'Нью-Йорк, 1930-е. Частный детектив Бен Райлли, который переживает не лучшие времена, сталкивается со своим прошлым. Бену, единственному супергерою в городе, приходится бороться с внутренними демонами и снова стать Человеком-пауком, чтобы спасти мегаполис и себя.'
            }
        ]

        with allure.step("Сверка результата с ожидаемым ответом"):
            compare = DeepDiff(expected_response, response_body, ignore_order=True)
            assert not compare, compare

    @allure.title("Успешное получение списка сериалов, отсортированных по рейтингу по возрастанию")
    @pytest.mark.positive
    def test_get_series_sort_by_rating_asc_success(self, api_client):
        with allure.step("Отправка GET-запроса на получение списка сериалов с сортировкой по рейтингу (возрастание)"):
            response = api_client.get(
                f"{BASE_URL}{SERIES}",
                params={"sort": "rating_asc"}
            )
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK
            response_body = response.json()
        with allure.step("Проверка корректности сортировки по рейтингу"):
            actual_ratings = [series["rating"] for series in response_body]
            expected_ratings = [6, 7, 8, 8, 9]
            assert actual_ratings == expected_ratings

    @allure.title("Успешное получение списка сериалов в диапазоне рейтингов")
    @pytest.mark.positive
    def test_get_series_by_rating_range_success(self, api_client):
        with allure.step("Отправка GET-запроса на получение списка сериалов с фильтрацией по диапазону рейтинга"):
            response = api_client.get(
                f"{BASE_URL}{SERIES}",
                params={"rating_range": "gt4_lt8"}
            )
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK
            response_body = response.json()
        with allure.step("Проверка соответствия полученных сериалов ожидаемому диапазону"):
            actual_names = [series["name"] for series in response_body]
            expected_names = ['Извне', 'Паук-Нуар']
            compare = DeepDiff(expected_names, actual_names, ignore_order=True)
            assert not compare, compare

    @allure.title("Проверка количества полученных сериалов в зависимости от объема тестовых данных")
    @pytest.mark.parametrize(
        "prepare_and_cleanup_test_data",
        [
            None,  # Кейс для 0 строк (в фикстуру уйдет None)
            "test_one_show_insert.sql",  # Кейс для 1 строки
            "test_three_shows_insert.sql"  # Кейс для 3 строк
        ],
        indirect=True,
        ids=["zero_rows", "one_row", "three_rows"]
    )
    def test_get_series_count(self, api_client, prepare_and_cleanup_test_data):
        with allure.step("Получение ожидаемого количества сериалов"):
            expected_count = prepare_and_cleanup_test_data

        with allure.step("Отправка GET-запроса на получение списка сериалов"):
            response = api_client.get(f"{BASE_URL}{SERIES}")

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("Проверка соответствия количества сериалов ожидаемому"):
            response_body = response.json()
            assert len(response_body) == expected_count

        with allure.step("Валидация ответа по схеме"):
            template = load_schema("series.yml")
            validate(instance=response_body, schema=template)

    @allure.title("Запрос несуществующего эндпоинта")
    @pytest.mark.negative
    def test_get_series_not_found_endpoint(self, api_client):
        with allure.step("Отправка GET-запроса на несуществующий эндпоинт"):
            invalid_endpoint = f"{BASE_URL}/api/v1/some_fake_endpoint_999"
            response = api_client.get(invalid_endpoint)
        with allure.step("Проверка статус-кода ответа (404 Not Found)"):
            assert response.status_code == HTTPStatus.NOT_FOUND

    @allure.title("Запрос с некорректным значением query-параметра status")
    @pytest.mark.negative
    def test_get_series_invalid_query_params(self, api_client):
        with allure.step("Отправка GET-запроса с некорректным значением статуса"):
            response = api_client.get(
                f"{BASE_URL}{SERIES}",
            params={"status": "invalid_status"})
        with allure.step("Проверка статус-кода ответа (400 Bad Request)"):
            assert response.status_code == HTTPStatus.BAD_REQUEST
            response_body = response.json()
        with allure.step("Проверка сообщения об ошибке валидации"):
            check.equal(response_body.get("error"), "validation error")

            expected_message = "Input should be 'watching', 'watched' or 'will_watch'"
            with check:
                error_detail = response_body.get("detail", [])
                assert expected_message == error_detail[0]["msg"]