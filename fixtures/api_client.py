import pytest
import requests

@pytest.fixture(scope="session")
def api_client():
    with requests.Session() as s:
        yield s