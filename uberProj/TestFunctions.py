import numpy as np
import pandas as pd
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

# Collecting Unique locations of cameras for both people and vehicles
Vehicle_Lats = list(df1["LAT"])
Vehicle_Longs = list(df1["LONG"])
Vehicle_Lat_Long = tuple(zip(Vehicle_Lats, Vehicle_Longs))
People_Lats = list(df2["LAT"])
People_Longs = list(df2["LONG"])
People_Lat_Long = tuple(zip(People_Lats, People_Longs))

Unique_Vehicle_Locations = list(set(Vehicle_Lat_Long))
Unique_People_Locations = list(set(People_Lat_Long))

dict_of_people_locations = {}
dict_of_vehicle_locations = {}
VehicleLocationID = 0
PersonLocationID = 0

for n in range(len(Unique_Vehicle_Locations)):
    VehicleLocationID = 2 * n + 1 #vehicle cam locations IDs only odd numbers
    latitude = Unique_Vehicle_Locations[n][0]
    longitude = Unique_Vehicle_Locations[n][1]
    dict_of_vehicle_locations[VehicleLocationID] = {"lat": latitude, "long": longitude}


for m in range(len(Unique_People_Locations)):
    PersonLocationID = m * 2 #person cam location IDs only even numbers
    latitude = Unique_People_Locations[m][0]
    longitude = Unique_Vehicle_Locations[m][1]
    dict_of_people_locations[PersonLocationID] = {"lat": latitude, "long": longitude}


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


PersonIDs = list(df2["PersonID"])
PlateNumbers = list(df1["PlateNumber"])
Plates_and_PersonIDs = PlateNumbers + PersonIDs
## remember all_times_dates = vehicle_times + person_times

#We are going to match all the IDs (person and plate) with the times
#they were collected
IDs_and_time_collected = tuple(zip(Plates_and_PersonIDs, all_hours))


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

##You can test functions here##
print(update_total_rides("2022-5-23"))