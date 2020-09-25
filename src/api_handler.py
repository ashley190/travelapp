import requests
from dotenv import load_dotenv
import os
import json


class ApiHandler():
    def __init__(self, url, query_string, headers):
        self.url = url
        self.query_string = query_string
        self.headers = headers

    def get_info(self):
        response = requests.get(self.url, params=self.query_string, headers=self.headers)
        response_code = response.status_code
        info = json.loads(response.text)
        return info


# testing
load_dotenv()
tripadvisor = ApiHandler(
    "https://tripadvisor1.p.rapidapi.com/locations/auto-complete",
    {"query": "Tōkyō, Japan"},
    {
        "x-rapidapi-host": "tripadvisor1.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("API_KEY")
        })
test = tripadvisor.get_info()
print(test['data'][0]['result_type'])
