import asyncio
import logging
from typing import Dict, Set

import aiohttp
import validators
from aiohttp import ClientConnectorError

from configs import configure_logging, parser
from constants import CONNECTION_ERROR_VALUE


def is_link(urls: Set[str]) -> Dict[str, None]:
    """
    Checks if all strings in a set are links.
    :param urls: set with urls
    :return  url_method_status: dictionary -
    keys is urls, values is empty dictionary.
    """
    url_method_status = {}
    for url in urls:
        if not validators.url(url):
            print(f'Строка {url} не является ссылкой.')
            logging.info(
                f'Строка "{url}" не является ссылкой.',
            )
            continue
        url_method_status[url] = {}
    return url_method_status


async def http_method_availability(
        url: str,
        method_to_status: Dict[str, int]
):
    """
    Function checks all http methods.
    :param  method_to_status: empty dictionary or
    with keys: methods and values: statuses
    :param url: url for http request.
    """
    async with aiohttp.ClientSession() as session:
        http_methods = {
            'GET': session.get,
            'HEAD': session.head,
            'POST': session.post,
            'PUT': session.put,
            'DELETE': session.delete,
            'OPTIONS': session.options,
            'PATCH': session.patch,
        }
        for method, client_session in http_methods.items():
            status_code = method_to_status.get(method, None)
            if status_code in [CONNECTION_ERROR_VALUE, None]:
                try:
                    resp = await client_session(url)
                    status_code = resp.status
                    method_to_status[method] = status_code

                except ClientConnectorError:
                    logging.info(
                        f'Возникла ошибка соединения при {method} запросе по адресу {url}'
                    )
                    method_to_status[method] = CONNECTION_ERROR_VALUE


async def check_urls(
        url_method_status: Dict[str, Dict[str, int]]
):
    """
    Check all urls in url_method_status dictionary
    and delete url which doesn't have any methods available.
    :param url_method_status: dictionary -
    keys are urls, values is empty dictionary.
    """
    # List for urls that encountered a connection error:
    error_urls_list = []
    for url, method_to_status in url_method_status.items():
        await http_method_availability(
            url, method_to_status
        )
        if CONNECTION_ERROR_VALUE in method_to_status.values():
            await http_method_availability(
                url, method_to_status)
        # Function removes unnecessary methods from the dictionary method_to_status:
        delete_unnecessary_methods(url, method_to_status)
        # If the dictionary method_to_status is empty, then add this url to the list:
        if not method_to_status:
            error_urls_list.append(url)
    # remove from dictionary url_method_status keys with urls for which
    # it was not possible to make requests:
    for url in error_urls_list:
        url_method_status.pop(url)


def delete_unnecessary_methods(url: str, method_to_status: Dict[str, int]):
    """
    Removes methods with a 405 status code or a connection error
    :param  method_to_status: empty dictionary
    with keys: methods and values: statuses
    """
    unnecessary_methods = [
        method for method, status in method_to_status.items()
        if status in [CONNECTION_ERROR_VALUE, 405]
    ]
    for method in unnecessary_methods:
        logging.info(
            f'Ссылка {url} - обработка метода {method}, '
            f'завершилась ошибкой {method_to_status[method]}'
        )
        method_to_status.pop(method)


async def main(urls: Set[str]) -> Dict[str, Dict[str, int]]:
    """
    Checks which methods are available on this url and print a
    dictionary, the keys are urls, the values are dictionaries
    in which the keys are http methods,and the values are status codes.
    :param urls: set with urls.
    """
    url_method_status = is_link(urls)
    if url_method_status:
        await check_urls(url_method_status)
    print(url_method_status)


if __name__ == '__main__':
    configure_logging()
    logging.info('Парсер запущен!')

    args = parser.parse_args()
    urls = set(args.urls)

    logging.info(f'Аргументы командной строки: {args}')

    asyncio.run(main(urls))

    logging.info('Парсер завершил работу.')
