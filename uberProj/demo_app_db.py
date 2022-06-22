import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import uuid

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px
from pymongo import MongoClient

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Person Identification and Plate Identification"
server = app.server


# Plotly mapbox public token. This loads the map interface
mapbox_access_token = "pk.eyJ1Ijoid2hpdHRpbmFrZW5uZXkiLCJhIjoiY2wzbmRrbWR6MGRpZTNrbXU1OTN4NmJnYyJ9.GRJfLp1eHrnerFrpDqpzAw"

#important locations
important_locations = {
    "Emerging Technology Institute": {"lat": 34.83373, "lon": -79.18246},
    "14442C1031A059D700": {"lat": 34.83358, "lon": -79.18238}
}

class mongo_handler:
    ##below is the IOT local server MongoDB
    # def __init__(self):
    #     self.client = MongoClient('192.168.50.115', 27017)
    #     self.db = self.client['detections']
    ##below is the test MongoDB
    def __init__(self):
        self.client = MongoClient('45.79.221.195', 27017)
        self.db = self.client['detections']

    def get_vehicles(self): #creates a collection which the vehicle identifications will be added to as posts
        collection = self.db["vehicles"]
        return collection

    def get_people(self): #creates a collection which the people identifications will be added to as posts
        collection = self.db["people"]
        return collection

##test_server() allows you to check if you're connected to the server. Used mostl for the local server.
# def test_server():
#     md = mongo_handler()
#     try:
#         md.client.server_info()
#     except pymongo.errors.ServerSelectionTimeoutError:
#         print('not connected')
#         return False

#create_vehicle_df() takes the posts from the vehicle collection in the db and puts them into a dataframe
def create_vehicle_df():
    md = mongo_handler()
    try:
        cursor = list(md.get_vehicles().find({}))
        initial_post = list(cursor[0].keys())
        rows = []
        # for post in cursor:
        #     print(post['id'])
        for post in cursor:
            if len(list(post.keys())) > len(initial_post):
                columns = list(post.keys())
            else:
                columns = initial_post
            row = post.values()
            rows.append(row)
        vehicle_df = pd.DataFrame(rows, columns=columns)
    except IndexError:
        columns = ['_id', 'id', 'color', 'lat', 'lon', 'label', 'postprocess']
        vehicle_df = pd.DataFrame(columns=columns)
    return vehicle_df

#create_people_df() takes the posts from the people collection in the db and puts them into a dataframe
def create_people_df():
    md = mongo_handler()
    try:
        cursor = list(md.get_people().find({}))
        initial_post = list(cursor[0].keys())
        rows = []
        # for post in cursor:
        #     print(post['id'])
        for post in cursor:
            if len(list(post.keys())) > len(initial_post):
                columns = list(post.keys())
            else:
                columns = initial_post
            row = post.values()
            rows.append(row)
        people_df = pd.DataFrame(rows, columns=columns)
    except IndexError:
        columns = ['_id', 'id', 'color', 'lat', 'lon', 'label', 'postprocess']
        people_df = pd.DataFrame(columns=columns)
    return people_df

##update_vehicle_df and update_person_df recreate the vehicle and person dataframes in order to catch new
#posts and updated posts in the database.
def update_vehicle_df():
    df1 = create_vehicle_df()
    return df1

def update_person_df():
    df2 = create_people_df()
    return df2


#the below was a first attempt at updating the datafram
#However, it required checking every post in the database in order to search for new and updated posts.
#We instead replace the dataframe entirely each time the update functions are run.

##searches for new posts in vehicles collection and adds them to dataframe
##checks for updates to postprocessing, if something has been post-processed, it
##deletes the original row and adds the post-processed row
# def update_vehicle_df(df1):
#     if len(df1) == 0:
#         df1 = create_vehicle_df()
#     md = mongo_handler()
#     cursor = md.get_vehicles().find({}) #gets all posts in the collection
#     df1_post_ids = list(df1['_id']) #makes list of post id's already in df
#     post_ids_preprocess = list(df1.loc[df1['postprocess'] == False, '_id']) #gets those in current df1 that are -
#     #post-processed
#     last_row_index = len(df1_post_ids)
#     for post in cursor:
#         if post['postprocess'] in post_ids_preprocess and post['postprocess'] == True:
#             #if those in dataframe that are false for post-processing, share a post id with posts
#             #in the database, but the post is true for post-processing...
#             df1.drop(df1.index[df1['_id'] == post['_id']]) #we drop the old one from the df
#             df1.append(post, ignore_index=True)
#     cursor = md.get_vehicles().find({})
#     for post in cursor: #if there's a post with a post id that is not already in our df, we add it
#         if post['_id'] not in df1_post_ids:
#             df1.append(post, ignore_index=True)
#             # df1.loc[last_row_index] = post.values()
#             # last_row_index += 1
#     print(df1)
#     return df1
# ##this function is the same as the one above, but for the vehicle collection
# def update_people_df(df2):
#     if len(df2) == 0:
#         df2 = create_vehicle_df()
#     md = mongo_handler()
#     cursor = md.get_people().find({})
#     df2_post_ids = list(df2['_id'])
#     post_ids_preprocess = list(df2.loc[df2['postprocess'] == False, '_id'])
#     last_row_index = len(df2_post_ids)
#     for post in cursor:
#         if post['postprocess'] in post_ids_preprocess and post['postprocess'] == True:
#             df2.drop(df2.index[df2['_id'] == post['_id']])
#             df2.append(post, ignore_index=True)
#     cursor = md.get_people().find({})
#     for post in cursor:
#         if post['_id'] not in df2_post_ids:
#             df2.append(post, ignore_index=True)
#             # df2.loc[last_row_index] = post.values()
#             # last_row_index += 1
#     return df2

#returns list of veicle and person times which is useful for adding interactivity that filters data by time
def extract_all_times(df1, df2):
    vehicle_times = list(df1["time"])
    person_times = list(df2["time"])
    all_times_dates = vehicle_times + person_times #all the times which are in the yyyymmdd-hhmmss format
    return all_times_dates

#returns list of all years, months, and days in df
def extract_times(df1, df2):
    all_years = [] #just collects all the years
    all_months = []
    all_hours = []
    for time in extract_all_times(df1,df2):
        year = int(time[0:4])
        month = int(time[4:6])
        day = int(time[6:8])
        hour = int(time[9:11])
        date = (year, month, day)
        all_years.append(year)
        all_months.append(month)
        all_hours.append(hour)
        #date_time_array = [np.array(all_dates), np.array(all_times)]  # array of dates and times
    return (all_years, all_months, all_hours)

#Makes lists of hours IDs were collected
def all_IDs(df1, df2):
    Person_ID_list = list(df2["id"])
    Plate_Num_List = list(df1["id"])
    Vehicle_Person_IDs = Plate_Num_List + Person_ID_list
    return Vehicle_Person_IDs

#Collecting labels
def all_labels(df1, df2):
    Vehicle_Labels = list(df1["label"])
    People_Labels = list(df2["label"])
    Vehicle_People_Labels = Vehicle_Labels + People_Labels
    return Vehicle_People_Labels

#returns list of vehicle lat and lon, people lat and lon, vehicle and people
# lat and lons, then finally, unique vehicle and unique people locations.
def lats_long(df1, df2):
    Vehicle_Lats = list(df1["lat"])
    Vehicle_Longs = list(df1["long"])
    Vehicle_Lat_Long = tuple(zip(Vehicle_Lats, Vehicle_Longs))
    People_Lats = list(df2["lat"])
    People_Longs = list(df2["long"])
    People_Lat_Long = tuple(zip(People_Lats, People_Longs))
    Vehicle_People_Coords = Vehicle_Lat_Long + People_Lat_Long
    Vehicle_People_Lats = Vehicle_Lats + People_Lats
    Vehicle_People_Longs = Vehicle_Longs + People_Longs
    Unique_Vehicle_Locations = list(set(Vehicle_Lat_Long))
    Unique_People_Locations = list(set(People_Lat_Long))
    return(Vehicle_Lat_Long, People_Lat_Long, Vehicle_People_Lats,
           Vehicle_People_Longs, Unique_Vehicle_Locations, Unique_People_Locations)

#gives each unique location in the database a unique ID
#appends the ID and location to a dictionary which it returns
def dict_of_locations(df1, df2):
    (Vehicle_Lat_Long, People_Lat_Long, Vehicle_People_Lats,
    Vehicle_People_Longs, Unique_Vehicle_Locations,
    Unique_People_Locations) = lats_long(df1, df2)
    dict_of_All_detection_locations = {}

    for q in range(len(Vehicle_Lat_Long)):
        LocationID = uuid.uuid4() #Gives ID to every detection
        latitude = float(Vehicle_Lat_Long[q][0])
        longitude = float(Vehicle_Lat_Long[q][1])
        label = 'vehicle'
        dict_of_All_detection_locations[LocationID] = {"lat": latitude, "lon": longitude,
                                                       "label": label}
        for r in range(len(People_Lat_Long)):
            LocationID = uuid.uuid4()
            latitude2 = float(People_Lat_Long[r][0])
            longitude2 = float(People_Lat_Long[r][1])
            label2 = 'person'
            dict_of_All_detection_locations[LocationID] = {"lat": latitude2, "lon": longitude2,
                                                           "label": label2}
    list_of_locations = dict_of_All_detection_locations
    return list_of_locations

#add color code column to df4. vehicles are white and people are turquoise
def assign_color_label(row):
    if row['labels'] == 'vehicle':
        color = "#FFFFFF"
        return color
    if row['labels'] == 'person':
        color = "#8607A9"
        return color

##Creates datafram with person and vehicles which will include ID, TIME in standard format, LAT, LONG, LABEL, COLOR
def data_frame4(df1, df2): ###more to be done
    (Vehicle_Lat_Long, People_Lat_Long, Vehicle_People_Lats,
    Vehicle_People_Longs, Unique_Vehicle_Locations,
    Unique_People_Locations) = lats_long(df1, df2)
    all_times_dates = extract_all_times(df1, df2)
    standard_date_time_list = []
    for n in range(len(all_times_dates)):
        hour = int(all_times_dates[n][9:11])
        date_string = "{}-{}-{} {}:{}:{}".format(
            all_times_dates[n][0:4],
            all_times_dates[n][4:6],
            all_times_dates[n][6:8],
            hour,
            all_times_dates[n][11:13],
            all_times_dates[n][13:15]
        )
        reformatted_date = dt.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        standard_date_time_list.append(reformatted_date)
    Vehicle_Person_IDs = all_IDs(df1, df2)
    Vehicle_People_Labels = all_labels(df1, df2)
    zipped = list(zip(Vehicle_Person_IDs, standard_date_time_list,
                      Vehicle_People_Lats, Vehicle_People_Longs,
                      Vehicle_People_Labels
                      ))
    df4 = pd.DataFrame(zipped, columns=[
        "id",
        "time",
        "lat",
        "long",
        "labels"]
    )
    df4['color'] = df4.apply(lambda row: assign_color_label(row), axis=1)
    return df4

# Layout of Dash App
app.layout = html.Div(
    children=[
        #creates an interval compnenet which is used to update certain code every n intervals
        html.Div(id='live-update-csv'),
        dcc.Interval(
        id='interval-component',
        interval=2*1000,# in milliseconds
        n_intervals=0),
        #creates left column for bar graphs and counters
        html.Div(
                className="four columns div-user-controls",
                children=[
                    #adds dash logo above all visuals
                    html.A(
                            html.Img(
                                className="logo",
                                src=app.get_asset_url("dash-logo-new.png"),
                            ),
                            href="https://plotly.com/dash/",
                        ),
                    #layout for total unique detection counter
                    html.Div(
                        className='div-for-LED',
                        children=[
                            dbc.CardHeader(
                                "Total detections:",
                                style={
                                    "text-align": "left",
                                    "color": "white",
                                    "font-size": 18,
                                },
                            ),
                            dbc.CardBody(
                                [
                                    daq.LEDDisplay(
                                        id="rul-estimation-indicator-led",
                                        size=48,
                                        color="#80E41D",
                                        style={"color": "#black"},
                                        backgroundColor="#2b2b2b",
                                        value="0.0",
                                    )
                                ],
                                style={
                                    "text-align": "left",
                                    "width": "auto"
                                },
                            ),
                        ]
                    ),
                    html.Div(
                        className='div-split-detections',
                        children=[
                                html.P(id="total-people-detections"),
                                html.P(id="total-vehicle-detections"),
                        ],
                        style={"text-align": "left"}
                    ),
                    html.Div(
                            className='div-for-bar-panel',
                            children=[
                                html.Div(
                                    className='div-for-gender-bar',
                                    children=[
                                        dcc.Graph(id="gender-bar",
                                            style={
                                                "text-align": "left",
                                                "width": "auto"
                                            }
                                        ),
                                    ]
                                ),
                                html.Div(
                                    className='div-for-hair-bar',
                                    children=[
                                        dcc.Graph(id="hair-bar",
                                                  style={
                                                      "text-align": "left",
                                                      "width": "auto"
                                                  }
                                                  ),
                                    ]
                                ),
                                html.Div(
                                    className='div-for-car-bar',
                                    children=[
                                        dcc.Graph(id="car-bar",
                                                  style={
                                                      "text-align": "left",
                                                      "width": "auto"
                                                  }
                                        )
                                    ]
                                )
                            ]
                        ),
                    # html.Div(
                    #     className='div-clear-button',
                    #     children=[
                    #         html.Div([
                    #             html.Button('Reset Bar Selection', id='btn-nclicks-1', n_clicks=0),
                    #             html.Div(id='container-button-timestamp')])]
                    # )
                    ]
                ),
        #making layout for map
        html.Div(
            # className="row",
            children=[
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph")
                    ],
                ),
            ],
        )
    ]
)

##wanted a botton which would reset the clickData
##saved here for later use when interactivity is added
# @app.callback(
#     [Output('btn-nclicks-1', 'n_clicks'), Output('gender-bar', 'clickData')],
#     [Input('btn-nclicks-1', 'n_clicks'), Input('gender-bar', 'clickData')]
# )
# def update_output(n_clicks, clickData):
#     print(clickData)
#     if n_clicks >= 1:
#         clickData = None
#         #clickData2 = None
#         n_clicks = 0
#     return n_clicks, clickData
# # Gets the amount of days in the specified month
# # Index represents month (0 is Jan, 1 is Feb, ... etc.)
# daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#
# # Get index for the specified month in the dataframe
# monthIndex = pd.Index(["Jan", "Feb", "Mar", "Apr", "May",
#                        "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"])

##count_per_hour takes the year, month, and day and creates a list of counts
#each count is the list is how many detections were at that hour on that day
def count_per_hour(year, month, day):
    hour_of_detection = []
    detections_by_hour = []
    df4 = data_frame4(df1, df2)
    for n in range(len(list(df4["time"]))):
        if (df4['time'][n].year == year and
            df4['time'][n].month == month and
            df4['time'][n].day == day
        ):
            for m in range(24):
                if df4['time'][n].hour == m:
                    hour_of_detection.append(m)
    for p in range(24):
        detections_by_hour.append(hour_of_detection.count(p))
    return detections_by_hour

#the led display that counts number of unique detections in both the vehicle and people collections
@app.callback(Output("rul-estimation-indicator-led", "value"), Input("interval-component", "n_intervals"))
def update_total_detections(n):
    df1 = update_vehicle_df()
    df2 = update_person_df()
    total_detections = all_IDs(df1, df2)
    unique_detections = list(set(total_detections))
    unique_det_without_nan = [x for x in unique_detections if pd.isnull(x) == False and x != 'nan']
    return len(unique_det_without_nan)

#under led display, this counts number of unique detections that are person detections
@app.callback(Output("total-people-detections", "children"), Input("interval-component", "n_intervals"))
def update_people_detections(n):
    df2 = update_person_df()
    people_ids = df2.id
    unique_ids = list(set(people_ids))
    unique_ids_without_nan = [x for x in unique_ids if pd.isnull(x) == False and x != 'nan']
    return "People detected: {:,d}".format(
        len(unique_ids_without_nan)
    )

#under led display, this counts number of unique detections that are vehicle detections
@app.callback(Output("total-vehicle-detections", "children"), Input("interval-component", "n_intervals"))
def update_vehicle_detections(n):
    df1 = update_vehicle_df()
    vehicle_ids = df1.id
    unique_ids = list(set(vehicle_ids))
    unique_ids_without_nan = [x for x in unique_ids if pd.isnull(x) == False and x != 'nan']
    return "Vehicles detected: {:,d}".format(
        len(unique_ids_without_nan)
    )

#item_counter requires a dataframe and a list of items.
#For example, a list of items may be ['long_sleeves', 'male']
#counts how many trues are in the dataframe column of each item in the domain
#For example, if there are 2 people in the database wearing long sleeves and 5 males
#this will return [2, 5]
def item_counter(dataFrame, domain):
    item_counter = []
    for item in domain:
        count = 0
        for n in range(len(dataFrame[item])):
            if dataFrame[item][n] == ('true' or 1 or True):
                count += 1
        item_counter.append(count)
    return(item_counter)

#Given date and time, this function will return a database with the ID, TIME, LAT, LONG, and LABEL
#that correspond to that specific date and time. Time is the index.
def getLatLonColor(selectedData, month, day):
    df1 = update_vehicle_df()
    df2 = update_person_df()
    all_times_dates = extract_all_times(df1, df2)
    df4 = data_frame4(df1, df2)
    include_rows = []
    include_rows_2 = []
    for n in range(len(all_times_dates)):
        if df4['time'][n].month == month and df4['time'][n].day == day:
            include_rows.append(n)
    listCoords = df4.iloc[include_rows]
    list_qualified_dates = list(listCoords['time'])
#No times selected, output all times for chosen month and date
    if selectedData == None or len(selectedData) == 0:
        listCoords = listCoords.set_index('time')
        return listCoords
    for time in selectedData:
        for m in range(len(list_qualified_dates)):
            hour_at_row_m = "{}".format(list_qualified_dates[m].hour)
            if hour_at_row_m == time:
                include_rows_2.append(m)
    listCoords_byHours = listCoords.iloc[include_rows_2]
    listCoords_byHours = listCoords_byHours.set_index('time')
    if len(selectedData) != 0:
        return listCoords_byHours

#create_map_df creates a unique dataframe that is used for the map
#it finds all the unique locations in the database
#it finds all the detections at each of those unique locations
#it counts how many detections are at each unique locations
#it creates a list of all the IDs at each unique location
#it assigns a color whether the detection at a unique location is a person, vehicle,
# or several detections at the same location
#all this information is then stored in df5 which it returns
def create_map_df(df_with_coords):
    if 'lat' in df_with_coords.columns:
        lats = list(df_with_coords["lat"])
        longs = list(df_with_coords['lon'])
    else:
        lats = []
        longs = []
    ID_nums = list(df_with_coords["id"])
    label_column = list(df_with_coords['label'])
    list_ID_list = [] #creates df5 IDs column
    list_labels_lists = [] #creates labels column in df5
    colors = [] #creates colors column of df5
    lats_longs = list(set(tuple(zip(lats, longs))))#takes only unique lat, lon combinations
    unique_lats = []
    unique_longs = []
    for n in range(len(lats_longs)):
        unique_lats.append(lats_longs[n][0])
        unique_longs.append(lats_longs[n][1])
        ID_list = []
        labels = []
        for m in range(len(df_with_coords["lat"])):
            if (lats[m] == lats_longs[n][0] and
                    longs[m] == lats_longs[n][1]):
                ID_list.append(ID_nums[m])
                labels.append(label_column[m])
        list_ID_list.append(ID_list)
        list_labels_lists.append(labels)
    number_of_detections = [] #creates number of detections column in df5
    for IDlist in list_ID_list:
        p = len(IDlist)
        number_of_detections.append(p)
    for label_list in list_labels_lists:
        if len(label_list) == 1 and label_list == ['vehicle']:
            colors.append('#FFFFFF')
        elif len(label_list) == 1 and label_list == ['person']:
            colors.append('#2BB5B8')
        else:
            colors.append('#7FFF00')
    zipped = list(zip(number_of_detections, unique_lats, unique_longs,
            list_ID_list, list_labels_lists, colors))
    df5 = pd.DataFrame(zipped, columns=[
        "detections",
        "lat",
        "long",
        "id",
        "labels",
        "color",
    ]
        )
    return df5

#get_text creates the hover texts for points on the map
def get_text(map_df1, map_df2):
    all_labels = list(map_df1.labels) + list(map_df2.labels)
    Unique_IDs = list(map_df1.id) + list(map_df2.id)
    total_detections = list(map_df1.detections) + list(map_df2.detections)
    text = []
    for n in range(len(all_labels)): #obj is a list in a list of label lists
        if len(all_labels[n]) == 1:
            text.append((all_labels[n], Unique_IDs[n]))
        if len(all_labels[n]) != 1:
            text.append((total_detections[n], Unique_IDs[n]))
    return text

##used when interactivity is added
# def map_filter(clickData):
#     person_feature = clickData["points"][0]["x"]
#     return person_feature

def map_xval_yval():
    df1 = update_vehicle_df()
    df2 = update_person_df()
    # if clickData != None:
    #     person_feature = map_filter(clickData)
    #     #df1_by_feat = df1.loc[df1[vehicle_feature] == 'TRUE']
    #     df2_by_feat = df2.loc[df2[person_feature] == 'TRUE']
    #     #df1_new = create_map_df(df1_by_feat)
    #     df1_new = create_map_df(df1)
    #     df2_new = create_map_df(df2_by_feat)
    #
    #     vehicle_lats = list(df1_new.LAT)
    #     person_lats = list(df2_new.LAT)
    #     veh_per_lats = vehicle_lats + person_lats
    #     vehicle_longs = list(df1_new.LONG)
    #     person_longs = list(df2_new.LONG)
    #     veh_per_longs = vehicle_longs + person_longs
    #
    #     vehicle_colors = list(df1_new.COLOR)
    #     person_colors = list(df2_new.COLOR)
    #     veh_per_colors = vehicle_colors + person_colors
    # else:
    df1_new = create_map_df(df1)
    df2_new = create_map_df(df2)

    vehicle_lats = list(df1_new.lat)
    person_lats = list(df2_new.lat)
    veh_per_lats = vehicle_lats + person_lats
    vehicle_longs = list(df1_new.long)
    person_longs = list(df2_new.long)
    veh_per_longs = vehicle_longs + person_longs

    vehicle_colors = list(df1_new.color)
    person_colors = list(df2_new.color)
    veh_per_colors = vehicle_colors + person_colors
    return df1_new, df2_new, veh_per_lats, veh_per_longs, veh_per_colors

def initial_map():
    zoom = 14.0
    latInitial = 34.83363
    lonInitial = -79.18255
    bearing = 0
    map = go.Figure(
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # ETI lat and long 34.83363, -79.18255
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        # "mapbox.zoom": 12,
                                        "mapbox.center.lon": "-79.18255",
                                        "mapbox.center.lat": "34.83363",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )
    return map

map = initial_map() #In order to run off wifi, we only want the map token to be loaded once

@app.callback(
    Output("map-graph", "figure"),
    [
        Input("interval-component", "n_intervals")
    ],
)
def update_graph(n):#date, time in string format, location
    df1_new, df2_new, veh_per_lats, veh_per_longs, veh_per_colors = map_xval_yval()

    return map.update(
        data=[
            Scattermapbox(
                lat=[important_locations[i]["lat"] for i in important_locations],
                lon=[important_locations[i]["lon"] for i in important_locations],
                mode="markers",
                hoverinfo="text",
                text=[i for i in important_locations],
                marker=dict(size=8, color="#A91007", allowoverlap=True),
            ),
            Scattermapbox(
                lat=veh_per_lats,
                lon=veh_per_longs,
                mode="markers",
                hoverinfo="lat+lon+text",
                text=get_text(df1_new, df2_new),
                marker=dict(size=5, color=veh_per_colors, allowoverlap=True)
            )
        ])

def percent_sex(people_df): #change to total or add unknown
    if 'sex' in people_df.columns:
        count_f = 0
        count_m = 0
        count_u = 0
        gender_list = people_df['sex']
        gender_wo_nan = [x for x in gender_list if pd.isnull(x) == False and x != 'nan']
        for gender in gender_wo_nan:
            if int(gender) == 0:
                count_f += 1
            if int(gender) == 1:
                count_m += 1
        count_u = len(gender_list) - len(gender_wo_nan)
        percent_female = (count_f/len(gender_list)) * 100
        percent_male = (count_m/len(gender_list)) * 100
        percent_unknown = (count_u/len(gender_list)) * 100
    else:
        percent_female = 0
        percent_male = 0
        percent_unknown = 100
    return percent_female, percent_male, percent_unknown

@app.callback(
    Output("gender-bar", "figure"),
    Input("interval-component", "n_intervals"))
def update_sex_chart(n):
    df2 = update_person_df()
    percent_female, percent_male, percent_unknown = percent_sex(df2)
    percentages = [percent_female, percent_male, percent_unknown]
    sex = ["Female", "Male", "Unknown"]
    graph_colors = px.colors.sequential.Viridis
    fig = go.Figure()
    for n in range(len(sex)):
        fig.add_trace(go.Bar(
            y=['people  '],
            x=[percentages[n]],
            name=sex[n],
            orientation='h',
            marker=dict(
                color=graph_colors[n],
                line=dict(color='#FFFFFF', width=1)
            )
        ))

    fig.update_layout(barmode='stack', width=350, height=100, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      font_color='#FFFFFF', margin=dict(l=0, r=20, t=20, b=20))
    return fig

def percent_car_color(vehicle_df):
    if 'paint' in vehicle_df.columns:
        paint_list = list(vehicle_df['paint'])
        colors = list(set(paint_list))
        colors_without_nan = [x for x in colors if pd.isnull(x) == False and x != 'nan']
        percents = []
        for color in colors_without_nan:
            count = 0
            for n in range(len(paint_list)):
                if color == paint_list[n]:
                    count += 1
            percent = (count/len(paint_list)) * 100
            percents.append(percent)
    else:
        percents = [0]
        colors_without_nan = ['unknown']

    return percents, colors_without_nan

@app.callback(
    Output("car-bar", "figure"),
    Input("interval-component", "n_intervals"))
def update_car_bar(n):
    df1 = update_vehicle_df()
    percents, colors = percent_car_color(df1)
    graph_colors = px.colors.sequential.Viridis
    percent_unknown = 100 - sum(percents)
    fig = go.Figure()
    for n in range(len(percents)):
        fig.add_trace(go.Bar(
            y=['vehicles '],
            x=[percents[n]],
            name=colors[n],
            orientation='h',
            marker=dict(
                color=graph_colors[n],
                line=dict(color='#FFFFFF', width=1)
            )
        ))
        last_color = n + 1
    fig.add_trace(go.Bar(
        y=['vehicles '],
        x=[percent_unknown],
        name='unknown',
        orientation='h',
        marker=dict(
            color=graph_colors[last_color],
            line=dict(color='#FFFFFF', width=1)
        )
    ))

    fig.update_layout(barmode='stack', width=350, height=100, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      font_color='#FFFFFF', margin=dict(l=0, r=20, t=20, b=20))
    return fig

def clothes_totals(person_df, factor:str): #factor is an n-factor like "hat." It's column should be 0's and 1's
    filtered_df = person_df[~person_df[factor].isnull()]
    factor_list = [int(i) for i in filtered_df[factor]]
    total_true = sum(factor_list)
    total_false = len(factor_list) - total_true
    total_unknown = len(person_df[factor]) - len(filtered_df)
    return total_true, total_false, total_unknown #tells you total trues for each factor and total false

@app.callback(
    Output("hair-bar", "figure"),
    Input("interval-component", "n_intervals"))
def update_hair_bar(n):
    df2 = update_person_df()
    if 'hair' in df2.columns:
        short_hair_count, long_hair_count, unknown = clothes_totals(df2, 'hair')
        graph_colors = px.colors.sequential.Viridis
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=['hair'],
            x=[short_hair_count],
            name='short hair',
            orientation='h',
            marker=dict(
                color=graph_colors[2],
                line=dict(color='#FFFFFF', width=1)
            )
        ))
        fig.add_trace(go.Bar(
            y=['hair'],
            x=[long_hair_count],
            name='long hair',
            orientation='h',
            marker=dict(
                color=graph_colors[4],
                line=dict(color='#FFFFFF', width=1)
            )
        ))
        fig.add_trace(go.Bar(
            y=['hair'],
            x=[unknown],
            name='unknown',
            orientation='h',
            marker=dict(
                color=graph_colors[6],
                line=dict(color='#FFFFFF', width=1)
            )
        ))
    else:
        graph_colors = px.colors.sequential.Viridis
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=['N/A'],
            x=[1],
            name='hair',
            orientation='h',
            marker=dict(
                color=graph_colors[6],
                line=dict(color='#FFFFFF', width=1)
            )
        ))
    fig.update_layout(barmode='stack', width=350, height=100, plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)',
                          font_color='#FFFFFF', margin=dict(l=0, r=20, t=20, b=20))
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)