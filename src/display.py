import textwrap
from prettytable import PrettyTable     # type: ignore


class Display:
    """Creates Display object for data display"""

    def __init__(self, data: dict):
        """Initialises object with a data instance attribute.

        Initialise Display object with a data attribute
        containing a pre-formatted dictionary to be displayed.

        Args:
            data (dict): Dictionary with pre-formatted data.
                This dictionary is generated by the 
                read_flag_and_save method of a UserFile object.
        """
        self.data = data

    def wrap_paragraph(self, text: str):
        """Wraps long lines of text into a maximum width of 80.

        Args:
            text (str): long text to be wrapped
        """        
        wrapped = textwrap.wrap(text, width=80)
        for line in wrapped:
            print(textwrap.indent(line, "    "))

    def poi_data_tables(self) -> PrettyTable:
        """Encapsulates poi data into individual tables.

        Generates one table per poi in self.data["Data"]["pois"]

        Returns:
            PrettyTable: One table containing details of each poi.
        """        
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
        """Consolidates and prints data.

        Consolidates data to be printed from self.data and prints data
        with region/city level with its description followed by poi tables
        with details of each poi.
        """        
        if "City" in self.data:
            print(f"City: {self.data['City'][0]}, {self.data['City'][1]}")
        elif "Region" in self.data:
            print(f"Region: {self.data['Region'][0]}, {self.data['Region'][1]}")
        if "description" in self.data["Data"]:
            print("Description:")
            self.wrap_paragraph(self.data["Data"]["description"])
        if "City" in self.data:
            print(f"Here are some places of interest in {self.data['City'][0]}, {self.data['City'][1]}")
        elif "Region" in self.data:
            print(f"Here are some places of interest in {self.data['Region'][0]}, {self.data['Region'][1]}")
        self.poi_data_tables()
