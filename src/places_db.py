from File_Handler import JsonHandler
from simple_term_menu import TerminalMenu


class Places:
    def __init__(self, places_file):
        self.places = JsonHandler.read_json(places_file)
        self.cities_database = self.create_cities_database()

    def create_cities_database(self):
        """
        creates database in the format {country: [{state/admin_area:[city1, city2, city3, etc...]]}}
        """
        database = {}
        for place in self.places:
            if place["country"] not in database:
                database[place["country"]] = {place["admin_name"]: [place["city_ascii"]]}
            elif place["admin_name"] not in database[place["country"]]:
                database[place["country"]][place["admin_name"]] = [place["city"]]
            elif place['city_ascii'] not in database[place['country']][place['admin_name']]:
                database[place['country']][place['admin_name']].append(place['city_ascii'])
        return database

    def select_country_and_city(self):
        countries = [country for country in self.cities_database]
        countries_menu = TerminalMenu(countries, title="Select a country")
        country_selection = countries_menu.show()
        cities = [city for city in self.cities_database[countries[country_selection]]]
        cities_menu = TerminalMenu(cities, title="Select a city")
        city_selection = cities_menu.show()


all_places = Places('resources/worldcities.json')
print(all_places.select_country_and_city())
