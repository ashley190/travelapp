from users import User
from userfile import UserFile
from places import Places
from get_poi import TripAdvisorApi
from poi_data import PoiData

# user and API check
# If no API key, user given instructions to subscribe.
# API_key saved as a persistent environment variable in src/.env
user = User()
key_exist = user.API_key_check()
while not key_exist:
    user.set_API_key()
    key_exist = user.API_key_check()

# place selection
place = Places()
selected_region = place.select_region()

# userfile object creation to search past history and display result if exists
user_file = UserFile(selected_region, user.path)
user_file.searchfile = f"{user_file.region[0]}-{user_file.region[1]}.json"

# history check at region level
history_check = user_file.search_and_display_data(selected_region)

# history check at city level
if not history_check:
    user_file.city = place.select_city(user_file.region)
    user_file.searchfile = f"{user_file.city[0]}-{user_file.city[1]}.json"
    history_check = user_file.search_and_display_data(user_file.city)

# look up TripAdvisorAPI if region and city does not exist in cached file
# Extract and consolidate data
# Save and display data
if not history_check:
    search_api = TripAdvisorApi(user_file.region, user_file.city)
    api_results = search_api.poi_search()
    results_data = PoiData(api_results[0], api_results[1])
    results_data.extract()
    results_data.consolidate_categories()

    # Save and display data
    user_file.read_flag_and_save(results_data.place_info, api_results[2])
