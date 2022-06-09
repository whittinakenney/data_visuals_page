import numpy as np
from pymongo import MongoClient
import pymongo
import pandas as pd
from csv import reader
import json


class mongo_handler:
    # def __init__(self):
    #     self.client = MongoClient('192.168.50.115', 27017)
    #     self.db = self.client['detections']
    def __init__(self):
        self.client = MongoClient('45.79.221.195', 27017)
        self.db = self.client['detections']

    def get_vehicles(self):
        collection = self.db["vehicles"]
        return collection

    def get_people(self):
        collection = self.db["people"]
        return collection

md = mongo_handler()
cursor = md.get_people().find({})
print(cursor)

def create_people_df():
    md = mongo_handler()
    cursor = md.get_people().find({})
    initial_post = list(cursor[0].keys())
    rows = []
    for post in cursor:
        if len(list(post.keys())) > len(initial_post):
            columns = list(post.keys())
        else:
            columns = initial_post
        row = post.values()
        rows.append(row)
    #columns = np.unique(columns)
    people_df = pd.DataFrame(columns=columns)
    for i in range(len(rows)):
        people_df.loc[i] = rows[i]
    return people_df
df = create_people_df()

def update_people_df(df):
    md = mongo_handler()
    cursor = md.get_people().find({})
    df_post_ids = list(df['_id'])
    post_ids_preprocess = list(df.loc[df['postprocess'] == False, '_id'])
    last_row_index = len(df_post_ids) + 1
    for post in cursor:
        if post['postprocess'] in post_ids_preprocess and post['postprocess'] == True:
            df.drop(df.index[df['_id'] == post['_id']])
            df.loc[last_row_index] = list(post.values())
            last_row_index += 1
    for post in cursor:
        if post['_id'] not in df_post_ids:
            df.loc[last_row_index] = post.values()
            last_row_index += 1
    return df
print(update_people_df(df))

important_locations = {
    "Emerging Technology Institute": {"lat": 34.83373, "lon": -79.18246},
    "14442C1031A059D700": {"lat": 34.83358, "lon": -79.18238}
}

# def update_important_locations(df, important_locations):
#     if 'camera' in df.columns:
#         titles = list(df.camera)
#         unique_titles = list(set(titles))
#         for n in range(len(unique_titles)):
#             lats = list(df.loc[df['camera'] == '14442C1031A059D700', 'id'])
#             longs = list(df.loc[df['camera'] == '14442C1031A059D700', 'id'])
#             important_locations[unique_titles[n]] = {"lat": lats[0], "long": longs[0]}
#     return important_locations
# print(update_important_locations(update_people_df(df), important_locations))

    # def update_vehicles(self, post):
    #     collection = self.db["vehicles"]
    #     frame = self.dataframe_to_dict(post)
    #     post_id = collection.insert_one(frame).inserted_id
    #     return post_id
    #
    # def update_people(self, post):
    #     collection = self.db["people"]
    #     frame = self.dataframe_to_dict(post)
    #     post_id = collection.insert_one(frame).inserted_id
    #     return post_id

# def example_update():
#     # Create an instance of the class
#     # This is needed to intialized class variables
#     md = mongo_handler()
#     md.get_vehicles().drop()
#     md.get_people().drop()
#     # Create a pd to upload to the database
#     people = pd.read_csv('Time_Location_Rand_People.csv')
#     # Then we can update the database with the new data
#     md.update_people(people)
#     # Here we can do the same thing with vehicles
#     vehicles = pd.read_csv('TrafficData_Rand.csv')
#     md.update_vehicles(vehicles)
#     cursor = md.get_vehicles().find({})
#     vehicle_collection = md.get_vehicles()
#     vehicle_posts = md.db['vehicles'].count_documents({})
#     for n in range(vehicle_posts):
#         print(cursor[n])
#     print(type(vehicle_posts))
#     #pull data from db and convert to df
#     # cursor = md.get_vehicles().find({})
#     # table = cursor[0]
#     # df1 = pd.DataFrame(index=table['index'], columns=table['columns'], data=table['data'])
#     # cursor2 = md.get_people().find({})
#     # table = cursor2[0]
#     # df2 = pd.DataFrame(index=table['index'], columns=table['columns'], data=table['data'])

# BBox = (-79.1884, -79.1804, 34.8442, 34.8288) #OpenStreetMap longmin, longmax, latmin, latmax
#
# fig, ax = plt.subplots(figsize=(8, 7))
# ax.scatter(veh_per_longs, veh_per_lats, zorder=1, alpha=0.2, c='b', s=10)
# ax.scatter(
#     x=[important_locations[i]["lon"] for i in important_locations],
#     y=[important_locations[i]["lat"] for i in important_locations],
#     mode="markers",
#     hoverinfo="text",
#     text=[i for i in important_locations],
#     marker=dict(size=8, color="#A91007", allowoverlap=True),
#     ),
# ax.scatter(
#     x=veh_per_longs,
#     y=veh_per_lats,
#     mode="markers",
#     hoverinfo="lat+lon+text",
#     text=get_text(df1_new, df2_new),
#     marker=dict(size=5, color=veh_per_colors, allowoverlap=True)
#             )
#     ])
# ax.set_title('Live Detections')
# ax.set_xlim(BBox[0], BBox[1])
# ax.set_ylim(BBox[2], BBox[3])
# ax.imshow(map, zorder=0, extent=BBox, aspect='equal')



