import dash
import plotly.graph_objs
from dash import dcc
from dash import html
import pandas as pd
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("FakePeopleData.csv")
#data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
#data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@100;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Fake People Stats"

##Layered Bar Graph##
x = list(data["PersonID"])
sig_vector = [.25, .25, .25, .25] #must be same size as number of characteristics and add to 1

characteristics = list(data.columns[1:])
unit_column_vectors = []

for m in range(len(characteristics)): #scales each column vectors by sig_vector
    column_m_times_sig_m = data[characteristics[m]] * sig_vector[m]
    unit_column_vectors.append(column_m_times_sig_m)

for n in range(len(characteristics)): #takes every person except the first and finds its characteristic composition
    if n == 0:
        fig = go.Figure(go.Bar(x=x, y=unit_column_vectors[n], name=characteristics[n]))
    else:
        fig.add_trace(go.Bar(x=x, y=unit_column_vectors[n], name=characteristics[n]))

fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'},
                  title="Total Confidence for Each Person's ID", paper_bgcolor = "#011311",
                  font_color="#BDEEE8", plot_bgcolor="#004C47", font_family="Georgia",
                  )
fig.update_yaxes(gridcolor="#01726A")

##App Layout##
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children=u"\U0001F47B", className="header-emoji"),
                html.H1(
                    children="Fake People Data", className="header-title"
                ),
                html.P(
                    children="20 fake people and their identifying characteristics",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # html.Div(
        #     children=[
        #         html.Div(children="Characteristic filters:", className="menu-title"),
        #         dcc.Dropdown(
        #             id="char-filter",
        #             options=[
        #                 {"label": characteristic, "value": characteristic}
        #                 for characteristic in data.columns[1:]
        #             ],
        #             value="reidentification",
        #             clearable=False,
        #             multi=True,
        #             className="dropdown",
        #         ),
        #     ],
        #     className="menu",
        # ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='Total_Confidence',
                        figure=fig,
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
