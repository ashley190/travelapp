import requests
import json
from error_handlers import ErrorHandling


class ApiQuery:
    def __init__(self, url, querystring=None, headers=None):
        self.url = url
        self.querystring = querystring
        self.headers = headers

    @ErrorHandling.handle_request_errors
    def get_data(self):
        response = requests.get(self.url, params=self.querystring, headers=self.headers)
        response_code = response.status_code
        data = json.loads(response.text)
        return response_code, data
