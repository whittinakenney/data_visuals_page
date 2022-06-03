import numpy as np
import pandas as pd
import uuid
from datetime import datetime as dt

df1 = pd.read_csv(
    "TrafficData_Rand.csv",
    dtype=object,
)
df2 = pd.read_csv(
    "Time_Location_Rand_People.csv",
    dtype=object,
)
df3 = pd.read_csv(
    "N-Factor_RandomGenerated .csv"
)

xVal = ['LONG_SLEEVE', 'SHORT_SLEEVE', 'SHORTS', 'PANTS', 'HAT']

def item_counter(dataFrame):
    item_counter = []
    for item in xVal:
        count = 0
        for n in range(len(dataFrame[item])):
            if dataFrame[item][n] == 'TRUE':
                count += 1
        item_counter.append(count)
    return(item_counter)

def get_bar_color(domain):
    colors = [
        "#F4EC15",
        "#DAF017",
        "#BBEC19",
        "#9DE81B",
        "#80E41D",
        "#66E01F",
        "#4CDC20",
        "#34D822",
        "#24D249",
        "#25D042",
        "#26CC58",
        "#28C86D",
        "#29C481",
        "#2AC093",
        "#2BBCA4",
        "#2BB5B8",
        "#2C99B4",
        "#2D7EB0",
        "#2D65AC",
        "#2E4EA4",
        "#2E38A4",
        "#3B2FA0",
        "#4E2F9C",
        "#603099",
    ]
    colorVal = []
    for n in range(len(domain)):
        colorVal.append(colors[n])
    return colorVal

def create_map_df(df_with_coords):
    print(df_with_coords)
    lats = list(df_with_coords["LAT"])
    longs = list(df_with_coords['LONG'])
    ID_nums = list(df_with_coords["ID"])
    label_column = list(df_with_coords['LABEL'])
    list_ID_list = [] #creates df5 IDs column
    list_labels_lists = [] #creates labels column in df5
    colors = [] #creates colors column of df5
    lats_longs = list(set(tuple(zip(lats, longs))))
    unique_lats = []
    unique_longs = []
    for n in range(len(lats_longs)):
        unique_lats.append(lats_longs[n][0])
        unique_longs.append(lats_longs[n][1])
        ID_list = []
        labels = []
        for m in range(len(df_with_coords["LAT"])):
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
            colors.append('#8607A9')
        else:
            colors.append('#7FFF00')
    zipped = list(zip(number_of_detections, unique_lats, unique_longs,
            list_ID_list, list_labels_lists, colors))
    df5 = pd.DataFrame(zipped, columns=[
        "DETECTIONS",
        "LAT",
        "LONG",
        "IDnumber",
        "LABELS",
        "COLOR"]
        )
    return df5

df1_new = create_map_df(df1)
df2_new = create_map_df(df2)
labels = list(df1_new.LABELS) + list(df2_new.LABELS)

def get_text(map_df1, map_df2):
    labels = list(map_df1.LABELS) + list(map_df2.LABELS)
    total_detections = list(map_df1.DETECTIONS) + list(map_df2.DETECTIONS)
    text = []
    for n in range(len(labels)): #obj is a list in a list of label lists
        if len(labels[n]) == 1:
            text.append(labels[n])
        if len(labels[n]) != 1:
            text.append(total_detections[n])
    return text

def map_filter(clickData):
    person_feature = clickData["points"][0]["x"]
    return person_feature

def map_xval_yval(clickData):
    df1 = pd.read_csv(
        "TrafficData_Rand.csv",
        dtype=object,
    )
    df2 = pd.read_csv(
        "Time_Location_Rand_People.csv",
        dtype=object,
    )
    if clickData != None:
        person_feature = map_filter(clickData)
        #df1_by_feat = df1.loc[df1[vehicle_feature] == 'TRUE']
        df2_by_feat = df2.loc[df2[person_feature] == 'TRUE']
        print(df2_by_feat)
        #df1_new = create_map_df(df1_by_feat)
        df1_new = create_map_df(df1)
        df2_new = create_map_df(df2_by_feat)
        print(df2_new)

        vehicle_lats = list(df1_new.LAT)
        person_lats = list(df2_new.LAT)
        veh_per_lats = vehicle_lats + person_lats
        vehicle_longs = list(df1_new.LONG)
        person_longs = list(df2_new.LONG)
        veh_per_longs = vehicle_longs + person_longs

        vehicle_colors = list(df1_new.COLOR)
        person_colors = list(df2_new.COLOR)
        veh_per_colors = vehicle_colors + person_colors
    else:
        df1_new = create_map_df(df1)
        df2_new = create_map_df(df2)

        vehicle_lats = list(df1_new.LAT)
        person_lats = list(df2_new.LAT)
        veh_per_lats = vehicle_lats + person_lats
        vehicle_longs = list(df1_new.LONG)
        person_longs = list(df2_new.LONG)
        veh_per_longs = vehicle_longs + person_longs

        vehicle_colors = list(df1_new.COLOR)
        person_colors = list(df2_new.COLOR)
        veh_per_colors = vehicle_colors + person_colors
    return df1_new, df2_new, veh_per_lats, veh_per_longs, veh_per_colors

clickData = {'points': [{'curveNumber': 0, 'pointNumber': 12, 'pointIndex': 12, 'x': "HAT", 'y': 2, 'label': 12, 'value': 2, 'marker.color': '#29C481', 'bbox': {'x0': 630.15, 'x1': 658.94, 'y0': 530, 'y1': 530}}]}
print(map_filter(clickData))
print(map_xval_yval(clickData))