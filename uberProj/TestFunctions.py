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
    "../previousVersions/N-Factor_RandomGenerated .csv"
)


paint_list = ['orange', 'null']
colors = list(set(paint_list))
colors.remove('null')

columns = ['_id', 'id', 'color', 'lat', 'lon', 'label', 'postprocess']
vehicle_df = pd.DataFrame(columns=columns)
print(vehicle_df)
print(len(vehicle_df))