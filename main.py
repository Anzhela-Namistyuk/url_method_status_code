import asyncio
import logging
from typing import Dict, Set

import aiohttp
import validators
from aiohttp import ClientConnectorError

from configs import configure_logging, parser
from constants import CONNECTION_ERROR_VALUE


class UrlMethodStatusCode:
    def __init__(self, urls: Set[str]) -> None:
        self.urls = urls
        self.url_method_status = {}

    def is_link(self, url: str) -> None:
        """
        Checks if string are link.
        Add in url_method_status: dictionary -
        keys is urls, values is empty dictionary.
        :param url: string
        """
        if not validators.url(url):
            print(f'Строка {url} не является ссылкой.')
            logging.info(
                f'Строка "{url}" не является ссылкой.',
            )
        else:
            self.url_method_status[url] = {}

    async def method_request(
            self,
            url: str,
            method_to_status: Dict[str, int],
            client_session,
            method: str
    ):
        """Make http request."""
        try:
            resp = await client_session(url)
            status_code = resp.status
            method_to_status[method] = status_code

        except ClientConnectorError:
            logging.info(
                f'Возникла ошибка соединения при {method} запросе по адресу {url}'
            )
            method_to_status[method] = CONNECTION_ERROR_VALUE

    async def http_method_availability(
            self,
            url: str,
            method_to_status: Dict[str, int]
    ):
        """
        Checks all http methods.
        :param  method_to_status: empty dictionary or
        with keys: methods and values: statuses
        :param url: url for http request.
        """
        async with aiohttp.ClientSession() as session:
            queue = asyncio.Queue()
            task_list = []
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
                    task = asyncio.create_task(
                        self.method_request(
                            url, method_to_status, client_session, method)
                    )
                    task_list.append(task)

            await queue.join()
            await asyncio.gather(*task_list)

    def delete_unnecessary_methods(
            self,
            url: str,
            method_to_status: Dict[str, int]):
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
                f'Ссылка {url} - {method} запрос, '
                f'завершился ошибкой {method_to_status[method]}'
            )
            method_to_status.pop(method)

    def check_urls(self):
        """
        Check all urls in url_method_status dictionary
        and delete url which doesn't have any methods available.
        """
        # List for urls that encountered a connection error:
        error_urls_list = []
        for url, method_to_status in self.url_method_status.items():
            asyncio.run(self.http_method_availability(url, method_to_status))
            if CONNECTION_ERROR_VALUE in method_to_status.values():
                asyncio.run(self.http_method_availability(
                    url, method_to_status))
            # Function removes unnecessary methods from the dictionary method_to_status:
            self.delete_unnecessary_methods(url, method_to_status)
            # If the dictionary method_to_status is empty, then add this url to the list:
            if not method_to_status:
                error_urls_list.append(url)
        # remove from dictionary url_method_status keys with urls for which
        # it was not possible to make requests:
        for url in error_urls_list:
            self.url_method_status.pop(url)

    def main(self) -> None:
        """
        Checks which methods are available on this url and print a
        dictionary, the keys are urls, the values are dictionaries
        in which the keys are http methods,and the values are status codes.
        """
        for url in self.urls:
            self.is_link(url)
        if self.url_method_status:
            self.check_urls()
        print(self.url_method_status)


if __name__ == '__main__':
    configure_logging()
    logging.info('Парсер запущен!')

    args = parser.parse_args()
    urls = set(args.urls)

    logging.info(f'Аргументы командной строки: {args}')
    urls_method_status = UrlMethodStatusCode(urls)
    urls_method_status.main()

    logging.info('Парсер завершил работу.')
