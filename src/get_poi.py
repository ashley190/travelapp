from dotenv import load_dotenv
import os
from places import Places
from helpers import Helpers, ApiQuery


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

    def location_search(self):
        url = self.endpoint + self.location_suffix
        querystring = {"query": f"{self.region}, {self.country}"}
        location_id_query = ApiQuery(url, querystring, self.headers)
        location_data = location_id_query.get_data()
        lookup = Helpers.geo_search(location_data["data"])
        dict_search = Helpers.key_lookup(lookup, "name", "location_id", "description")
        return dict_search

    def get_poi(self, location_id):
        url = self.endpoint + self.poi_suffix
        querystring = {"location_id": (location_id)}
        poi_query = ApiQuery(url, querystring, self.headers)
        poi_results = poi_query.get_data()
        return poi_results