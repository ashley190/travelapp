from file_handler import JsonHandler
from simple_term_menu import TerminalMenu   # type: ignore


class Database:
    def __init__(self, places_file: str = 'resources/worldcities.json'):
        self.places = JsonHandler.read_json(places_file)
        self.cities_database: dict = self.create_cities_database()

    def create_cities_database(self) -> dict:
        """
        creates database in the format {country: {state/admin_area:[city1, city2, city3, etc...]}}
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


class Places(Database):
    def select_country(self):
        list_of_countries: list = [country for country in self.cities_database]
        countries_menu: TerminalMenu = TerminalMenu(list_of_countries, title="Select a country")
        country_index: int = countries_menu.show()
        selected_country: str = list_of_countries[country_index]
        return selected_country

    def select_region(self) -> tuple:
        selected_country = self.select_country()
        list_of_regions: list = [region for region in self.cities_database[selected_country] if region != ""]
        regions_menu: TerminalMenu = TerminalMenu(list_of_regions, title=f"Select a region in {selected_country}")
        region_index: int = regions_menu.show()
        selected_region: str = list_of_regions[region_index]
        return (selected_region, selected_country)

    def select_city(self, selected_region_and_country: tuple) -> tuple:
        selected_region, selected_country = selected_region_and_country
        list_of_cities: list = [city for city in self.cities_database[selected_country][selected_region] if city != []]
        cities_menu: TerminalMenu = TerminalMenu(list_of_cities, title=f"Select a city in {selected_region}")
        city_index: int = cities_menu.show()
        selected_city: str = list_of_cities[city_index]
        return (selected_city, selected_country)