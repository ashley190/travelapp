from places_db import Places
from api_handler import TripAdvisorApi


print("Welcome to the travel app")

print("Where to go?")
places = Places()
place = TripAdvisorApi(places.select_city())   #(city,country)
location_id=place.get_location_id()
places_of_interest = place.get_poi(location_id)
print(place.top_poi(places_of_interest))