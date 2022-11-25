import pytest

from constants import TEST_URL_1
from main import is_link


def test_valid_url():
    assert is_link({TEST_URL_1}) == {TEST_URL_1: {}}


def test_empty_set():
    assert is_link({}) == {}


def test_not_valid_url():
    assert is_link({'https://google'}) == {}
