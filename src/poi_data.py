from helpers import Helpers


class PoiData:
    def __init__(self, city_info, poi_results):
        self.city_info = city_info
        self.poi_results = poi_results["data"]

    def extract(self):
        raw_pois = Helpers.remove_ads(self.poi_results)
        list_of_pois = []
        for poi in raw_pois:
            poi_details = Helpers.key_lookup(poi, "name", "location_id", "rating", "description", "category", "subcategory", "web_url", "website", "subtype")
            list_of_pois.append(poi_details)
        self.city_info["pois"] = list_of_pois

    def consolidate_categories(self):
        for item in self.city_info["pois"]:
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


class Display:
    def __init__(self, place, data):
        self.data = data
        self.place = place
