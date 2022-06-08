
from plotly import graph_objs as go
from plotly.graph_objs import *
import plotly.express as px


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1Ijoid2hpdHRpbmFrZW5uZXkiLCJhIjoiY2wzbmRrbWR6MGRpZTNrbXU1OTN4NmJnYyJ9.GRJfLp1eHrnerFrpDqpzAw"

#important locations
important_locations = {
    "Emerging Technology Institute": {"lat": 34.83373, "lon": -79.18246},
    "14442C1031A059D700": {"lat": 34.83358, "lon": -79.18238}
}

def initial_map():
    zoom = 14.0
    latInitial = 34.83363
    lonInitial = -79.18255
    bearing = 0
    map = go.Figure(
        data=[
            Scattermapbox(
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
    map.show()
    return map
initial_map()
