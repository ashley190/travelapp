from file_handler import JsonHandler
from simple_term_menu import TerminalMenu   # type: ignore


class Database:
    """Database class to create database of cities"""

    def __init__(self, places_file: str = 'resources/worldcities.json'):
        """Initialises Database object with two instance attributes.

        Using data from places_file (list of cities in json format), the
        cities_db dictionary is created using the create_cities_db()
        method and stored as an instance attribute.

        Args:
            places_file (str, optional): file path pointing to json
                file for data lookup and extraction during instantiation.
                Defaults to 'resources/worldcities.json'.
        """
        self.places: list = JsonHandler.read_json(places_file)
        self.cities_db: dict = self.create_cities_db()

    def create_cities_db(self) -> dict:
        """Creates cities_db from json file output in a predefined format.

        Extracts country, state and city data from json file output and
        store it in standardised format.

        Returns:
            dict: Dictionary in the following format -  {country: {
                state/admin_area:[city1, city2, city3, etc...]}}
        """
        database: dict = {}
        for place in self.places:
            country: str = place["country"]
            state: str = place["admin_name"]
            city: str = place["city_ascii"]
            if country not in database:
                database[country] = {state: [city]}
            elif state not in database[country]:
                database[country][state] = [place["city"]]
            elif city not in database[country][state]:
                database[country][state].append(city)
        return database


class Places(Database):
    """Inherits database from Database class with additional selection methods

    Args:
        Database (class): Database class that creates a standardised cities_db
            when instantiated as an object.
    """
    def select_country(self) -> str:
        """Creates a selection menu from a list of countries for user selection.

        Creates a list of countries from the inherited instance attribute
        cities_db; create a selection menu based on the list of countries for
        user selection; Searches for country from the list of countries based
        on the index returned from user's selection.

        Returns:
            str: Selected country
        """
        list_of_countries: list = [country for country in self.cities_db]
        countries_menu: TerminalMenu = TerminalMenu(
            list_of_countries,
            title="Select a country")
        country_index: int = countries_menu.show()
        selected_country: str = list_of_countries[country_index]
        return selected_country

    def select_region(self) -> list:
        """Creates a selection menu from a list of regions/state for user selection.

        Creates a list of regions/states from the instance attribute cities_db
        based on the previously selected country; create a selection menu based
        on the list of regions/state for user selection; Searches for
        regions/state from the list of regions/state based on the index
        returned from user's selection.

        Returns:
            str: Selected region/state
        """
        selected_country: str = self.select_country()
        country_regions: dict = self.cities_db[selected_country]
        regions: list = [region for region in country_regions if region != ""]
        regions_menu: TerminalMenu = TerminalMenu(
            regions,
            title=f"Select a region in {selected_country}")
        region_index: int = regions_menu.show()
        selected_region: str = regions[region_index]
        return [selected_region, selected_country]

    def select_city(self, selected_region_and_country: list) -> list:
        """Creates a selection menu from a list of cities for user selection.

        Creates a list of cities from the instance attribute cities_db
        based on the previously selected country and region/state; create a
        selection menu based on the list of cities for user selection;
        Searches for city from the list of cities based on the
        index returned from user's selection.

        Returns:
            str: Selected region/state
        """
        selected_region, selected_country = selected_region_and_country
        db_cities: list = self.cities_db[selected_country][selected_region]
        cities: list = [city for city in db_cities if city != []]
        cities_menu: TerminalMenu = TerminalMenu(
            cities,
            title=f"Select a city in {selected_region}")
        city_index: int = cities_menu.show()
        selected_city: str = cities[city_index]
        return [selected_city, selected_country]
