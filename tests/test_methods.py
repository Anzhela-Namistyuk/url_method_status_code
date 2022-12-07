import asyncio

import pytest

from constants import (CONNECTION_ERROR_VALUE, TEST_INCORRECT_URL, TEST_URL_1,
                       TEST_WRONG_URL, TEST_URL_2)
from main import UrlMethodStatusCode

link_method_status = UrlMethodStatusCode(
    {
        TEST_INCORRECT_URL, TEST_URL_2, TEST_WRONG_URL
    }
)


def test_valid_url():
    assert link_method_status.is_link(TEST_URL_1)


def test_not_valid_url(capsys, a_links):
    is_valid_url = link_method_status.is_link(TEST_WRONG_URL)
    captured = capsys.readouterr()
    assert captured.out == a_links
    assert not is_valid_url


def test_method_availability_valid_url(url_with_method):
    asyncio.run(
        link_method_status.http_method_availability(TEST_URL_2)
    )
    value_by_key = link_method_status.url_method_status[TEST_URL_2]
    assert value_by_key == url_with_method[TEST_URL_2]


def test_method_availability_with_incorrect_url():
    asyncio.run(
        link_method_status.http_method_availability(TEST_INCORRECT_URL)
    )
    value_by_key = link_method_status.url_method_status[TEST_INCORRECT_URL]
    assert all(
        [status is CONNECTION_ERROR_VALUE for status in value_by_key.values()]
    )


def test_print_available_url_methods(capsys, result_dict):
    asyncio.run(link_method_status.check_urls())
    link_method_status.print_available_url_methods()
    captured = capsys.readouterr()
    for url, method_to_status in result_dict.items():
        assert str(url) in captured.out
        for method, status in method_to_status.items():
            assert f"'{method}': {status}" in captured.out


def test_check_urls(dict_after_check_urls):
    asyncio.run(link_method_status.check_urls())
    assert link_method_status.url_method_status == dict_after_check_urls
