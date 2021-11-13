from libs.clients.bare_http_client import BareHttpClient


class BaseApi:

    url: str = None

    def __init__(self, client: BareHttpClient):
        self._client = client
