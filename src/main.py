# from get_poi import TripAdvisorApi
# from poi_data import PoiData
# from helpers import ErrorHandling
# from users import User
# from file_handler import UserFile


# place = Places()                # Instantiate place
# region = place.select_region()  # Select country and region
# region_search = TripAdvisorApi(region)  # Query TripAdvisorAPI
# location_result = region_search.location_search()   # get location id
# poi = region_search.get_poi(location_result["location_id"])   # get pois
# if "errors" in poi:    # select city if search is too wide
#     location_result, poi, region = ErrorHandling.poi_error(region)
# data = PoiData(location_result, poi)
# data.extract()
# data.consolidate_categories()
# userfile = UserFile("resources/saved")
# userfile.save_data(region, data.city_info)
