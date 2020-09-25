from places import Places
from poi import TripAdvisorApi


class ErrorHandling:
    @classmethod
    def poi_error(cls, region_and_country):
        """Handles error returned from API due to too wide a search"""
        region = Places()
        city = region.select_city(region_and_country)
        city_search = TripAdvisorApi(city)
        location_id = city_search.get_location_id()
        poi = city_search.get_poi(location_id)
        return poi
