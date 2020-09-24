import requests
from dotenv import load_dotenv
import os


class ApiHandler():
    def __init__(self, url, query_string, headers):
        self.url = url
        self.query_string = query_string
        self.headers = headers

    def construct_api_query(self):
        response = requests.get(self.url, params=self.query_string, headers=self.headers)
        return response.status_code


load_dotenv()
tripadvisor = ApiHandler(
    "https://tripadvisor1.p.rapidapi.com/locations/auto-complete",
    {"query": "Tōkyō, Japan"},
    {
        "x-rapidapi-host": "tripadvisor1.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("API_KEY")
        })
code = tripadvisor.construct_api_query()
print(code)
