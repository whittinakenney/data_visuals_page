import pymongo
import numpy as np
import datetime
import pandas as pd
from pymongo import MongoClient

client = MongoClient('45.79.221.195', 27017)

def reupload_csv():
    db = client['test-database']
    posts = db.posts
    df1 = pd.read_csv('Time_Location_Rand_People.csv')
    post1 = df1.to_dict(orient='split')
    post_id1 = posts.insert_one(post1).inserted_id

    df2 = pd.read_csv('TrafficData_Rand.csv')
    post2 = df2.to_dict(orient='split')
    post_id2 = posts.insert_one(post2).inserted_id
    return(post_id1, post_id2)

def reload_dataframe():
        db = client['test-database']
        posts = db.posts
        post_id1, post_id2 = reupload_csv()
        new_df1 = pd.DataFrame(columns=posts.find_one(post_id1)['columns'])
        for idx,row in zip(posts.find_one(post_id1)['index'],posts.find_one(post_id1)['data']):
                new_df1.loc[idx] = row
        new_df2 = pd.DataFrame(columns=posts.find_one(post_id2)['columns'])
        for idx,row in zip(posts.find_one(post_id2)['index'],posts.find_one(post_id2)['data']):
                new_df2.loc[idx] = row
        return(new_df1, new_df2)
df1, df2 = reload_dataframe()
print(type(df2["LAT"][0]))