import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

important_locations = {
    "Emerging Technology Institute": {"lat": 34.83373, "lon": -79.18246},
    "14442C1031A059D700": {"lat": 34.83358, "lon": -79.18238}
}
df1 = pd.read_csv(
    "TrafficData_Rand.csv",
    dtype=object,
)
veh_lats = df1.lat
veh_longs = df1.long
#veh_per_lats = [float(i) for i in veh_per_lats]
#veh_per_longs = [float(i) for i in veh_per_longs]


important_lat = [important_locations[i]["lat"] for i in important_locations]
important_lon = [important_locations[i]["lon"] for i in important_locations]
eti_lats = [34.83459512953768, 34.83480684650813, 34.83286712508545, 34.83309441422892]
eti_longs = [-79.18291931862396, -79.1822972311781, -79.18214550253276, -79.18136789322543]
veh_lats = [float(i) for i in veh_lats]
veh_longs = [float(i) for i in veh_longs]


print(important_lat)
print(important_lon)
BBox = (-79.17789, -79.18631, 34.83597, 34.83219) #OpenStreetMap longmin, longmax, latmin, latmax

map = plt.imread('openstreet.png')

fig, ax = plt.subplots(figsize=(10, 8.5))

ax.scatter(
    x=important_lon,
    y=important_lat,
    zorder=1,
    alpha=0.5,
    c="#A91007",
    s=10
    )
ax.scatter(
    x=eti_longs,
    y=eti_lats,
    zorder=1,
    alpha=0.5,
    c='#FFFFFF',
    s=10
    )
ax.scatter(
    x=veh_longs,
    y=veh_lats,
    zorder=1,
    alpha=0.5,
    cmap=mpl.cm.viridis,
    s=10
    )
ax.grid(True)
#ax.set_facecolor(color='#000000')
ax.set_alpha(0)
ax.set_title('Live Detections')
ax.set_xlim(BBox[0], BBox[1])
ax.set_ylim(BBox[2], BBox[3])
ax.imshow(map, zorder=0, extent=BBox, aspect='equal')
plt.show()