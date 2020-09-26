class ErrorHandling:
    @classmethod
    def poi_error(cls, region_and_country):
        from places import Places
        from get_poi import TripAdvisorApi

        """Handles error returned from API due to too wide a search"""
        region = Places()
        city = region.select_city(region_and_country)
        city_search = TripAdvisorApi(city)
        location_result = city_search.location_search()
        poi = city_search.get_poi(location_result["location_id"])
        return location_result, poi, city

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


class Helpers:
    @classmethod
    def key_lookup(cls, target, *keys):
        key_dict = {}
        for key in keys:
            if key in target:
                key_dict[key] = target[key]
        return key_dict

    @classmethod
    def geo_search(cls, target):
        for data in target:
            if data["result_type"] == "geos":
                return data["result_object"]

    @classmethod
    def remove_ads(cls, target):
        ads_removed = []
        for item in target:
            if "ad_position" not in item and "ad_size" not in item:
                ads_removed.append(item)
        return ads_removed
