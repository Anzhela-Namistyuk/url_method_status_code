import asyncio

import pytest

from constants import (CONNECTION_ERROR_VALUE, TEST_INCORRECT_URL, TEST_URL_1,
                       TEST_WRONG_URL)
from main import UrlMethodStatusCode

link_method_status = UrlMethodStatusCode({})


def test_valid_url(a_links):
    link_method_status.is_link(TEST_URL_1)
    assert link_method_status.url_method_status.get(TEST_URL_1) == a_links[TEST_URL_1]


def test_not_valid_url(capsys, a_links):
    link_method_status.is_link(TEST_WRONG_URL)
    captured = capsys.readouterr()
    assert link_method_status.url_method_status.get(TEST_WRONG_URL) == a_links[TEST_WRONG_URL]
    assert captured.out == 'Строка https://google не является ссылкой.\n'


def test_method_availability_valid_url(url_with_method):
    method_to_status = {}
    asyncio.run(
        link_method_status.http_method_availability(TEST_URL_1, method_to_status)
    )
    assert method_to_status == url_with_method[TEST_URL_1]


def test_method_availability_valid_url_with_conrct_error(url_with_method):
    method_to_status = {'DELETE': CONNECTION_ERROR_VALUE}
    asyncio.run(
        link_method_status.http_method_availability(TEST_URL_1, method_to_status)
    )
    assert method_to_status == url_with_method[TEST_URL_1]


def test_method_availability_incorrect_url():
    method_to_status = {}
    asyncio.run(
        link_method_status.http_method_availability(TEST_INCORRECT_URL, method_to_status)
    )
    assert all(
        [status is CONNECTION_ERROR_VALUE for status in method_to_status.values()]
    )


def test_delete_unnecessary_methods_with_405_cev(remaining_method):
    method_to_status = {'HEAD': 200, 'GET': 405,
                        'POST': CONNECTION_ERROR_VALUE}
    link_method_status.delete_unnecessary_methods(TEST_URL_1, method_to_status)
    assert method_to_status == remaining_method


def test_check_urls_with_exist_urls(url_with_method):
    link_method_status.url_method_status = {TEST_URL_1: {}}
    link_method_status.check_urls()
    assert link_method_status.url_method_status == url_with_method


def test_check_urls_with_non_exist_urls():
    link_method_status.url_method_status = {TEST_INCORRECT_URL: {}}
    link_method_status.check_urls()
    assert not link_method_status.url_method_status


def test_main_data(capsys):
    link_method_status.urls = {TEST_INCORRECT_URL}
    link_method_status.main()
    captured = capsys.readouterr()
    assert captured.out == "{}\n"
