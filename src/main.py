from users import User, UserFile
from places import Places
from get_poi import TripAdvisorApi
from poi_data import PoiData

# user and API check
ash = User()
key_check = ash.API_key_check()
while not key_check:
    ash.set_API_key()
    key_check = ash.API_key_check()

# place selection
place = Places()
selected_region = place.select_region()
user_path = f"resources/{ash.name}/"

# userfile object creation to search past history and display result if exists
ash_file = UserFile(selected_region, user_path)
file_name = f"{ash_file.region[0]}-{ash_file.region[1]}.json"
history_check = ash_file.search_and_display_data(selected_region, file_name)
if not history_check:
    ash_file.city = place.select_city(ash_file.region)
    file_name = f"{ash_file.region[0]}-{ash_file.region[1]}.json"
    history_check = ash_file.search_and_display_data(ash_file.city, file_name)
if not history_check:
    search_api = TripAdvisorApi(ash_file.region, ash_file.city)
    api_results = search_api.poi_search()
    results_data = PoiData(api_results[0], api_results[1])
    results_data.extract()
    results_data.consolidate_categories()
    ash_file.read_flag_and_save(results_data.city_info, api_results[2])
