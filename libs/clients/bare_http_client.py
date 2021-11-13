from urllib.parse import urlparse

import allure
import curlify
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from libs.clients.response_handler import Handler


class BareHttpClient:
    request_message_tpl = 'METHOD: {method}\nURL: {url}\nHEADERS: {headers}\nBODY: {body}'
    response_message_tpl = 'STATUS: {status}\nHEADERS: {headers}\nBODY: {body}'

    def __init__(self, base_url: str, max_retries=5, default_headers=None):
        adapter = HTTPAdapter(max_retries=Retry(total=max_retries))
        self.session = requests.session()
        self.session.verify = False
        self.session.mount(f'{urlparse(base_url).scheme}://', adapter)
        self._default_headers = default_headers or {}
        self._base_url = base_url if not base_url.endswith('/') else f'{base_url}/'
        self._errors_handler = None
        self._last_errors_handler = None
        self._content_handler = None
        self._last_content_handler = None

    def add_errors_handler(self, handler: Handler):
        if not self._last_errors_handler:
            self._errors_handler = self._last_errors_handler = handler
        else:
            self._last_errors_handler = self._last_errors_handler.set_next(handler)

    def add_content_handler(self, handler: Handler):
        if not self._last_content_handler:
            self._content_handler = self._last_content_handler = handler
        else:
            self._last_content_handler = self._last_content_handler.set_next(handler)

    def handle_response_content(self, response):
        if self._content_handler:
            return self._content_handler.handle(response)
        return response

    def handle_response(self, response):
        if self._errors_handler:
            response = self._errors_handler.handle(response)
        return self.handle_response_content(response)

    def _get_url(self, url):
        return f'{self._base_url}{url}'

    def _log_action(self, response):
        request_message = self.request_message_tpl.format(
            method=response.request.method,
            url=response.request.url,
            headers=response.request.headers,
            body=response.request.body
        )
        response_message = self.response_message_tpl.format(
            status=response.status_code, headers=response.headers, body=response.text
        )

        allure.attach(request_message, 'REQUEST', allure.attachment_type.TEXT)
        if not response.request.headers.get('content-type', '').startswith('application/msgpack'):
            allure.attach(curlify.to_curl(response.request), 'CURL', allure.attachment_type.TEXT)
        allure.attach(response_message, 'RESPONSE', allure.attachment_type.TEXT)

    def request(self, method, url, **kwargs):
        kwargs['headers'] = dict(self._default_headers, **kwargs.get('headers', {}))
        if method.lower() == 'get':
            kwargs['headers'].pop('content-type', None)
        response = self.session.request(method, self._get_url(url), **kwargs)
        self._log_action(response)
        return response

    def do_request(self, method, url, **kwargs):
        return self.request(method, url, **kwargs)

    def get(self, url, **kwargs):
        return self.handle_response(self.do_request('GET', url, **kwargs))

    def post(self, url, **kwargs):
        return self.handle_response(self.do_request('POST', url, **kwargs))

    def put(self, url, **kwargs):
        return self.handle_response(self.do_request('PUT', url, **kwargs))

    def patch(self, url, **kwargs):
        return self.handle_response(self.do_request('PATCH', url, **kwargs))

    def delete(self, url, **kwargs):
        return self.handle_response(self.do_request('DELETE', url, **kwargs))
