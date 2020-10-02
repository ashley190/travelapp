import csv
import json


class CsvHandler:
    """Contains method(s) that interact with csv files"""

    @classmethod
    def read_csv(cls, file_path: str) -> list:
        """Attempts to generate a dictionary from csv data.

        Attempts to read a csv file into a dictionary format
        with csv headers as key and row data as values;
        then convert into a list of dictionaries.

        Args:
            file_path (str): file path pointing to csv file
                to be read

        Returns:
            list: If succssful, a list of dictionaries with
                each dictionary representing a row of csv
                data in a dictionary format with the csv
                headers as keys and row data as values. Blank
                list returned if no csv file found.
        """
        try:
            with open(file_path, 'r') as csv_file:
                raw_csv = csv.DictReader(csv_file)
                python_list = list(raw_csv)
                return python_list
        except FileNotFoundError:
            return []


class JsonHandler:
    @classmethod
    def read_json(cls, path: str) -> list:
        """Reads json into python data.

        Attempts to open a json file in read mode; read
        contents of json file and decodes json data into python
        data.

        Args:
            path (str): file path pointing to json file to
                be read.

        Returns:
            list: If successful, a list containing decoded json
                data returned. Blank list returned if no valid
                json file found.
        """
        try:
            with open(path, "r") as json_file:
                json_string: str = json_file.read()
                return json.loads(json_string)
        except FileNotFoundError:
            return []

    @classmethod
    def write_json(cls, path: str, data):
        """Encodes and save python data into json format

        Args:
            path (str): file path pointing to location of json
                file to be opened in write mode.
            data : python data to be encoded into json format
        """
        with open(path, "w") as json_file:
            json_string: str = json.dumps(data)
            json_file.write(json_string)


class FileConverter:
    """Contains method to convert csv file to json."""
    @classmethod
    def save_csv_as_json(cls, csv_path: str, json_path: str):
        """Convert csv file into json.

        Reads csv file data from a file into python data;
        then convert python data into json and saved in a
        json file

        Args:
            csv_path (str): file path pointing to csv file
                to be read.
            json_path (str): file path pointing to json file to
                be saved.
        """
        python_list: list = CsvHandler.read_csv(csv_path)
        JsonHandler.write_json(json_path, python_list)


# convert external worldcities file from csv to json format
FileConverter.save_csv_as_json(
    "resources/worldcities.csv",
    "resources/worldcities.json")
