class ErrorHandling:
    @classmethod
    def poi_error(cls, region_and_country):
        from places import Places
        from poi import TripAdvisorApi

        """Handles error returned from API due to too wide a search"""
        region = Places()
        city = region.select_city(region_and_country)
        city_search = TripAdvisorApi(city)
        location_id = city_search.get_location_id()
        poi = city_search.get_poi(location_id)
        return poi

    @classmethod
    def handle_request_errors(cls, func):
        def wrapper(*args, **kwargs):
            func_value = func(*args, **kwargs)
            if func_value[0] >= 500:
                return "Server Error. Try Again"
            elif func_value[0] >= 400:
                return "Request Error. Try Again"
            elif func_value[0] >= 300:
                return "Redirection Error. Try Again"
            return func_value[1]
        return wrapper
