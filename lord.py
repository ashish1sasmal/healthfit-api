from pymongo import MongoClient
import pymongo

CONNECTION_STRING = ""
from pymongo import MongoClient

mongo = MongoClient(CONNECTION_STRING)["healthfit"]

doctorsDb = mongo["doctors"]
citiesDb = mongo["cities"]
specDb = mongo["speciality"]

import json

# f = open("THE_DATA/cities")
# data = json.load(f)
# citiesDb.insert_many(data)

# f = open("THE_DATA/speciality")
# data = json.load(f)
# specDb.insert_many(data)

# c = 0
# for i in range(20):
#     f = open(f'THE_DATA/sample{i}.json')
#     data = json.load(f)
#     doctorsDb.insert_many(data)
#     print(len(data))
#     c+=len(data)
# # doctorsDb.delete_many({})
# print(c)

f = open(f'doctors')
data = json.load(f)
doctorsDb.insert_many(data)