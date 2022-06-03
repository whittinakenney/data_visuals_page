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

##must manually add x-values (i.e. "FEMALE") in update_histogram_live


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Person Identification and Plate Identification"
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1Ijoid2hpdHRpbmFrZW5uZXkiLCJhIjoiY2wzbmRrbWR6MGRpZTNrbXU1OTN4NmJnYyJ9.GRJfLp1eHrnerFrpDqpzAw"

#important locations
important_locations = {
    "Emerging Technology Institute": {"lat": 34.83373, "lon": -79.18246}
}

#Maximum Date from data
def extract_all_times(df1, df2):
    vehicle_times = list(df1["TIME"])
    person_times = list(df2["TIME"])
    all_times_dates = vehicle_times + person_times #all the times which are in the yyyymmdd-hhmmss format
    return all_times_dates

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

def max_date():
    df1 = pd.read_csv(
        "TrafficData_Rand.csv",
        dtype=object,
    )
    df2 = pd.read_csv(
        "Time_Location_Rand_People.csv",
        dtype=object,
    )
    all_years, all_months, all_hours = extract_times(df1, df2)
    max_year = max(all_years)
    max_month = max(all_months) + 12
    if max_month == 13:
        max_month = 1
        max_year = max_year + 1
    return "{}-{}-{}".format(max_year, max_month, 1)

#Next we make lists of hours IDs were collected
def all_IDs(df1, df2):
    Person_ID_list = list(df2["ID"])
    Plate_Num_List = list(df1["ID"])
    Vehicle_Person_IDs = Plate_Num_List + Person_ID_list
    return Vehicle_Person_IDs

## remember all_times_dates = vehicle_times + person_times

#We are going to match all the IDs (person and plate) with the times
#they were collected
#IDs_and_time_collected = tuple(zip(Vehicle_Person_IDs, all_hours))

#Collecting labels
def all_labels(df1, df2):
    Vehicle_Labels = list(df1["LABEL"])
    People_Labels = list(df2["LABEL"])
    Vehicle_People_Labels = Vehicle_Labels + People_Labels
    return Vehicle_People_Labels

# Collecting Unique locations of cameras for both people and vehicles
def lats_long(df1, df2):
    Vehicle_Lats = list(df1["LAT"])
    Vehicle_Longs = list(df1["LONG"])
    Vehicle_Lat_Long = tuple(zip(Vehicle_Lats, Vehicle_Longs))
    People_Lats = list(df2["LAT"])
    People_Longs = list(df2["LONG"])
    People_Lat_Long = tuple(zip(People_Lats, People_Longs))
    Vehicle_People_Coords = Vehicle_Lat_Long + People_Lat_Long
    Vehicle_People_Lats = Vehicle_Lats + People_Lats
    Vehicle_People_Longs = Vehicle_Longs + People_Longs
    Unique_Vehicle_Locations = list(set(Vehicle_Lat_Long))
    Unique_People_Locations = list(set(People_Lat_Long))
    return(Vehicle_Lat_Long, People_Lat_Long, Vehicle_People_Lats,
           Vehicle_People_Longs, Unique_Vehicle_Locations, Unique_People_Locations)

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

#add color code column to df4
def assign_color_label(row):
    if row['LABELS'] == 'vehicle':
        color = "#FFFFFF"
        return color
    if row['LABELS'] == 'person':
        color = "#8607A9"
        return color

##Creating datafram with person and vehicles which will include ID, TIME in standard format, LAT, LONG, LABEL, COLOR
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
        "ID",
        "TIME",
        "LAT",
        "LONG",
        "LABELS"]
    )
    df4['COLOR'] = df4.apply(lambda row: assign_color_label(row), axis=1)
    return df4

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(id='live-update-csv'),
        dcc.Interval(
        id='interval-component',
        interval=2.5*1000, # in milliseconds
        n_intervals=0),
        html.Div(
                className="four columns div-user-controls",
                children=[
                    html.A(
                            html.Img(
                                className="logo",
                                src=app.get_asset_url("dash-logo-new.png"),
                            ),
                            href="https://plotly.com/dash/",
                        ),
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
        html.Div(
            #className="row",
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

def count_per_hour(year, month, day):
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
    hour_of_detection = []
    detections_by_hour = []
    df4 = data_frame4(df1, df2)
    for n in range(len(list(df4["TIME"]))):
        if (df4['TIME'][n].year == year and
            df4['TIME'][n].month == month and
            df4['TIME'][n].day == day
        ):
            for m in range(24):
                if df4['TIME'][n].hour == m:
                    hour_of_detection.append(m)
    for p in range(24):
        detections_by_hour.append(hour_of_detection.count(p))
    return detections_by_hour

def get_selection(year, month, day, selection):
    xVal = []
    yVal = []
    xSelected = []
    colorVal = [
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

    # Put selected times into a list of numbers xSelected
    xSelected.extend([int(x) for x in selection])

    for i in range(24):
        # If bar is selected then color it white
        if i in xSelected and len(xSelected) < 24:
            colorVal[i] = "#FFFFFF"
        xVal.append(i)
        # Get the number of people and plates at a particular time
        yVal = count_per_hour(year, month, day)
    return [np.array(xVal), np.array(yVal), np.array(colorVal)]

#Selected Data in the Histogram updates map
# @app.callback(
#     Output("bar-selector", "value"),
#     [Input("histogram", "selectedData"), Input("histogram", "clickData")]
# )
# def update_bar_selector(value, clickData):
#     holder = []
#     if clickData:
#         holder.append(str(int(clickData["points"][0]["x"])))
#     if value:
#         for x in value["points"]:
#             holder.append(str(int(x["x"])))
#     return list(set(holder))


# Clear Selected Data if Click Data is used
# @app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
# def update_selected_data(clickData):
#     if clickData:
#         return {"points": []}


@app.callback(Output("rul-estimation-indicator-led", "value"), Input("interval-component", "n_intervals"))
def update_total_detections(n):
    df1 = pd.read_csv(
        "TrafficData_Rand.csv",
        dtype=object,
    )
    df2 = pd.read_csv(
        "Time_Location_Rand_People.csv",
        dtype=object,
    )
    #date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    #qualified_dates = []
    all_times_dates = extract_all_times(df1, df2)
    #for time in all_times_dates:
        # if (date_picked.year == int(time[0:4])
        #         and date_picked.month == int(time[4:6])
        #         and date_picked.day == int(time[6:8])
        # ):
        #     qualified_dates.append(time)
    return len(all_times_dates)

def item_counter(dataFrame, domain):
    item_counter = []
    for item in domain:
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
    # for n in range(len(domain)):
    #     if clickData != None:
    #         selectedFeature = clickData["points"][0]["x"]
    #     else:
    #         selectedFeature = None
    #     if domain[n] == selectedFeature:
    #         colorVal.append("#FFFFFF")
    #     else:
    #         colorVal.append(colors[n])
    return colorVal

# @app.callback(
#     Output("histogram", "figure"),
#     [Input("interval-component", "n_intervals")]
# )
# def update_histogram_live(n):
#     # date_picked = dt.strptime(datePicked, "%Y-%m-%d")
#     # monthPicked = date_picked.month #- 4
#     # dayPicked = date_picked.day #- 1
#     # yearPicked = date_picked.year
#     #[xVal, yVal, colorVal] = get_selection(yearPicked, monthPicked, dayPicked, value)
#
#     df2 = pd.read_csv(
#         "Time_Location_Rand_People.csv",
#         dtype=object,
#     )
#
#     xVal = ['LONG_SLEEVE', 'SHORT_SLEEVE', 'SHORTS', 'PANTS', 'HAT', 'FEMALE', 'MALE']
#     yVal = np.array(item_counter(df2, xVal))
#     colorVal = np.array(get_bar_color(xVal))
#
#
#     layout = go.Layout(
#         bargap=0.05,
#         bargroupgap=0,
#         barmode="group",
#         margin=go.layout.Margin(l=10, r=0, t=0, b=50),
#         showlegend=False,
#         plot_bgcolor="#323130",
#         paper_bgcolor="#323130",
#         dragmode="select",
#         font=dict(color="white"),
#         xaxis=dict(
#             range=[-1, len(xVal)],
#             showgrid=False,
#             nticks=25,
#             fixedrange=True,
#             ticksuffix="",
#         ),
#         yaxis=dict(
#             range=[0, max(yVal)+10],
#             showticklabels=False,
#             showgrid=False,
#             fixedrange=True,
#             rangemode="nonnegative",
#             zeroline=False,
#         ),
#         annotations=[
#             dict(
#                 x=xi,
#                 y=yi,
#                 text=str(yi),
#                 xanchor="center",
#                 yanchor="bottom",
#                 showarrow=False,
#                 font=dict(color="white"),
#             )
#             for xi, yi in zip(xVal, yVal)
#         ],
#     )
#
#     return go.Figure(
#         data=[
#             go.Bar(x=xVal, y=yVal, marker=dict(color=colorVal), hoverinfo="x"),
#             go.Scatter(
#                 opacity=0,
#                 x=xVal,
#                 y=yVal / 2,
#                 hoverinfo="none",
#                 mode="markers",
#                 marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
#                 visible=True,
#             ),
#         ],
#         layout=layout,
#     )


#Given date and time, this function will return a database with the ID, TIME, LAT, LONG, and LABEL
#that correspond to that specific date and time. Time is the index.

def getLatLonColor(selectedData, month, day):
    df1 = pd.read_csv(
        "TrafficData_Rand.csv",
        dtype=object,
    )
    df2 = pd.read_csv(
        "Time_Location_Rand_People.csv",
        dtype=object,
    )
    all_times_dates = extract_all_times(df1, df2)
    df4 = data_frame4(df1, df2)
    include_rows = []
    include_rows_2 = []
    for n in range(len(all_times_dates)):
        if df4['TIME'][n].month == month and df4['TIME'][n].day == day:
            include_rows.append(n)
    listCoords = df4.iloc[include_rows]
    list_qualified_dates = list(listCoords['TIME'])
#No times selected, output all times for chosen month and date
    if selectedData == None or len(selectedData) == 0:
        listCoords = listCoords.set_index('TIME')
        return listCoords
    for time in selectedData:
        for m in range(len(list_qualified_dates)):
            hour_at_row_m = "{}".format(list_qualified_dates[m].hour)
            if hour_at_row_m == time:
                include_rows_2.append(m)
    listCoords_byHours = listCoords.iloc[include_rows_2]
    listCoords_byHours = listCoords_byHours.set_index('TIME')
    if len(selectedData) != 0:
        return listCoords_byHours

#function that creates df5
def create_map_df(df_with_coords):
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
            colors.append('#2BB5B8')
        else:
            colors.append('#7FFF00')
    zipped = list(zip(number_of_detections, unique_lats, unique_longs,
            list_ID_list, list_labels_lists, colors))
    df5 = pd.DataFrame(zipped, columns=[
        "DETECTIONS",
        "LAT",
        "LONG",
        "ID",
        "LABELS",
        "COLOR"]
        )
    return df5

def get_text(map_df1, map_df2):
    labels = list(map_df1.LABELS) + list(map_df2.LABELS)
    Unique_IDs = list(map_df1.ID) + list(map_df2.ID)
    total_detections = list(map_df1.DETECTIONS) + list(map_df2.DETECTIONS)
    text = []
    for n in range(len(labels)): #obj is a list in a list of label lists
        if len(labels[n]) == 1:
            text.append((labels[n], Unique_IDs[n]))
        if len(labels[n]) != 1:
            text.append((total_detections[n], Unique_IDs[n]))
    return text

def map_filter(clickData):
    person_feature = clickData["points"][0]["x"]
    return person_feature

def map_xval_yval():
    df1 = pd.read_csv(
        "TrafficData_Rand.csv",
        dtype=object,
    )
    df2 = pd.read_csv(
        "Time_Location_Rand_People.csv",
        dtype=object,
    )
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

# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("interval-component", "n_intervals")
    ],
)
def update_graph(n):#date, time in string format, location

    df1_new, df2_new, veh_per_lats, veh_per_longs, veh_per_colors = map_xval_yval()

    zoom = 12.0
    latInitial = 34.83363
    lonInitial = -79.18255
    bearing = 0

    return go.Figure(
        data=[
            Scattermapbox(
                lat=veh_per_lats,
                lon=veh_per_longs,
                mode="markers",
                hoverinfo="lat+lon+text",
                text=get_text(df1_new, df2_new),
                marker=dict(size=5, color=veh_per_colors, allowoverlap=True)
                ),
            Scattermapbox( #double check things are picked up at ETI
                lat=[important_locations[i]["lat"] for i in important_locations],
                lon=[important_locations[i]["lon"] for i in important_locations],
                mode="markers",
                hoverinfo="text",
                text=[i for i in important_locations],
                marker=dict(size=8, color="#A91007", allowoverlap=True),
            ),
        ],
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
                                        #"mapbox.zoom": 12,
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

def percent_sex(people_df):
    count = 0
    bool_list = people_df['FEMALE']
    for bool in bool_list:
        if bool == "TRUE":
            count += 1
    percent_female = (count/len(bool_list)) * 100
    percent_male = 100 - percent_female
    return percent_female, percent_male

@app.callback(
    Output("gender-bar", "figure"),
    Input("interval-component", "n_intervals"))
def update_sex_chart(n):
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
            line=dict(color='#FFFFFF', width=1)
        )
    ))
    fig.add_trace(go.Bar(
        y=['people'],
        x=[percent_male],
        name='Male',
        orientation='h',
        marker=dict(
            color=colors[1],
            line=dict(color='#FFFFFF', width=1)
        )
    ))

    fig.update_layout(barmode='stack', width=400, height=150, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      font_color='#FFFFFF', margin=dict(l=0, r=20, t=20, b=20))
    return fig

def percent_car_color(vehicle_df):
    paint_list = list(vehicle_df['PAINT'])
    colors = list(set(paint_list))
    percents = []
    for color in colors:
        count = 0
        for n in range(len(paint_list)):
            if color == paint_list[n]:
                count += 1
        percent = (count/len(paint_list)) * 100
        percents.append(percent)
    return percents, colors

@app.callback(
    Output("car-bar", "figure"),
    Input("interval-component", "n_intervals"))
def update_car_bar(n):
    df1 = pd.read_csv(
        "TrafficData_Rand.csv",
        dtype=object,
    )
    percents, colors = percent_car_color(df1)
    graph_colors = px.colors.sequential.Viridis
    fig = go.Figure()
    for n in range(len(percents)):
        fig.add_trace(go.Bar(
            y=['vehicles'],
            x=[percents[n]],
            name=colors[n],
            orientation='h',
            marker=dict(
                color=graph_colors[n],
                line=dict(color='#FFFFFF', width=1)
            )
        ))

    fig.update_layout(barmode='stack', width=400, height=150, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      font_color='#FFFFFF', margin=dict(l=0, r=20, t=20, b=20))
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)