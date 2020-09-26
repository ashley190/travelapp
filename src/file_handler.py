import csv
import json


class CsvHandler:
    @classmethod
    def read_csv(cls, file_path):
        try:
            with open(file_path, 'r') as csv_file:
                raw_csv = csv.DictReader(csv_file)
                python_list = list(raw_csv)
                return python_list
        except FileNotFoundError:
            return None


class JsonHandler:
    @classmethod
    def read_json(cls, path):
        try:
            with open(path, "r") as json_file:
                json_string = json_file.read()
                return json.loads(json_string)
        except FileNotFoundError:
            return []

    @classmethod
    def write_json(cls, path, data):
        with open(path, "w") as json_file:
            json_string = json.dumps(data)
            json_file.write(json_string)


class FileConverter:
    @classmethod
    def save_csv_as_json(cls, csv_path, json_path):
        python_list = CsvHandler.read_csv(csv_path)
        JsonHandler.write_json(json_path, python_list)


# convert worldcities from csv to json format
FileConverter.save_csv_as_json("resources/worldcities.csv", "resources/worldcities.json")


class UserFile:
    def __init__(self, path):
        self.path = path
        self.past_searches = set()

    def save_data(self, region, data):
        final_format = {"City": region, "Data": data}
        content = JsonHandler.read_json(self.path)
        content.append(final_format)
        JsonHandler.write_json(self.path, content)

    def check_duplicates(self, region):
        if region in self.past_searches:
            return True
        elif region not in self.past_searches:
            self.past_searches.add(region)
            return False


# saved = UserFile("resources/saved.json")
# saved.past_searches = {('Tōkyō', 'Japan')}
# saved.check_duplicates(('New York', 'United States'))
# print(saved.past_searches)
# print(saved.check_duplicates(('Tōkyō', 'Japan')))
# if saved.check_duplicates(('Brooklyn', 'United States')):
#     print("yes")
# else:
#     print("no")
# print(saved.past_searches)
