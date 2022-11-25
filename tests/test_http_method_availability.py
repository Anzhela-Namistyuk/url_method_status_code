import asyncio

import pytest

from constants import CONNECTION_ERROR_VALUE, TEST_URL_1
from main import http_method_availability


def test_get_method():
    entry_dict = {}
    expected_dict = {'GET': 200}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['GET'] == expected_dict['GET']


def test_get_method_with_error_connect():
    entry_dict = {'GET': CONNECTION_ERROR_VALUE}
    expected_dict = {'GET': 200}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['GET'] == expected_dict['GET']


def test_head_method():
    entry_dict = {}
    expected_dict = {'HEAD': 200}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['HEAD'] == expected_dict['HEAD']


def test_head_method_with_error_connect():
    entry_dict = {'HEAD': CONNECTION_ERROR_VALUE}
    expected_dict = {'HEAD': 200}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['HEAD'] == expected_dict['HEAD']


def test_post_method():
    entry_dict = {}
    expected_dict = {'POST': 200}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['POST'] == expected_dict['POST']


def test_post_method_with_error_connect():
    entry_dict = {'POST': CONNECTION_ERROR_VALUE}
    expected_dict = {'POST': 200}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['POST'] == expected_dict['POST']


def test_put_method():
    entry_dict = {}
    expected_dict = {'PUT': 400}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['PUT'] == expected_dict['PUT']


def test_put_method_with_error_connect():
    entry_dict = {'PUT': CONNECTION_ERROR_VALUE}
    expected_dict = {'PUT': 400}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['PUT'] == expected_dict['PUT']


def test_patch_method():
    entry_dict = {}
    expected_dict = {'PATCH': 400}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['PATCH'] == expected_dict['PATCH']


def test_patch_method_with_error_connect():
    entry_dict = {'PATCH': CONNECTION_ERROR_VALUE}
    expected_dict = {'PATCH': 400}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['PATCH'] == expected_dict['PATCH']


def test_delete_method():
    entry_dict = {}
    expected_dict = {'DELETE': 200}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['DELETE'] == expected_dict['DELETE']


def test_delete_method_with_error_connect():
    entry_dict = {'DELETE': CONNECTION_ERROR_VALUE}
    expected_dict = {'DELETE': 200}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['DELETE'] == expected_dict['DELETE']


def test_options_method():
    entry_dict = {}
    expected_dict = {'OPTIONS': 204}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['OPTIONS'] == expected_dict['OPTIONS']


def test_options_method_with_error_connect():
    entry_dict = {'OPTIONS': CONNECTION_ERROR_VALUE}
    expected_dict = {'OPTIONS': 204}

    async def do_it(entry_dict):
        await http_method_availability(
            TEST_URL_1, entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert entry_dict['OPTIONS'] == expected_dict['OPTIONS']


def test_http_method_availability_with_wrong_url():
    entry_dict = {}

    async def do_it(entry_dict):
        await http_method_availability(
            'https://google.coms', entry_dict
        )

    asyncio.run(do_it(entry_dict))
    assert all(
        [status is CONNECTION_ERROR_VALUE for status in entry_dict.values()]
    )
