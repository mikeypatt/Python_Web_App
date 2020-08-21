import dash
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
import numpy as np
import pandas as pd

import layouts as dash_layout
import components_plus_methods as cm
from plotly.graph_objects import *

import time
from server import server
from Database import Connection
from datetime import datetime as dt

# metatags explained in https://community.plot.ly/t/how-to-get-a-responsive-layout/18029
# All constructor args https://github.com/plotly/dash/blob/dev/dash/dash.py
# https://dash.plot.ly/external-resources Topic on adding own css stylesheets
app = dash.Dash(
    __name__,
    server=server,
    meta_tags=[{
        "name": "viewport",
        "content": "width=device-width",
    }],
)

app.title = 'AGATHA'


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

# Create app layout
app.layout = dash_layout.new_layout()


## callback to update pie chart ##
## make it so that it displays crime per type over requested range ##
@app.callback([Output("pie-chart", "figure"),
               Output("pie-chart-title", "children")],
              [Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date'),
               Input("crime-dropdown", "value"),
               Input("location-dropdown", "value"),
               Input('my-date-picker-range-2', 'start_date'),
               Input('my-date-picker-range-2', 'end_date'),
               Input("crime-dropdown-future", "value"),
               Input("location-dropdown-future", "value")])
def update_pie_chart(start_date, end_date, selectedCrime, selectedLocation,
                     start_date_fut, end_date_fut, selectedCrime_fut, selectedLocation_fut):
    crime_code = selectedCrime
    location_code = selectedLocation

    location = "London"
    if selectedLocation:
        zoom = 15.0
        latInitial = cm.list_of_locations[selectedLocation]["lat"]
        lonInitial = cm.list_of_locations[selectedLocation]["lon"]
        location_code = cm.location_codes[selectedLocation]
        location = selectedLocation

    if selectedCrime:
        crime_code = cm.crime_mapping[selectedCrime]

    if start_date and end_date and not selectedCrime:
        start = dt.strptime(start_date, "%Y-%m-%d")
        end = dt.strptime(end_date, "%Y-%m-%d")

        start = start.strftime("%b %Y")
        end = end.strftime("%b %Y")

        # get the data set
        start_time = time.time()
        database = Connection()
        dataset = cm.database_pull_accelerated(start_date, end_date, crime_code,
                                               location_code, database)
        print(time.time() - start_time, " update_pie_chart()")
        dataset["Crime_type_num"] = dataset["crime_type"]
        dataset.replace({"crime_type": cm.crime_mapping_reverse},
                        inplace=True)

        # count number of crimes
        crime_count = [0] * 16
        crime_counts = dataset["Crime_type_num"].value_counts()
        values = list(crime_counts.values.astype(int))
        index = list(crime_counts.index.astype(int))
        labels = [cm.crime_mapping_reverse[i] for i in index]

        colors = ['rgb(61,73,154)',
                  'rgb(67,80,168)',
                  'rgb(72,86,182)',
                  'rgb(86,99,188)',
                  'rgb(100,112,193)',
                  'rgb(114,125,199)',
                  'rgb(128,138,205)',
                  'rgb(142,151,210)',
                  'rgb(156,164,216)',
                  'rgb(170,177,221)',
                  'rgb(184,190,227)',
                  'rgb(198,203,232)',
                  'rgb(212,216,238)',
                  'rgb(226,229,244)',
                  'rgb(240,241,249)',
                  'rgb(251,253,254)']

        colors = colors[0:len(labels)]

        layout = go.Layout(
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=20,
                pad=4
            ),
            template="plotly_dark",
            showlegend=False,
        )
        trace1 = {
            "labels": labels,
            "values": values,
            "textinfo": "none",
            "marker": {"colors": colors}
        }

        if start == end:
            return go.Figure(data=[go.Pie(**trace1)], layout=layout), "Total crime in " + location + " (" + start + ")"
        else:
            return go.Figure(data=[go.Pie(**trace1)],
                             layout=layout), "Total crime in " + location + " (" + start + " - " + end + ")"

    else:
        labels = []
        values = []

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(template="plotly_dark", )

        # Please return figure data and new title: x is amount of crimes, Date is the date
        return fig, "Select All Crimes and date range to see analysis"


## callback to update bar chart title ##
@app.callback([Output("bar-graph", "figure"),
               Output("bar-graph-title", "children")],
              [Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date'),
               Input("crime-dropdown", "value"),
               Input("location-dropdown", "value"),
               Input('my-date-picker-range-2', 'start_date'),
               Input('my-date-picker-range-2', 'end_date'),
               Input("crime-dropdown-future", "value"),
               Input("location-dropdown-future", "value")])
def update_bar_graph(start_date, end_date, selectedCrime, selectedLocation,
                     start_date_fut, end_date_fut, selectedCrime_fut, selectedLocation_fut):
    crime_code = selectedCrime
    location_code = selectedLocation

    location = "London"
    if selectedLocation:
        zoom = 15.0
        latInitial = cm.list_of_locations[selectedLocation]["lat"]
        lonInitial = cm.list_of_locations[selectedLocation]["lon"]
        location_code = cm.location_codes[selectedLocation]
        location = selectedLocation

    if selectedCrime:
        crime_code = cm.crime_mapping[selectedCrime]

    if start_date and end_date and not selectedLocation:
        start = dt.strptime(start_date, "%Y-%m-%d")
        end = dt.strptime(end_date, "%Y-%m-%d")

        start = start.strftime("%b %Y")
        end = end.strftime("%b %Y")

        # get the data set
        start_time = time.time()
        database = Connection()

        dataset = cm.barchart_database_pull(start_date, end_date, crime_code,
                                            database)
        print(time.time() - start_time, " update_bar_graph()")
        dataset.replace({"lsoa_name": cm.location_mapping_reverse},
                        inplace=True)

        locations = list(dataset["lsoa_name"])
        num_crimes = list(dataset["count"])
        fig = go.Figure(go.Bar(x=locations, y=num_crimes, name='Borough 1'))
        fig.update_layout(template="plotly_dark", )

        if not selectedCrime:
            selectedCrime = ""
        else:
            selectedCrime += " "

        if start == end:
            return fig, 'Boroughs with most cases ({})'.format(start)
        else:
            return fig, 'Boroughs with most cases ({} - {})'.format(
                start, end)



    else:
        x = []
        fig = go.Figure(go.Bar(x=x, y=[], name='Borough 1'))
        fig.update_layout(template="plotly_dark", )

        return fig, 'Select London and date range to see analysis'


@app.callback([Output("timeline-graph", "figure"),
               Output("timeline-graph-title", "children")],
              [Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date'),
               Input("crime-dropdown", "value"),
               Input("location-dropdown", "value"),
               Input('my-date-picker-range-2', 'start_date'),
               Input('my-date-picker-range-2', 'end_date'),
               Input("crime-dropdown-future", "value"),
               Input("location-dropdown-future", "value")])
def update_timeline(start_date, end_date, selectedCrime, selectedLocation,
                    start_date_fut, end_date_fut, selectedCrime_fut, selectedLocation_fut):
    first_date = dt(2010, 12, 1)
    last_date = dt(2019, 11, 1)

    crime_code = selectedCrime
    location_code = selectedLocation

    location = "London"
    crime_str = "all crime"
    if selectedLocation:
        zoom = 15.0
        latInitial = cm.list_of_locations[selectedLocation]["lat"]
        lonInitial = cm.list_of_locations[selectedLocation]["lon"]
        location_code = cm.location_codes[selectedLocation]
        location = selectedLocation

    if selectedCrime:
        crime_code = cm.crime_mapping[selectedCrime]
        crime_str = selectedCrime

    if start_date and end_date:
        start = dt.strptime(start_date, "%Y-%m-%d")
        end = dt.strptime(end_date, "%Y-%m-%d")

        start = start.strftime("%b %Y")
        end = end.strftime("%b %Y")

    if (start_date and end_date) or (not start_date and not end_date):

        # get the data set
        start_time = time.time()
        database = Connection()

        dataset = cm.timeline_database_pull(start_date, end_date, crime_code,
                                            location_code, database)
        print(time.time() - start_time, " update_timeline()")

        dates = list(dataset[0]["date"])
        crimes = list(dataset[0]["count"])

        if isinstance(dataset[1], pd.DataFrame):
            # When a date range has been entered
            average_crimes = list(dataset[1]["avg"])[0]
            fig = go.Figure(
                data=[go.Scatter(x=dates, y=crimes, name="# of crimes"),  # actual data,
                      {'x': [min(dates), max(dates)], 'y': [average_crimes,
                                                            average_crimes], 'name': 'avg of period'}],
                # horizontal line that represents crime level over selected period
                layout=go.Layout(
                    xaxis=dict(
                        rangeslider={'visible': True},
                        type="date"),
                    margin=dict(
                        l=20,
                        r=20,
                        b=20,
                        t=20,
                        pad=4
                    ),
                    template="plotly_dark",

                ))

        else:
            # When no date range has been entered
            fig = go.Figure(
                data=[go.Scatter(x=dates, y=crimes, name="# of crimes")],
                layout=go.Layout(
                    xaxis=dict(
                        rangeslider={'visible': True},
                        type="date"),
                    margin=dict(
                        l=20,
                        r=20,
                        b=20,
                        t=20,
                        pad=4
                    ),
                    template="plotly_dark",

                ))

        return fig, "Crime timeline for {} in {}".format(crime_str,
                                                         location)

    else:

        fig = go.Figure(
            data=[go.Scatter(x=[], y=[])],
            layout=go.Layout(
                xaxis=dict(
                    rangeslider={'visible': True},
                    type="date"),
                margin=dict(
                    l=20,
                    r=20,
                    b=20,
                    t=20,
                    pad=4
                ),
                template="plotly_dark",

            ))

    return fig, "Select full date range to see analysis"


@app.callback([Output("estm-cost", "figure"), ],
              [Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date'),
               Input("crime-dropdown", "value"),
               Input("location-dropdown", "value"),
               Input('my-date-picker-range-2', 'start_date'),
               Input('my-date-picker-range-2', 'end_date'),
               Input("crime-dropdown-future", "value"),
               Input("location-dropdown-future", "value")])
def update_estm_cost(start_date, end_date, selectedCrime, selectedLocation,
                     start_date_fut, end_date_fut, selectedCrime_fut, selectedLocation_fut):
    crime_code = selectedCrime
    location_code = selectedLocation

    if selectedLocation:
        zoom = 15.0
        latInitial = cm.list_of_locations[selectedLocation]["lat"]
        lonInitial = cm.list_of_locations[selectedLocation]["lon"]
        location_code = cm.location_codes[selectedLocation]

    if selectedCrime:
        crime_code = cm.crime_mapping[selectedCrime]

    if start_date and end_date:

        # get the data set
        start_time = time.time()
        database = Connection()
        dataset = cm.database_pull_accelerated(start_date, end_date, crime_code,
                                               location_code, database)
        print(time.time() - start_time, " update_avg_serious()")
        dataset["Crime_type_num"] = dataset["crime_type"]
        dataset.replace({"crime_type": cm.crime_mapping_reverse},
                        inplace=True)

        # count number of crimes
        num_crimes = len(dataset.index)
        days, months = cm.date_interval(start_date, end_date)
        crimes_per_day = num_crimes / days
        if not selectedLocation:
            area = cm.borough_sizes["Greater London"]/1000000
        else:
            area = cm.borough_sizes[selectedLocation]/1000000
        crime_density = round(crimes_per_day/area, 4)

        layout = go.Layout(
            annotations=[dict(text=str(crime_density), x=0.5,
            y=0.5, font_size=14, showarrow=False),
                         ],
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=20,
                pad=4
            ),
            template="plotly_dark",
            showlegend=False,
            hovermode=False,
        )

        trace1 = {
            "hole": 0.8,
            "labels": ["Crime density (per day per sqr km): " +
            str(crime_density)],
            "values": [crime_density],
            "textinfo": "none"
        }


    else:
        layout = go.Layout(
            annotations=[dict(text=str(0), x=0.5, y=0.5, font_size=14, showarrow=False),
                         ],
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=20,
                pad=4
            ),
            template="plotly_dark",
            showlegend=False,
            hovermode=False,
        )
        trace1 = {
            "hole": 0.8,
            "labels": ["No Interval Chosen"],
            "values": [0],
            "textinfo": "none",
        }

    return go.Figure(data=[go.Pie(**trace1)], layout=layout),


@app.callback([Output("avg-daily", "figure"), ],
              [Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date'),
               Input("crime-dropdown", "value"),
               Input("location-dropdown", "value"),
               Input('my-date-picker-range-2', 'start_date'),
               Input('my-date-picker-range-2', 'end_date'),
               Input("crime-dropdown-future", "value"),
               Input("location-dropdown-future", "value")])
def update_avg_daily(start_date, end_date, selectedCrime, selectedLocation,
                     start_date_fut, end_date_fut, selectedCrime_fut, selectedLocation_fut):
    crime_code = selectedCrime
    location_code = selectedLocation

    if selectedLocation:
        zoom = 15.0
        latInitial = cm.list_of_locations[selectedLocation]["lat"]
        lonInitial = cm.list_of_locations[selectedLocation]["lon"]
        location_code = cm.location_codes[selectedLocation]

    if selectedCrime:
        crime_code = cm.crime_mapping[selectedCrime]

    if start_date and end_date:

        # get the data set
        start_time = time.time()
        database = Connection()
        dataset = cm.database_pull_accelerated(start_date, end_date, crime_code,
                                               location_code, database)
        print(time.time() - start_time, " update_avg_serious()")
        dataset["Crime_type_num"] = dataset["crime_type"]
        dataset.replace({"crime_type": cm.crime_mapping_reverse},
                        inplace=True)

        # count number of crimes
        num_crimes = len(dataset.index)
        days, months = cm.date_interval(start_date, end_date)
        crimes_per_day = round(num_crimes / days, 1)

        layout = go.Layout(
            annotations=[dict(text=str(crimes_per_day), x=0.5, y=0.5, font_size=14, showarrow=False),
                         ],
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=20,
                pad=4
            ),
            template="plotly_dark",
            showlegend=False,
            hovermode=False,
        )

        trace1 = {
            "hole": 0.8,
            "labels": ["Crimes per Day: " + str(crimes_per_day)],
            "values": [crimes_per_day],
            "textinfo": "none"
        }


    else:
        layout = go.Layout(
            annotations=[dict(text=str(0), x=0.5, y=0.5, font_size=14, showarrow=False),
                         ],
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=20,
                pad=4
            ),
            template="plotly_dark",
            showlegend=False,
            hovermode=False,
        )
        trace1 = {
            "hole": 0.8,
            "labels": ["No Interval Chosen"],
            "values": [0],
            "textinfo": "none",
        }

    return go.Figure(data=[go.Pie(**trace1)], layout=layout),


@app.callback([Output("avg-serious", "figure"), ],
              [Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date'),
               Input("crime-dropdown", "value"),
               Input("location-dropdown", "value"),
               Input('my-date-picker-range-2', 'start_date'),
               Input('my-date-picker-range-2', 'end_date'),
               Input("crime-dropdown-future", "value"),
               Input("location-dropdown-future", "value")])
def update_avg_serious(start_date, end_date, selectedCrime, selectedLocation,
                       start_date_fut, end_date_fut, selectedCrime_fut, selectedLocation_fut):
    crime_code = selectedCrime
    location_code = selectedLocation

    if selectedLocation:
        zoom = 15.0
        latInitial = cm.list_of_locations[selectedLocation]["lat"]
        lonInitial = cm.list_of_locations[selectedLocation]["lon"]
        location_code = cm.location_codes[selectedLocation]

    if selectedCrime:
        crime_code = cm.crime_mapping[selectedCrime]

    if start_date and end_date:

        # get the data set
        start_time = time.time()
        database = Connection()
        dataset = cm.database_pull_accelerated(start_date, end_date, crime_code,
                                               location_code, database)
        print(time.time() - start_time, " update_avg_serious()")
        dataset["Crime_type_num"] = dataset["crime_type"]
        dataset.replace({"crime_type": cm.crime_mapping_reverse},
                        inplace=True)

        # count number of crimes
        num_crimes = len(dataset.index)
        days, months = cm.date_interval(start_date, end_date)
        crimes_per_month = round(num_crimes / months, 1)

        layout = go.Layout(
            annotations=[dict(text=str(crimes_per_month), x=0.5, y=0.5, font_size=14, showarrow=False),
                         ],
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=20,
                pad=4
            ),
            template="plotly_dark",
            showlegend=False,
            hovermode=False,
        )
        trace1 = {
            "hole": 0.8,
            "labels": ["Crimes per Month: " + str(crimes_per_month)],
            "values": [crimes_per_month],
            "textinfo": "none"
        }


    else:
        layout = go.Layout(
            annotations=[dict(text=str(0), x=0.5, y=0.5, font_size=14, showarrow=False),
                         ],
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=20,
                pad=4
            ),
            template="plotly_dark",
            showlegend=False,
            hovermode=False,
        )
        trace1 = {
            "hole": 0.8,
            "labels": ["No Interval Chosen"],
            "values": [0],
            "textinfo": "none"
        }

    return go.Figure(data=[go.Pie(**trace1)], layout=layout),


@app.callback(Output("map-graph", 'figure'),
              [Input('button', 'n_clicks'),
               Input('my-date-picker-range-2', 'end_date')],
              state=[State('my-date-picker-range', 'start_date'),
                     State('my-date-picker-range', 'end_date'),
                     State("crime-dropdown", "value"),
                     State("location-dropdown", "value"),
                     State('my-date-picker-range-2', 'start_date')])
def update_graph(n_clicks,end_date_fut,start_date, end_date, selectedCrime, selectedLocation,
                 start_date_fut):

    zoom = 10.0
    latInitial = 51.507879
    lonInitial = -0.087732
    bearing = 0

    crime_code = selectedCrime
    location_code = selectedLocation

    if start_date_fut or end_date_fut:
        return go.Figure(cm.display_predictions())

    if selectedLocation:
        zoom = 15.0
        latInitial = cm.list_of_locations[selectedLocation]["lat"]
        lonInitial = cm.list_of_locations[selectedLocation]["lon"]
        location_code = cm.location_codes[selectedLocation]

    if selectedCrime:
        crime_code = cm.crime_mapping[selectedCrime]

    dataset = pd.DataFrame(columns=['crime_type', 'date', 'latitude', 'longitude', 'Crime_type_num'])

    if start_date and end_date:
        # get the data set
        start_time = time.time()
        database = Connection()
        dataset = cm.database_pull_accelerated(start_date, end_date, crime_code,
                                               location_code, database)

        dataset["Crime_type_num"] = dataset["crime_type"]
        dataset.replace({"crime_type": cm.crime_mapping_reverse},
                        inplace=True)

    return go.Figure(
        data=[
            # Data for all points plotted
            Scattermapbox(
                lat=dataset["latitude"],
                lon=dataset["longitude"],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=dataset["crime_type"],
                marker=go.scattermapbox.Marker(
                    size=5, color=dataset["Crime_type_num"],
                    showscale=False
                )
            ),
            Scattermapbox(
                lat=[cm.list_of_locations[i]["lat"] for i in cm.list_of_locations],
                lon=[cm.list_of_locations[i]["lon"] for i in cm.list_of_locations],
                mode="markers",
                hoverinfo="text",
                text=[i for i in cm.list_of_locations],
                marker=dict(size=8, color="#ffa0a0"),
            ),
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
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
                                        "mapbox.zoom": zoom,
                                        "mapbox.center.lon": lonInitial,
                                        "mapbox.center.lat": latInitial,
                                        "mapbox.bearing": bearing,
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
    app.run_server(debug=False, port=8080)
