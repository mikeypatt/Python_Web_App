import dash
from dash.dependencies import Input, Output
from datetime import datetime as dt


import components_plus_methods as cm
from Database import Connection
from layouts import simple_app_layout

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


app.layout = simple_app_layout()

# Update Function based on date-picker,location dropdown, and type of crime
@app.callback(
    [Output('output-container-date-picker-range', 'children'),
     Output("output-1", "children"),
     Output("output-2", "children")],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input("crime-dropdown", "value"),
     Input("location-dropdown", "value")])
def update_graph(start_date, end_date, selectedCrime, selectedLocation):
    zoom = 12.0
    latInitial = 51.507879
    lonInitial = -0.087732
    bearing = 0

    if selectedLocation:
        zoom = 15.0
        latInitial = list_of_locations[selectedLocation]["lat"]
        lonInitial = list_of_locations[selectedLocation]["lon"]

    if start_date and end_date:

        # Instantiate a Database Class
        database = Connection()
        # get the data set
        dataset = cm.database_pull(start_date, end_date, selectedCrime, selectedLocation,database)

    else:
        dataset = []

    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(start_date.split(' ')[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date.split(' ')[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here', selectedCrime, selectedLocation
    else:
        return string_prefix, selectedCrime, selectedLocation


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
