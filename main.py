import asyncio
import logging
from typing import Set

import aiohttp
import validators
from aiohttp import ClientConnectorError

from configs import configure_logging, parser
from constants import CONNECTION_ERROR_VALUE


class UrlMethodStatusCode:
    def __init__(self, urls: Set[str]) -> None:
        self.url_method_status = {
            url: {} for url in urls if self.is_link(url)
        }

    @staticmethod
    def is_link(url: str) -> bool:
        """
        Checks if string is link.
        :param url: string
        """
        is_url_valid = validators.url(url)
        if not is_url_valid:
            print(f'Строка {url} не является ссылкой.')
            logging.info(
                f'Строка "{url}" не является ссылкой.',
            )
        return is_url_valid

    async def method_request(
            self,
            url: str,
            http_method,
            method: str
    ):
        """
        Make http request for each method
        and adds in dictionary
        key: methods, value: status code to the
        "url_method_status"  dictionary  values.
        """

        try:
            resp = await http_method(url)
            status_code = resp.status
            self.url_method_status[url][method] = status_code

        except ClientConnectorError:
            logging.info(
                f'Возникла ошибка соединения при {method} запросе по адресу {url}'
            )
            self.url_method_status[url][method] = CONNECTION_ERROR_VALUE

    async def http_method_availability(self, url: str):
        """
        Checks all http methods.
        :param url: url for http request.
        """
        async with aiohttp.ClientSession() as session:
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

            method_to_status = self.url_method_status.get(url)

            for method, client_session in http_methods.items():
                status_code = method_to_status.get(method, None)
                if status_code in [CONNECTION_ERROR_VALUE, None]:
                    task = asyncio.create_task(
                        self.method_request(
                            url, client_session, method)
                    )
                    task_list.append(task)

            await asyncio.gather(*task_list)

    async def availability_method_for_url(self, url):
        """
        Check available methods for url and
        re-check available methods if response
        came with CONNECTION_ERROR_VALUE.
        :param url:
        """
        await self.http_method_availability(url)
        method_to_status = self.url_method_status.get(url)
        if CONNECTION_ERROR_VALUE in method_to_status.values():
            await self.http_method_availability(url)

    async def check_urls(self):
        """
        Check all urls in url_method_status dictionary.
        """
        task_list = []

        for url in self.url_method_status:
            task = asyncio.create_task(self.availability_method_for_url(url))
            task_list.append(task)

        await asyncio.gather(*task_list)

    def print_available_url_methods(self):
        """
        Print dictionary with available urls,
        methods and their status code
        without a 405 status code or a connection error
        :param url:
        """
        result_dict = {}
        for url, method_to_status in self.url_method_status.items():
            filtered_method_to_status = {}
            for method, status in method_to_status.items():

                if status not in [CONNECTION_ERROR_VALUE, 405]:
                    filtered_method_to_status[method] = status
                else:
                    logging.info(
                        f'Ссылка {url} - {method} запрос, '
                        f'завершился ошибкой {status}'
                    )
            if filtered_method_to_status:
                result_dict[url] = filtered_method_to_status
        print(result_dict)


def main():

    configure_logging()
    logging.info('Парсер запущен!')

    args = parser.parse_args()
    urls = set(args.urls)

    logging.info(f'Аргументы командной строки: {args}')

    urls_method_status: UrlMethodStatusCode = UrlMethodStatusCode(urls)
    asyncio.run(urls_method_status.check_urls())
    urls_method_status.print_available_url_methods()

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
