import asyncio

from main import main


def test_main_empty_set(capsys):
    data_input = set()
    asyncio.run(main(data_input))
    captured = capsys.readouterr()
    assert captured.out == '{}\n'


def test_main_data(capsys):
    data_input = {'https://google.coms', 'https://google.com'}
    asyncio.run(main(data_input))
    captured = capsys.readouterr()
    assert captured.out == "{'https://google.com': {'GET': 200, 'HEAD': 301}}\n"


def test_main_data(capsys):
    data_input = {'google.com'}
    asyncio.run(main(data_input))
    captured = capsys.readouterr()
    assert captured.out == 'Строка google.com не является ссылкой.\n{}\n'
