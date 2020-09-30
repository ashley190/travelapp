from dotenv import load_dotenv
import os
from helpers import Helpers, ApiQuery, ErrorHandling


class TripAdvisorApi:
    """Construct and perform API queries.

    Constructs API queries to two different endpoints for
    location and Points of interest (POI) search to the
    TripAdvisor API on RapidAPI.

    Attributes:
        endpoint (str): TripAdvisor API endpoint prefix
        location_suffix (str): TripAdvisor API endpoint suffix
            for the location autocomplete search.
        poi_suffix (str): TripAdvisor API endpoint suffix
            for list of attractions search.
        headers (dict): required headers for API get query.
            This includes the API key stored as a persistent
            environment variable in the src/.env file.
    """
    load_dotenv()
    endpoint: str = "https://tripadvisor1.p.rapidapi.com/"
    location_suffix: str = "locations/auto-complete"
    poi_suffix: str = "attractions/list"
    headers: dict = {
            "x-rapidapi-host": "tripadvisor1.p.rapidapi.com",
            "x-rapidapi-key": os.getenv("API_KEY")
            }

    def __init__(self, region, city):
        """initialises TripAdvisorApi object with search fields.

        Args:
            region (list): inherited from the region attribute
                of a UserFile object. Used as a search field
                for a region/state level query on API.
            city (list): inherited from the city attribute of
                a UserFile object.
        """
        #: list: Used as a search field for a
        # region/state level query on API.
        self.region_and_country: list = region

        #: list: Used as a search field for a
        # city level query on API.
        self.city_and_country: list = city

    def location_search(self, place: list) -> dict:
        """Queries API endpoint for location data.

        Constructs API query, query API location autocomplete
        endpoint, process response for errors and consolidates
        required data from response.

        Args:
            place (list): self.region_and_country or
            self.city_and_country based on region or city
            level search as required.

        Returns:
            dict: relevant fields from API query response.
        """
        url: str = self.endpoint + self.location_suffix
        querystring: dict = {"query": f"{place[0]}, {place[1]}"}
        location_id_query: ApiQuery = ApiQuery(url, querystring, self.headers)
        location_data: tuple = location_id_query.get_data()
        ErrorHandling.handle_request_errors(location_data)
        lookup: dict = Helpers.geo_search(location_data[1]["data"])
        dict_search: dict = Helpers.key_lookup(
            lookup, "name",
            "location_id",
            "description")
        return dict_search

    def get_poi(self, location_id: str) -> dict:
        """Queries API endpoint for POI data.

        Constructs API query, query API attractions endpoint,
        process response for errors and returns results if successful.

        Args:
            location_id (str): location_id found in a successful
                location_search.

        Returns:
            dict: Dictionary containing a list of Points of Interests(POIs)
                from the attractions query using a locations location_id.
        """
        url: str = self.endpoint + self.poi_suffix
        querystring: dict = {"location_id": (location_id)}
        poi_query: ApiQuery = ApiQuery(url, querystring, self.headers)
        poi_results: tuple = poi_query.get_data()
        ErrorHandling.handle_request_errors(poi_results)
        return poi_results[1]

    def poi_search(self) -> tuple:
        """Conducts region level and city level location and poi search.

        Conducts a region level API search for location and poi and if
        results are too wide (indicated by error in poi result), narrows
        down to a city level search for location and poi.

        Returns:
            tuple: A tuple containing (location results, poi results and
            flag) depending on whether a regional level search was
            successful or a city level search was successful.
        """
        region_info: dict = self.location_search(self.region_and_country)
        region_pois: dict = self.get_poi(region_info["location_id"])
        if "errors" in region_pois:
            city_info: dict = self.location_search(self.city_and_country)
            city_pois: dict = self.get_poi(city_info["location_id"])
            return (city_info, city_pois, "city")
        else:
            return (region_info, region_pois, "region")
