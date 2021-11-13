from config import config
from core.api.login import Login
from core.api.register import Register
from core.api.resources import Resources
from core.api.users import Users
from libs.clients.bare_http_client import BareHttpClient
from libs.clients.response_handler import OKStatusHandler, ErrorStatusHandler, DefaultJsonContentHandler


class Backend:
    def __init__(self):
        client = BareHttpClient(config.host_url)
        client.add_errors_handler(OKStatusHandler())
        client.add_errors_handler(ErrorStatusHandler())
        client.add_content_handler(DefaultJsonContentHandler())
        self.auth = Login(client)
        self.register = Register(client)
        self.resources = Resources(client)
        self.users = Users(client)
