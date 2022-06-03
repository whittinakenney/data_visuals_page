import numpy as np
import pandas as pd
from plotly import graph_objs as go
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

def percent_car_color(vehicle_df):
    paint_list = list(vehicle_df['PAINT'])
    colors = set(paint_list)
    percents = []
    for color in colors:
        count = 0
        for n in range(len(paint_list)):
            if color == paint_list[n]:
                count += 1
        percent = (count/len(paint_list)) * 100
        percents.append(percent)
    return percents

def item_counter(dataFrame, domain):
    item_counter = {}
    for item in domain:
        count = 0
        for n in range(len(dataFrame[item])):
            if dataFrame[item][n] == 'TRUE':
                count += 1
        item_counter[item] = count
    no_hats = len(dataFrame['HAT']) - item_counter['HAT']
    item_counter['NO_HAT'] = no_hats
    return(item_counter)

def count_car_color(vehicle_df):
    paint_list = list(vehicle_df['PAINT'])
    colors = set(paint_list)
    car_color_count = {}
    for color in colors:
        count = 0
        for n in range(len(paint_list)):
            if color == paint_list[n]:
                count += 1
        car_color_count[color] = count
    return car_color_count

# def get_y_lists(people_item_count, car_color_count, x):
#     y_lists = {}
#     for x_val in x:
#         if x_val == 'top':
#             y_lists[x_val]={'long_sleeve': people_item_count["LONG_SLEEVE"],
#                             'short_sleeve': people_item_count['SHORT_SLEEVE'],
#                             'shorts': 0,
#                             'pants': 0,
#                             'hats': 0,
#                             'without_hats': 0,
#                             'car color': 0
#                             }
#         if x_val == 'bottoms':
#             y_lists[x_val] = {'long_sleeve': 0,
#                               'short_sleeve': 0,
#                               'shorts': people_item_count['SHORTS'],
#                               'pants': people_item_count['PANTS'],
#                               'hats': 0,
#                               'without_hats': 0,
#                               'car color': 0
#                               }
#         if x_val == 'hat':
#             y_lists[x_val] = {'long_sleeve': 0,
#                               'short_sleeve': 0,
#                               'shorts': 0,
#                               'pants': 0,
#                               'hats': people_item_count['HAT'],
#                               'without_hats': people_item_count['NO_HAT'],
#                               'car color': 0
#                               }
#         if x_val == 'vehicle color':
#             y_lists[x_val] = {'long_sleeve': 0,
#                               'short_sleeve': 0,
#                               'shorts': 0,
#                               'pants': 0,
#                               'hats': 0,
#                               'without_hats': 0,
#                               'car color': list(car_color_count.values())
#                               }
#     return y_lists
#
# def bar_graph(person_df, vehicle_df):
#     x = ['top', 'bottoms', 'hat', 'vehicle color'] #same as names
#     name_1 = ['long sleeve', 'short sleeve', 'shorts', 'pants', 'hats', 'no hats']
#     people_variables = ['LONG_SLEEVE', 'SHORT_SLEEVE', 'SHORTS', 'PANTS', 'HAT', 'FEMALE', 'MALE']
#     people_item_count = item_counter(person_df, people_variables)
#     paint_list = list(vehicle_df['PAINT'])
#     vehicle_variables = list(set(paint_list))
#     car_color_count = count_car_color(vehicle_df)
#     names = name_1 + vehicle_variables
#     print(names)
#     y_lists = get_y_lists(people_item_count, car_color_count, x)
#     print(y_lists)
#     y_values = []
#     for xval in x:
#         y = list(y_lists[xval].values())
#         if xval != 'vehicle color':
#             zeroes = len(vehicle_variables) * [0]
#             y.append(zeroes)
#         y_values.append(y)
#     print(y_values)
#     fig = go.Figure(go.Bar(x=x, y=y_values[0], name=names[0]))
#     fig.add_trace(go.Bar(x=x, y=[], name=names[n]))
#     fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
#     fig.show()
# print(bar_graph(df2, df1))

def percent_sex(people_df):
    count = 0
    bool_list = people_df['FEMALE']
    for bool in bool_list:
        if bool == "TRUE":
            count += 1
    percent_female = (count/len(bool_list)) * 100
    percent_male = 100 - percent_female
    return percent_female, percent_male

# @app.callback(
#     Output("gender-pie", "figure"),
#     Input("interval-component", "n_intervals"))
def update_sex_chart():
    df1 = pd.read_csv(
        "TrafficData_Rand.csv",
        dtype=object,
    )
    df2 = pd.read_csv(
        "Time_Location_Rand_People.csv",
        dtype=object,
    )
    percent_female, percent_male = percent_sex(df2)
    percentages = [percent_female, percent_male]
    sex = ["Female", "Male"]
    zipped = list(zip(sex, percentages))
    df = pd.DataFrame(zipped, columns=[
        "SEX",
        "%"]
                       )
    colors = ['#BBEC19', '#2BB5B8']
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['people'],
        x=[percent_female],
        name='Female',
        orientation='h',
        marker=dict(
            color=colors[0],
            line=dict(color=colors[0], width=2)
        )
    ))
    fig.add_trace(go.Bar(
        y=['people'],
        x=[percent_male],
        name='Male',
        orientation='h',
        marker=dict(
            color=colors[1],
            line=dict(color=colors[1], width=2)
        )
    ))

    fig.update_layout(barmode='stack', width=500, height=300)
    fig.show()
    return fig

print(update_sex_chart())