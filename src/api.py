import requests
import json


class ApiQuery():
    def __init__(self,url, querystring, headers):
        self.url = url
        self.querystring = querystring
        self.headers = headers
    
    def get_data(self):
        response = requests.get(self.url, params=self.querystring, headers = self.headers)
        response_code = response.status_code
        data = json.loads(response.text)
        return data
