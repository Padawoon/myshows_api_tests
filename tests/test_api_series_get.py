import pytest
from http import HTTPStatus
from config.api_config import BASE_URL
from data.api_endpoints import SERIES
from helpers.file_helpers import load_schema
from jsonschema import validate
from pytest_check import check
from deepdiff import DeepDiff

@pytest.mark.usefixtures("prepare_and_cleanup_test_data")
class TestGetSeries:
    @pytest.mark.positive
    def test_get_all_series_success(self, api_client):
        response = api_client.get(f"{BASE_URL}{SERIES}")
        assert response.status_code == HTTPStatus.OK
        response_body = response.json()
        template = load_schema("series.yml")
        validate(instance=response_body, schema=template)

    @pytest.mark.positive
    def test_get_series_with_rating_success(self, api_client):
        response = api_client.get(
            f"{BASE_URL}{SERIES}",
        params=({"rating": 7}))
        assert response.status_code == HTTPStatus.OK
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

    @pytest.mark.positive
    def test_get_series_filter_by_status_success(self, api_client):
        response = api_client.get(
            f"{BASE_URL}{SERIES}",
            params={"status": "watched"}
        )
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

        compare = DeepDiff(expected_response, response_body, ignore_order=True)
        assert not compare, compare

    @pytest.mark.positive
    def test_get_series_sort_by_rating_asc_success(self, api_client):
        response = api_client.get(
            f"{BASE_URL}{SERIES}",
            params={"sort": "rating_asc"}
        )
        assert response.status_code == HTTPStatus.OK
        response_body = response.json()
        actual_ratings = [series["rating"] for series in response_body]
        expected_ratings = [6, 7, 8, 8, 9]
        assert actual_ratings == expected_ratings

    @pytest.mark.positive
    def test_get_series_by_rating_range_success(self, api_client):
        response = api_client.get(
            f"{BASE_URL}{SERIES}",
            params={"rating_range": "gt4_lt8"}
        )
        assert response.status_code == HTTPStatus.OK
        response_body = response.json()
        actual_names = [series["name"] for series in response_body]
        expected_names = ['Извне', 'Паук-Нуар']
        compare = DeepDiff(expected_names, actual_names, ignore_order=True)
        assert not compare, compare

    @pytest.mark.negative
    def test_get_series_not_found_endpoint(self, api_client):
        invalid_endpoint = f"{BASE_URL}/api/v1/some_fake_endpoint_999"
        response = api_client.get(invalid_endpoint)
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.negative
    def test_get_series_invalid_query_params(self, api_client):
        response = api_client.get(
            f"{BASE_URL}{SERIES}",
        params={"status": "invalid_status"})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        response_body = response.json()
        check.equal(response_body.get("error"), "validation error")

        expected_message = "Input should be 'watching', 'watched' or 'will_watch'"
        with check:
            error_detail = response_body.get("detail", [])
            assert expected_message == error_detail[0]["msg"]