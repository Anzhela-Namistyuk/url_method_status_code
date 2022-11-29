import pytest

from constants import TEST_URL_1


@pytest.fixture()
def a_links():
    return {TEST_URL_1: {}, 'https://google': None}


@pytest.fixture()
def url_with_method():
    return {
        TEST_URL_1:
            {'OPTIONS': 204, 'PATCH': 400, 'PUT': 400, 'HEAD': 200, 'DELETE': 200, 'GET': 200, 'POST': 200}
    }

@pytest.fixture()
def remaining_method():
    return {'HEAD': 200}