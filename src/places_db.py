from file_handlers import *


# cities_by_country = CsvHandler.read_csv("resources/worldcities.csv")
# cities_database = {}
# for location in cities_by_country:
#     if location['country'] not in cities_database:
#         cities_database[location['country']] = {location['admin_name']: [location['city_ascii']]}
#     elif location['admin_name'] not in cities_database[location['country']]:
#         cities_database[location["country"]][location["admin_name"]] = [location["city_ascii"]]
#     elif location['city_ascii'] not in cities_database[location['country']][location['admin_name']]:
#         cities_database[location['country']][location['admin_name']].append(location['city_ascii'])

# print(cities_database['Korea, South'])
