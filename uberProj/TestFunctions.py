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

Vehicle_Labels = list(df1["LABEL"])
People_Labels = list(df2["LABEL"])
Vehicle_People_Labels = Vehicle_Labels + People_Labels

Person_ID_list = list(df2["PersonID"])
Plate_Num_List = list(df1["PlateNumber"])
Vehicle_Person_IDs = Plate_Num_List + Person_ID_list
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
VehicleLocationID = 0
PersonLocationID = 0

# Collecting Unique locations of cameras for both people and vehicles
Vehicle_Lats = list(df1["LAT"])
Vehicle_Longs = list(df1["LONG"])
Vehicle_Lat_Long = tuple(zip(Vehicle_Lats, Vehicle_Longs))
People_Lats = list(df2["LAT"])
People_Longs = list(df2["LONG"])
People_Lat_Long = tuple(zip(People_Lats, People_Longs))

dict_of_vehicle_people_locations = {}
ALL_LocationID = 0

Unique_Vehicle_People_Locations = list(set(Unique_Vehicle_Locations + Unique_People_Locations))

for p in range(len(Unique_Vehicle_People_Locations)):
    ALL_LocationID = p #unique locations from both person and vehicle cams
    latitude = float(Unique_Vehicle_People_Locations[p][0])
    longitude = float(Unique_Vehicle_People_Locations[p][1])
    dict_of_vehicle_people_locations[ALL_LocationID] = {"lat": latitude, "lon": longitude}

list_of_locations = dict_of_vehicle_people_locations

print(list_of_locations)

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
    return (max_year, max_month, 1)


Person_ID_list = list(df2["PersonID"])
Plate_Num_List = list(df1["PlateNumber"])
Vehicle_Person_IDs = Plate_Num_List + Person_ID_list
print(Vehicle_Person_IDs)
## remember all_times_dates = vehicle_times + person_times

#We are going to match all the IDs (person and plate) with the times
#they were collected
IDs_and_time_collected = tuple(zip(Vehicle_Person_IDs, all_hours))

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
print(df4)

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

##function that takes a list of hours and tells returns how many instances
#of each hour.
#the idea is to filter IDs by a date first, then search for each of those ID's
#corresponding times so we can get a count of people on a certain date at a certain time

def by_time(list_of_hours):
    traffic_by_time = {}
    for m in range(len(list_of_hours)):
        for n in range(0,24):
            traffic_by_time[n] = list_of_hours.count(n)
    return(traffic_by_time)

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
        yVal = by_time(people_by_date(year, month, day)).values()
    return [np.array(xVal), np.array(yVal), np.array(colorVal)]

def update_total_detections(datePicked):
    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    qualified_dates = []
    for time in all_times_dates:
        if (date_picked.year == int(time[0:4])
                and date_picked.month == int(time[4:6])
                and date_picked.day == int(time[6:8])
        ):
            qualified_dates.append(time)
    return "Total Number of detections: {:,d}".format(
        len(qualified_dates)
    )

#Given date and time, this function will return a database with the ID, TIME, LAT, LONG, and LABEL
#that corespond to that specific date and time

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


listCoords: pd.DataFrame = getLatLonColor(['21', '24', '17', '13'], 5, 23)
#listCoords = listCoords.set_index('TIME')

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

#listCoords = listCoords.set_index('TIME')\

print(getLatLonColor(['21', '24', '17', '13'], 5, 23))

def choose_color(df_with_lat_long):
    lats = list(df_with_lat_long["LAT"])
    longs = list(df_with_lat_long["LONG"])

print(Vehicle_People_Labels)
for m in range(len(Vehicle_People_Labels)):
    colors = []
    if Vehicle_People_Labels[m] == "vehicle":
        colors.append("#FFFFFF")
    if Vehicle_People_Labels[m] == "person":
        colors.append("#8607A9")
print(colors)