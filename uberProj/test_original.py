import numpy as np
import pandas as pd
# Initialize data frame
df1 = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv",
    dtype=object,
)
df2 = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data2.csv",
    dtype=object,
)
df3 = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data3.csv",
    dtype=object,
)
df = pd.concat([df1, df2, df3], axis=0)
df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d %H:%M")
df.index = df["Date/Time"]
df.drop("Date/Time", 1, inplace=True)
totalList = []
for month in df.groupby(df.index.month):
    dailyList = []
    for day in month[1].groupby(month[1].index.day):
        dailyList.append(day[1])
    totalList.append(dailyList)
totalList = np.array(totalList)

# def getLatLonColor(selectedData, month, day):
#     listCoords = totalList[month][day]
#
#     # No times selected, output all times for chosen month and date
#     if selectedData is None or len(selectedData) is 0:
#         return listCoords
#     listStr = "listCoords["
#     for time in selectedData:
#         if selectedData.index(time) is not len(selectedData) - 1:
#             listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ") | "
#         else:
#             listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ")]"
#     return eval(listStr)

def getLatLonColor(selectedData, month, day):
    listCoords = totalList[month][day]

    # No times selected, output all times for chosen month and date
    if selectedData is None or len(selectedData) is 0:
        return listCoords
    listStr = "listCoords["
    for time in selectedData:
        if selectedData.index(time) is not len(selectedData) - 1:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ") | "
        else:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ")]"
    return eval(listStr)
print(getLatLonColor(['5', '6'], 4, 14))