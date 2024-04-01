import json
import logging
import allure
import httpx
from httpx import Client


def response_to_curl(response: httpx.Response) -> str:
    curl_command = f"curl -X {response.request.method} '{response.url}'"
    for name, value in response.request.headers.items():
        curl_command += f" -H '{name}: {value}'"
    if response.request.content:
        curl_command += f" -d '{response.request.content.decode()}'"
    return curl_command


def allure_request_logger(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        logging.info(f'{response.status_code} ')

        try:
            allure.attach(
                body=response_to_curl(response),
                name=f'Request {response.request.method} status code - {response.status_code}',
                attachment_type=allure.attachment_type.TEXT,
                extension='txt'
            )
        except UnicodeDecodeError:
            pass
        try:
            allure.attach(
                body=json.dumps(response.json(), indent=4, ensure_ascii=False).encode('utf8'),
                name=f'Response {response.content}',
                attachment_type=allure.attachment_type.JSON,
                extension='json'
            )
        except ValueError:
            allure.attach(
                body=response.text.encode('utf8'),
                name=f'NOT JSON Response {response.content}',
                attachment_type=allure.attachment_type.JSON,
                extension='json'
            )
        return response

    return wrapper


class BaseSession(Client):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    @allure_request_logger
    def request(self, method, url: str, *args, **kwargs) -> httpx.Response:
        with allure.step(f'{method} {url}'):
            response = super().request(method, f'{self.base_url}{url}', *args, **kwargs)
        return response

