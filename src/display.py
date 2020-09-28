import textwrap
from prettytable import PrettyTable     # type: ignore


class Display:
    def __init__(self, data):
        self.data = data

    def wrap_paragraph(self, text):
        wrapped = textwrap.wrap(text, width=80)
        for line in wrapped:
            print(textwrap.indent(line, "    "))

    def poi_data_tables(self) -> PrettyTable:
        for poi in self.data["Data"]["pois"]:
            poi_table = PrettyTable()
            poi_table.field_names = ["POI", poi['name']]
            poi_table.align = "l"
            poi_table._max_width = {"POI": 15, poi["name"]: 80}
            if "description" in poi:
                poi_table.add_row(["Description", poi["description"]])
            if "category" in poi:
                poi_table.add_row(["Category", poi["category"]])
            if "rating" in poi:
                poi_table.add_row(["Rating", poi["rating"]])
            if "web_url" in poi:
                poi_table.add_row(["More info", poi["web_url"]])
            print(poi_table)

    def display_saved_data(self):
        if "City" in self.data:
            print(f"City: {self.data['City']}")
        elif "Region" in self.data:
            print(f"Region: {self.data['Region']}")
        if "description" in self.data["Data"]:
            print("Description:")
            self.wrap_paragraph(self.data["Data"]["description"])
        if "City" in self.data:
            print(f"Here are some places of interest in {self.data['City']}")
        elif "Region" in self.data:
            print(f"Here are some places of interest in {self.data['Region']}")
        self.poi_data_tables()
