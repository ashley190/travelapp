import csv


class CsvHandler:
    @classmethod
    def read_csv(cls, file_path):
        with open(file_path, 'r') as csv_file:
            raw_csv = csv.DictReader(csv_file)
            python_list = list(raw_csv)
            return python_list




cities_by_country = CsvHandler.read_csv("worldcities.csv")
cities_database = {}
for location in cities_by_country:
    if location['country'] not in cities_database:
        cities_database[location['country']] = {location['admin_name']: [location['city_ascii']]}
    elif location['admin_name'] not in cities_database[location['country']]:
        cities_database[location['country']['admin_name']] = [location['city_ascii']]
    # elif location['admin_name'] in cities_database[location['country']]:
    #     cities_database[location['country']['admin_name']].append(location['city_ascii'])

print(cities_database['Malaysia']['Pulau Pinang'])