from helpers import Helpers


class PoiData:
    """Creates PoiData object for data cleaning and formatting."""

    def __init__(self, place_info: dict, poi_results: dict):
        """Creates two instance attributes upon instantiation

        Creates instance attributes based on output of the
        poi_search method of a TripAdvisorApi object.

        Args:
            place_info (dict): dictionary of a region/city
                level information.
            poi_results (dict): dictionary containing a list
                of points of interests (POIs) and their associated data.
        """
        self.place_info: dict = place_info
        self.poi_results: list = poi_results["data"]

    def extract(self):
        """Remove ads and extract desired poi data.

        Removes embedded ads with Helpers.remove_ads(); lookup and extract
        desired data using Helpers.key_lookup() for all pois within list;
        consolidate extracted data into the place_info instance attribute
        under the key 'pois'.
        """
        raw_pois: list = Helpers.remove_ads(self.poi_results)
        list_of_pois: list = []
        for poi in raw_pois:
            poi_details = Helpers.key_lookup(
                poi,
                "name",
                "location_id",
                "rating",
                "description",
                "category",
                "subcategory",
                "web_url",
                "website",
                "subtype")
            list_of_pois.append(poi_details)
        self.place_info["pois"] = list_of_pois

    def consolidate_categories(self):
        """Consolidates categorical data into a single field

        Iterates through each poi dictionary and consolidate
        values that has the keys 'category', 'subcategory',
        and 'subtype' into a single key ('category') with
        subcategories and subtypes separated by a '>' delimiter.
        """
        for item in self.place_info["pois"]:
            # consolidated = ""
            if "category" in item and item["category"]["name"]:
                item["category"] = item["category"]["name"]
            if "subcategory" in item:
                for name in item["subcategory"]:
                    if name["name"]:
                        item["category"] += f" > {name['name']}"
                item.pop("subcategory")
            if "subtype" in item:
                for name in item["subtype"]:
                    if name["name"]:
                        item["category"] += f" > {name['name']}"
                item.pop("subtype")
