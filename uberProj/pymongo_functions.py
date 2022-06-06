from pymongo import MongoClient
import pandas as pd
from csv import reader
import json

#goal: post each row in csv as its own post
#write function that checks for new post id
#create dataframe of every post

class mongo_handler:
    def __init__(self):
        self.client = MongoClient('45.79.221.195', 27017)
        self.db = self.client['detections']

    def dataframe_to_dict(self, post):
        dataframe = post.to_dict(orient='split')
        return dataframe

    def get_vehicles(self):
        collection = self.db["vehicles"]
        return collection

    def get_people(self):
        collection = self.db["people"]
        return collection

    def update_vehicles(self, post):
        collection = self.db["vehicles"]
        frame = self.dataframe_to_dict(post)
        post_id = collection.insert_one(frame).inserted_id
        print(post_id)
        return post_id

    def update_people(self, post):
        collection = self.db["people"]
        frame = self.dataframe_to_dict(post)
        post_id = collection.insert_one(frame).inserted_id
        print(post_id)
        return post_id

def example_update():
    # Create an instance of the class
    # This is needed to intialized class variables
    md = mongo_handler()
    md.get_vehicles().drop()
    md.get_people().drop()
    # Create a pd to upload to the database
    people = pd.read_csv('Time_Location_Rand_People.csv')
    # Then we can update the database with the new data
    md.update_people(people)
    # Here we can do the same thing with vehicles
    vehicles = pd.read_csv('TrafficData_Rand.csv')
    md.update_vehicles(vehicles)
    #pull data from db and convert to df
    cursor = md.get_vehicles().find({})
    table = cursor[0]
    df1 = pd.DataFrame(index=table['index'], columns=table['columns'], data=table['data'])
    cursor2 = md.get_people().find({})
    table = cursor2[0]
    df2 = pd.DataFrame(index=table['index'], columns=table['columns'], data=table['data'])
    return df1, df2

 with open('Time_Location_Rand_People.csv' 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                print(row)

