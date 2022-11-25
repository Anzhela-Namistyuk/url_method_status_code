import asyncio

import pytest

from main import check_urls


def test_check_urls_with_exist_urls():
    entry_dict = {'https://docs.python.org': {}}
    expected_dict = {
        'https://docs.python.org': {
            'GET': 200, 'HEAD': 302, 'POST': 200
        }
    }

    async def do_it(entry_dict):
        await check_urls(entry_dict)

    asyncio.run(do_it(entry_dict))
    assert entry_dict == expected_dict


def test_check_urls_with_non_exist_urls():
    entry_dict = {'https://google.coms': {}}
    expected_dict = {}

    async def do_it(entry_dict):
        await check_urls(entry_dict)

    asyncio.run(do_it(entry_dict))
    assert entry_dict == expected_dict