import textwrap
from prettytable import PrettyTable


class Display:
    def __init__(self, data):
        self.data = data

    def wrap_paragraph(self, text):
        wrapped = textwrap.wrap(text, width=80)
        for line in wrapped:
            print(textwrap.indent(line, "    "))

    def display_saved_data(self):
        print(f"City: {self.data['City']}")
        print("Description:")
        self.wrap_paragraph(self.data["Data"]["description"])
        print(f"Here are some places of interest in {self.data['City']}")
        # list_of_pois = self.data["Data"]["pois"]
        self.poi_data_tables()

    def poi_data_tables(self):
        for poi in self.data["Data"]["pois"]:
            # print(poi["name"])
            poi_table = PrettyTable()
            poi_table.field_names = ["POI", poi['name']]
            poi_table.align = "l"
            poi_table._max_width = {"POI": 15, poi["name"]: 80}
            if poi["description"]:
                poi_table.add_row(["Description", poi["description"]])
            if poi["category"]:
                poi_table.add_row(["Category", poi["category"]])
            if poi["rating"]:
                poi_table.add_row(["Rating", poi["rating"]])
            if poi["web_url"]:
                poi_table.add_row(["More info", poi["web_url"]])
            # poi_table.add_row(["", ""])
            print(poi_table)
