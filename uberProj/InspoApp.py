import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import uuid

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Person Identification and Plate Identification"
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1Ijoid2hpdHRpbmFrZW5uZXkiLCJhIjoiY2wzbmRrbWR6MGRpZTNrbXU1OTN4NmJnYyJ9.GRJfLp1eHrnerFrpDqpzAw"

#Read CSV files
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

#Maximum Date from data
vehicle_times = list(df1["TIME"])
person_times = list(df2["TIME"])
all_times_dates = vehicle_times + person_times #all the times which are in the yyyymmdd-hhmmss format
all_dates = [] #dates formatted as (yyyy, m, dd)
all_years = [] #just collects all the years
all_months = []
all_hours = []
all_times = []
for time in all_times_dates:
    year = int(time[0:4])
    month = int(time[4:6])
    day = int(time[6:8])
    hour = int(time[9:11])
    total_time = int(time[9:15])
    date = (year, month, day)
    all_dates.append(date)
    all_years.append(year)
    all_months.append(month)
    all_hours.append(hour)
    all_times.append(total_time)
    date_time_array = [np.array(all_dates), np.array(all_times)]  # array of dates and times
def max_date():
    max_year = max(all_years)
    max_month = max(all_months) + 1
    if max_month == 13:
        max_month = 1
        max_year = max_year + 1
    return "{}-{}-{}".format(max_year, max_month, 1)

#Next we make lists of hours IDs were collected
Person_ID_list = list(df2["PersonID"])
Plate_Num_List = list(df1["PlateNumber"])
Vehicle_Person_IDs = Plate_Num_List + Person_ID_list
## remember all_times_dates = vehicle_times + person_times

#We are going to match all the IDs (person and plate) with the times
#they were collected
IDs_and_time_collected = tuple(zip(Vehicle_Person_IDs, all_hours))

#Collecting labels
Vehicle_Labels = list(df1["LABEL"])
People_Labels = list(df2["LABEL"])
Vehicle_People_Labels = Vehicle_Labels + People_Labels

#important locations
important_locations = {
    "Emerging Technology Institute": {"lat": 34.83373, "lon": -79.18246},
}

# Collecting Unique locations of cameras for both people and vehicles
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

dict_of_people_locations = {}
dict_of_vehicle_locations = {}
dict_of_vehicle_people_locations = {}
dict_of_All_detection_locations = {}
VehicleLocationID = 0
PersonLocationID = 0
ALL_LocationID = 0

Unique_Vehicle_People_Locations = list(set(Unique_Vehicle_Locations + Unique_People_Locations))

for p in range(len(Unique_Vehicle_People_Locations)):
    ALL_LocationID = p #unique locations from both person and vehicle cams
    latitude = float(Unique_Vehicle_People_Locations[p][0])
    longitude = float(Unique_Vehicle_People_Locations[p][1])
    dict_of_vehicle_people_locations[ALL_LocationID] = {"lat": latitude, "lon": longitude}

for q in range(len(Vehicle_Lat_Long)):
    LocationID = uuid.uuid4() #Gives ID to every detection
    latitude = float(Vehicle_Lat_Long[q][0])
    longitude = float(Vehicle_Lat_Long[q][1])
    label = 'vehicle'
    color = "#FFFFFF" #vehicles will be white
    dict_of_All_detection_locations[LocationID] = {"lat": latitude, "lon": longitude,
                                                   "label": label, "color": color}
    for r in range(len(People_Lat_Long)):
        LocationID = uuid.uuid4()
        latitude2 = float(People_Lat_Long[r][0])
        longitude2 = float(People_Lat_Long[r][1])
        label2 = 'person'
        color2 = "#8607A9" #people will be purple
        dict_of_All_detection_locations[LocationID] = {"lat": latitude2, "lon": longitude2,
                                                       "label": label2, "color": color2}

list_of__unique_locations = dict_of_vehicle_people_locations
list_of_locations = dict_of_All_detection_locations

##Creating datafram with person and vehicles which will include ID, TIME in standard format, LAT, LONG, LABEL
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

zipped = list(zip(Vehicle_Person_IDs, standard_date_time_list,
                  Vehicle_People_Lats, Vehicle_People_Longs,
                  Vehicle_People_Labels
                  ))
df4 = pd.DataFrame(zipped, columns=[
    "IDnumber",
    "TIME",
    "LAT",
    "LONG",
    "LABELS"]
)

# df = pd.concat([df1, df2, df3], axis=0)
# df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d %H:%M")
# df.index = df["Date/Time"]
# df.drop("Date/Time", 1, inplace=True)
# totalList = []
# for month in df.groupby(df.index.month):
#     dailyList = []
#     for day in month[1].groupby(month[1].index.day):
#         dailyList.append(day[1])
#     totalList.append(dailyList)
# totalList = np.array(totalList)

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
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
                        html.H2("Person and Plate Information"),
                        html.P(
                            """Select filters for data"""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2022, 5, 1),
                                    max_date_allowed=max_date(),
                                    initial_visible_month=dt(2022, 5, 1),
                                    date=dt(2022, 5, 1).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for cameras collecting person data
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in important_locations
                                            ],
                                            placeholder="Location",
                                        )
                                    ],
                                ),
                                # html.Div(
                                #     className="div-for-dropdown",
                                #     children=[
                                #         # Dropdown for cameras collecting vehicle data
                                #         dcc.Dropdown(
                                #             id="location-dropdown",
                                #             options=[
                                #                 {"label": p, "value": p}
                                #                 for p in dict_of_vehicle_locations
                                #             ],
                                #             placeholder="Location of vehicle camera",
                                #         )
                                #     ],
                                # ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector",
                                            options=[
                                                {
                                                    "label": str(n) + ":00",
                                                    "value": str(n),
                                                }
                                                for n in range(24)
                                            ],
                                            multi=True,
                                            placeholder="Select certain hours",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-detections"),
                        #html.P(id="total-selection-detections"),
                        html.P(id="date-value"),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                                "" #can add text between map and histogram
                            ],
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

# Gets the amount of days in the specified month
# Index represents month (0 is Jan, 1 is Feb, ... etc.)
daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Get index for the specified month in the dataframe
monthIndex = pd.Index(["Jan", "Feb", "Mar", "Apr", "May",
                       "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"])

## Get the amount of images captured based on the time selected ##

#This function takes a chosen date and returns a list of the hour
#each detection was detected
#for example: if three people were detected at 9AM on 5/23/2022,
#it would return [9, 9, 9]
def people_by_date(year, month, day):
    time_from_date = []
    for date in all_times_dates:
        if int(date[0:4]) == year and int(date[4:6]) == month and int(date[6:8]) == day:
            time_from_date.append(int(date[9:11]))
    return time_from_date

#function that takes a list of hours and tells returns how many instances
#of each hour.
#the idea is to filter IDs by a date first, then search for each of those ID's
#corresponding times so we can get a count of people on a certain date at a certain time
def by_time(list_of_hours):
    traffic_by_time = {}
    for m in range(len(list_of_hours)):
        for n in range(0,24):
            traffic_by_time[n] = list_of_hours.count(n)
    return(traffic_by_time)

#this functions takes the chosen year, month, and date
#Then, it finds all instances in database that match
#Then, it lists all the hours those instance occured
#Ex: two people were detected at 9 on jan 23, 2022, it would list [9, 9]
#Finally, it counts the occurence of each hour so [9, 9] would return [2]
def count_per_hour(year, month, day):
    hour_of_detection = []
    detections_by_hour = []
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


# Selected Data in the Histogram updates the Values in the Hours selection dropdown menu
@app.callback(
    Output("bar-selector", "value"),
    [Input("histogram", "selectedData"), Input("histogram", "clickData")],
)
def update_bar_selector(value, clickData):
    holder = []
    if clickData:
        holder.append(str(int(clickData["points"][0]["x"])))
    if value:
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))


# Clear Selected Data if Click Data is used
@app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(clickData):
    if clickData:
        return {"points": []}


# Update the total persons tag
@app.callback(Output("total-detections", "children"), [Input("date-picker", "date")])
def update_total_detections(datePicked):
    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    qualified_dates = []
    for time in all_times_dates:
        if (date_picked.year == int(time[0:4])
                and date_picked.month == int(time[4:6])
                and date_picked.day == int(time[6:8])
        ):
            qualified_dates.append(time)
    return "Total Number of detections on day selected: {:,d}".format(
        len(qualified_dates)
    )


# Update the total number of detections in selected times
# @app.callback(
#     [Output("total-selection-detections", "children"), Output("date-value", "children")],
#     [Input("date-picker", "date"), Input("bar-selector", "value")],
# )
# def update_total_detection_selection(datePicked, selection):
#     firstOutput = ""
#
#     if selection is not None or len(selection) is not 0:
#         date_picked = dt.strptime(datePicked, "%Y-%m-%d")
#         totalInSelection = 0
#         for x in selection:
#             totalInSelection += len(
#                 totalList[date_picked.month - 4][date_picked.day - 1][
#                     totalList[date_picked.month - 4][date_picked.day - 1].index.hour
#                     == int(x)
#                 ]
#             )
#         firstOutput = "Total detections in selection: {:,d}".format(totalInSelection)
#
#     if (
#         datePicked is None
#         or selection is None
#         or len(selection) is 24
#         or len(selection) is 0
#     ):
#         return firstOutput, (datePicked, " - showing hour(s): All")
#
#     holder = sorted([int(x) for x in selection])
#
#     if holder == list(range(min(holder), max(holder) + 1)):
#         return (
#             firstOutput,
#             (
#                 datePicked,
#                 " - showing hour(s): ",
#                 holder[0],
#                 "-",
#                 holder[len(holder) - 1],
#             ),
#         )
#
#     holder_to_string = ", ".join(str(x) for x in holder)
#     return firstOutput, (datePicked, " - showing hour(s): ", holder_to_string)


# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    [Input("date-picker", "date"), Input("bar-selector", "value")],
)
def update_histogram(datePicked, value):
    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month #- 4
    dayPicked = date_picked.day #- 1
    yearPicked = date_picked.year

    [xVal, yVal, colorVal] = get_selection(yearPicked, monthPicked, dayPicked, value)

    layout = go.Layout(
        bargap=0.01,
        bargroupgap=0,
        barmode="group",
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        dragmode="select",
        font=dict(color="white"),
        xaxis=dict(
            range=[-0.5, 23.5],
            showgrid=False,
            nticks=25,
            fixedrange=True,
            ticksuffix=":00",
        ),
        yaxis=dict(
            range=[0, max(yVal) + max(yVal) / 4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode="nonnegative",
            zeroline=False,
        ),
        annotations=[
            dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font=dict(color="white"),
            )
            for xi, yi in zip(xVal, yVal)
        ],
    )

    return go.Figure(
        data=[
            go.Bar(x=xVal, y=yVal, marker=dict(color=colorVal), hoverinfo="x"),
            go.Scatter(
                opacity=0,
                x=xVal,
                y=yVal / 2,
                hoverinfo="none",
                mode="markers",
                marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
                visible=True,
            ),
        ],
        layout=layout,
    )


#Given date and time, this function will return a database with the ID, TIME, LAT, LONG, and LABEL
#that correspond to that specific date and time. Time is the index.

def getLatLonColor(selectedData, month, day):
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

# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("date-picker", "date"),
        Input("bar-selector", "value"),
        Input("location-dropdown", "value"),
    ],
)
def update_graph(datePicked, selectedData, selectedLocation):#date, time in string format, location
    zoom = 12.0
    latInitial = 34.83363
    lonInitial = -79.18255
    bearing = 0

    if selectedLocation:
        zoom = 15.0
        latInitial = important_locations[selectedLocation]["lat"]
        lonInitial = important_locations[selectedLocation]["lon"]

    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month #- 4
    dayPicked = date_picked.day #- 1
    listCoords = getLatLonColor(selectedData, monthPicked, dayPicked)

    return go.Figure(
        data=[
            # Data for all rides based on date and time
            # Scattermapbox(
            #     lat=[list_of_locations[m]["lat"] for m in list_of_locations],
            #     lon=[list_of_locations[m]["lon"] for m in list_of_locations],
            #     mode="markers",
            #     hoverinfo="lat+lon+text",
            #     text=[list_of_locations[m]["label"] for m in list_of_locations],
            #     marker=dict(size=8,
            #                 color=[list_of_locations[m]["color"] for m in list_of_locations]),
            # ),
            # # Plot of important locations on the map
            Scattermapbox(
                lat=listCoords["Lat"],
                lon=listCoords["Lon"],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=listCoords.index.hour,
                marker=dict(
                    showscale=True,
                    color=##function to determine color,
                    size=5,
                    colorscale=[
                        [0, "#F4EC15"],
                        [0.04167, "#DAF017"],
                        [0.0833, "#BBEC19"],
                        [0.125, "#9DE81B"],
                        [0.1667, "#80E41D"],
                        [0.2083, "#66E01F"],
                        [0.25, "#4CDC20"],
                        [0.292, "#34D822"],
                        [0.333, "#24D249"],
                        [0.375, "#25D042"],
                        [0.4167, "#26CC58"],
                        [0.4583, "#28C86D"],
                        [0.50, "#29C481"],
                        [0.54167, "#2AC093"],
                        [0.5833, "#2BBCA4"],
                        [1.0, "#613099"],
                    ],
                    colorbar=dict(
                        title="Time of<br>Day",
                        x=0.93,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(color="#d8d8d8"),
                        titlefont=dict(color="#d8d8d8"),
                        thicknessmode="pixels",
                    ),
                ),
            ),
            Scattermapbox(
                lat=[important_locations[i]["lat"] for i in important_locations],
                lon=[important_locations[i]["lon"] for i in important_locations],
                mode="markers",
                hoverinfo="text",
                text=[i for i in important_locations],
                marker=dict(size=8, color="#A91007"),
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
                                        "mapbox.zoom": 12,
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


if __name__ == "__main__":
    app.run_server(debug=True)