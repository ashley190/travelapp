from file_handler import JsonHandler
from simple_term_menu import TerminalMenu   # type: ignore


class Database:
    def __init__(self, places_file: str = 'resources/worldcities.json'):
        self.places = JsonHandler.read_json(places_file)
        self.cities_db: dict = self.create_cities_db()

    def create_cities_db(self) -> dict:
        """
        creates database in the following format
        {country: {state/admin_area:[city1, city2, city3, etc...]}}
        """
        database = {}
        for place in self.places:
            country = place["country"]
            state = place["admin_name"]
            city = place["city_ascii"]
            if country not in database:
                database[country] = {state: [city]}
            elif state not in database[country]:
                database[country][state] = [place["city"]]
            elif city not in database[country][state]:
                database[country][state].append(city)
        return database


class Places(Database):
    def select_country(self):
        list_of_countries: list = [country for country in self.cities_db]
        countries_menu: TerminalMenu = TerminalMenu(
            list_of_countries,
            title="Select a country")
        country_index: int = countries_menu.show()
        selected_country: str = list_of_countries[country_index]
        return selected_country

    def select_region(self) -> list:
        selected_country = self.select_country()
        country_regions = self.cities_db[selected_country]
        regions: list = [region for region in country_regions if region != ""]
        regions_menu: TerminalMenu = TerminalMenu(
            regions,
            title=f"Select a region in {selected_country}")
        region_index: int = regions_menu.show()
        selected_region: str = regions[region_index]
        return [selected_region, selected_country]

    def select_city(self, selected_region_and_country: list) -> list:
        selected_region, selected_country = selected_region_and_country
        regions_cities = self.cities_db[selected_country][selected_region]
        cities: list = [city for city in regions_cities if city != []]
        cities_menu: TerminalMenu = TerminalMenu(
            cities,
            title=f"Select a city in {selected_region}")
        city_index: int = cities_menu.show()
        selected_city: str = cities[city_index]
        return [selected_city, selected_country]
