import pytest

from constants import CONNECTION_ERROR_VALUE, TEST_URL_1
from main import delete_unnecessary_methods


def test_delete_unnecessary_methods_with_405_cev():
    entry_dict = {'HEAD': 200, 'GET': 405,
                  'POST': CONNECTION_ERROR_VALUE}
    expected_dict = {'HEAD': 200}
    delete_unnecessary_methods(TEST_URL_1, entry_dict)
    assert entry_dict == expected_dict


def test_delete_unnecessary_methods_suitable_statuses():
    entry_dict = {'GET': 200, 'HEAD': 302, 'POST': 200}
    expected_dict = {'GET': 200, 'HEAD': 302, 'POST': 200}
    delete_unnecessary_methods(TEST_URL_1, entry_dict)
    assert entry_dict == expected_dict
