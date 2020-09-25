from dotenv import load_dotenv
import os
from places import Places
from api import ApiQuery


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
        location_id_query = ApiQuery(url, querystring, self.headers)
        location_id = location_id_query.get_data()
        return location_id["data"][0]["result_object"]["location_id"]

    def get_poi(self, location_id):
        url = self.endpoint + self.poi_suffix
        querystring = {"location_id": (location_id)}
        poi_query = ApiQuery(url, querystring, self.headers)
        poi_results = poi_query.get_data()
        return poi_results
