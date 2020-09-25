import requests
from dotenv import load_dotenv
import os
import json
from places import Places


class TripAdvisorApi:
    load_dotenv()
    endpoint = "https://tripadvisor1.p.rapidapi.com/"
    location_suffix = "locations/auto-complete"
    poi_suffix = "attractions/list"
    headers = {
            "x-rapidapi-host": "tripadvisor1.p.rapidapi.com",
            "x-rapidapi-key": os.getenv("API_KEY")
            }

    def __init__(self, place):
        self.region_and_country = place
        self.region = place[0]
        self.country = place[1]

    def get_location_id(self):
        url = self.endpoint + self.location_suffix
        querystring = {"query": f"{self.region}, {self.country}"}
        response = requests.get(url, params=querystring, headers=self.headers)
        response_code = response.status_code
        result = json.loads(response.text)
        return result["data"][0]["result_object"]["location_id"]

    def get_poi(self, location_id):
        url = self.endpoint + self.poi_suffix
        querystring = {"location_id": (location_id)}
        response = requests.get(url, params=querystring, headers=self.headers)
        response_code = response.status_code
        result = json.loads(response.text)
        return (result)
