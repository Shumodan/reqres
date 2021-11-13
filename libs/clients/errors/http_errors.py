from requests import HTTPError, Response


class HttpBaseError(HTTPError):

    def __init__(self, response):
        super(HttpBaseError, self).__init__()
        self.response: Response = response
        self.message = ''

    @staticmethod
    def get_text(response):
        if response.text.startswith('"'):
            return response.json()
        return response.text

    def __str__(self):
        return self.message.format(self.get_text(self.response)).strip()


class HttpUnsupportedStatus(HttpBaseError):

    def __init__(self, response):
        super(HttpUnsupportedStatus, self).__init__(response)
        self.message = 'The response contains an unsupported status code: {}'

    def __str__(self):
        return self.message.format(self.response.status_code).strip()


class HttpBadRequest(HttpBaseError):

    def __init__(self, response):
        super(HttpBadRequest, self).__init__(response)
        self.message = 'The request cannot be processed: {}'


class HttpNotFound(HttpBaseError):

    def __init__(self, response):
        super(HttpNotFound, self).__init__(response)
        self.message = 'The resource is not found on the server side: {}'
