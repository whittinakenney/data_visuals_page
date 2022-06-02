import pymongo
import numpy as np
import datetime
import csv
import json
import pandas as pd
import sys, getopt, pprint
import pandas as pd
from pymongo import MongoClient

#CSV to JSON Conversion
# vehiclefile = open('TrafficData_Rand.csv', 'r')
# reader = csv.DictReader( vehiclefile )
#
client = MongoClient('45.79.221.195', 27017)
db = client['test-database']


posts = db.posts

# df1 = pd.read_csv('Time_Location_Rand_People.csv')
# post1 = df1.to_dict(orient='split')
# post_id1 = posts.insert_one(post1).inserted_id
#
# df2 = pd.read_csv('TrafficData_Rand.csv')
# post2 = df2.to_dict(orient='split')
# post_id2 = posts.insert_one(post2).inserted_id
#
# new_df1 = pd.DataFrame(columns=posts.find_one(post_id1)['columns'])
# for idx,row in zip(posts.find_one(post_id1)['index'],posts.find_one(post_id1)['data']):
#     new_df1.loc[idx] = row
# new_df2 = pd.DataFrame(columns=posts.find_one(post_id2)['columns'])
# for idx,row in zip(posts.find_one(post_id2)['index'],posts.find_one(post_id2)['data']):
#     new_df2.loc[idx] = row

cursor=posts.find({})#how to get specific post
for doc in cursor:
    print(doc)
