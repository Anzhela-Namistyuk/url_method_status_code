import pytest

from constants import TEST_URL_1, TEST_INCORRECT_URL, CONNECTION_ERROR_VALUE, TEST_URL_2


@pytest.fixture()
def a_links():
    return 'Строка https://google не является ссылкой.\n'


@pytest.fixture()
def url_with_method():
    return {
        TEST_URL_2:
            {'GET': 200, 'HEAD': 200, 'POST': 200, 'DELETE': 200, 'PUT': 200, 'PATCH': 200, 'OPTIONS': 405}
    }


@pytest.fixture()
def dict_after_check_urls():
    return {
        TEST_INCORRECT_URL:
            {'OPTIONS': CONNECTION_ERROR_VALUE,
             'PATCH': CONNECTION_ERROR_VALUE,
             'PUT': CONNECTION_ERROR_VALUE,
             'HEAD': CONNECTION_ERROR_VALUE,
             'DELETE': CONNECTION_ERROR_VALUE,
             'GET': CONNECTION_ERROR_VALUE,
             'POST': CONNECTION_ERROR_VALUE},
        TEST_URL_2:
            {'GET': 200, 'HEAD': 200, 'POST': 200, 'DELETE': 200, 'PUT': 200, 'PATCH': 200, 'OPTIONS': 405}
    }


@pytest.fixture()
def result_dict():
    return {
        TEST_URL_2:
            {'GET': 200, 'HEAD': 200, 'POST': 200, 'DELETE': 200, 'PUT': 200, 'PATCH': 200}
    }
