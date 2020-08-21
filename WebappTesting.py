import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import psycopg2
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import sys, os

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server
# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

# Dictionary of important locations in London
list_of_locations = {
    "Barking and Dagenham": {"lat": 51.5607, "lon": 0.1557},
    "Barnet": {"lat": 51.6252, "lon": -0.1517},
    "Bexley": {"lat": 51.4549, "lon": 0.1505},
    "Brent": {"lat": 51.5588, "lon": -0.2817},
    "Bromley": {"lat": 51.4039, "lon": 0.0198},
    "Camden": {"lat": 51.5290, "lon": -0.1255},
    "City of London": {"lat": 51.5155, "lon": -0.0922},
    "Croyden": {"lat": 51.3714, "lon": -0.0977},
    "Ealing": {"lat": 51.5130, "lon": -0.3089},
    "Enfield": {"lat": 51.6538, "lon": -0.0799},
    "Greenwich": {"lat": 51.4892, "lon": 0.0648},
    "Hackney": {"lat": 51.5450, "lon": -0.0553},
    "Hammmersmith and Fulham": {"lat": 51.4927, "lon": -0.2339},
    "Haringey": {"lat": 51.6000, "lon": -0.1119},
    "Harrow": {"lat": 51.5898, "lon": -0.3346},
    "Havering": {"lat": 51.5812, "lon": 0.1837},
    "Hillingdon": {"lat": 51.5441, "lon": -0.4760},
    "Hounslow": {"lat": 51.4746, "lon": -0.3580},
    "Islington": {"lat": 51.5416, "lon": -0.1022},
    "Kensington and Chelsea": {"lat": 51.5020, "lon": -0.1947},
    "Kingston upon Thames": {"lat": 51.4085, "lon": -0.3064},
    "Lambeth": {"lat": 51.4607, "lon": -0.1163},
    "Lewisham": {"lat": 51.4452, "lon": -0.0209},
    "Merton": {"lat": 51.4014, "lon": -0.1958},
    "Newham": {"lat": 51.5077, "lon": 0.0469},
    "Redbridge": {"lat": 51.5590, "lon": 0.0741},
    "Richmond upon Thames": {"lat": 51.4479, "lon": -0.3260},
    "Southwark": {"lat": 51.5035, "lon": -0.0804},
    "Sutton": {"lat": 51.3618, "lon": -0.1945},
    "Tower Hamlets": {"lat": 51.5099, "lon": -0.0059},
    "Waltham Forest": {"lat": 51.5908, "lon": -0.0134},
    "Wandsworth": {"lat": 51.4567, "lon": -0.1910},
    "Westminster": {"lat": 51.4973, "lon": -0.1372},
}

crime_mapping = {
    "Anti-social behaviour": 0,
    "Drugs": 1,
    "Other theft": 2,
    "Theft from the person": 3,
    "Violence and sexual offences": 4,
    "Bicycle theft": 5,
    "Possession of weapons": 6,
    "Public order": 7,
    "Vehicle crime": 8,
    "Burglary": 9,
    "Criminal damage and arson": 10,
    "Robbery": 11,
    "Shoplifting": 12,
    "Other crime": 13
}

# Create app layout
app.layout = html.Div(
    [
        # headers and titles of the map
        html.Div(
            className="four columns div-user-controls",
            children=[
                html.H2("LONDON CRIME DATA MAPPED"),
                html.Div(
                    className="div-for-slider",
                    children=[dcc.Slider(
                        id="years-slider",
                        min=2016,
                        max=2022,
                        value=2019,
                        marks={
                            str(i): {
                                "label": str(i),
                                "style": {"color": "#7fafdf"},
                            }
                            for i in range(2016, 2023)
                        },
                    )]),

                html.Div(
                    className="div-for-dropdown",
                    children=[
                        dcc.DatePickerSingle(
                            id="date-picker",
                            min_date_allowed=dt(2000, 1, 1),
                            max_date_allowed=dt(2020, 12, 30),
                            initial_visible_month=dt(2019, 11, 1),
                            date=dt(2019, 11, 1).date(),
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
                                # Dropdown for locations on map
                                dcc.Dropdown(
                                    id="location-dropdown",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in list_of_locations
                                    ],
                                    placeholder="Select a Borough",
                                )
                            ],
                        ),

                    ],
                ),
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                # Dropdown for locations on map
                                dcc.Dropdown(
                                    id="crime-dropdown",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in crime_mapping
                                    ],
                                    placeholder="Select a Crime Type",
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="div-for-dropdown",
                            children=[dcc.RangeSlider(
                                id="time-slider",
                                min=0,
                                max=24,
                                value=[4, 14],
                                marks={
                                    str(i): {
                                        "label": str(i),
                                        "style": {"color": "#7fafdf"},
                                    }
                                    for i in range(0, 25)
                                },
                            )],
                        ),
                    ],
                ),
            ],
        ),
        # second lot of columns 8 accross
        html.Div(
            className="eight columns div-for-charts bg-grey",
            children=[
                dcc.Graph(id="map-graph")], ),
    ],

)

# Update Map Graph based on date-picker,location dropdown, and type of crime
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("date-picker", "date"),
        Input("location-dropdown", "value"),
        Input("crime-dropdown", "value"),
    ],
)
def testingCallbacks(datePicked, selectedLocation, selectedCrime):
    print(hi)
