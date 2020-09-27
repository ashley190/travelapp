from dotenv import load_dotenv
import os
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

    def __init__(self, region, city):
        self.region_and_country = region
        self.city_and_country = city

    def location_search(self, place):
        url = self.endpoint + self.location_suffix
        querystring = {"query": f"{place[0]}, {place[1]}"}
        location_id_query = ApiQuery(url, querystring, self.headers)
        location_data = location_id_query.get_data()
        lookup = Helpers.geo_search(location_data["data"])
        dict_search = Helpers.key_lookup(
            lookup, "name",
            "location_id",
            "description")
        return dict_search

    def get_poi(self, location_id):
        url = self.endpoint + self.poi_suffix
        querystring = {"location_id": (location_id)}
        poi_query = ApiQuery(url, querystring, self.headers)
        poi_results = poi_query.get_data()
        return poi_results

    def poi_search(self):
        region_info = self.location_search(self.region_and_country)
        region_pois = self.get_poi(region_info["location_id"])
        return (region_info, region_pois, "region")
        if "errors" in region_pois:
            city_info = self.location_search(self.city_and_country)
            city_pois = self.get_poi(city_info["location_id"])
            return (city_info, city_pois, "city")
