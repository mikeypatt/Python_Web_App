import dash
import dash_html_components as html
import os
import sys

from components_plus_methods import date_selector, crime_selector, location_selector

os.path.dirname(sys.modules['__main__'].__file__)
from dash.testing.composite import DashComposite
from datetime import datetime as dt
import dash_core_components as dcc
from dash.dependencies import Output, Input
from dash import Dash, callback_context, no_update
from dash.exceptions import (
    PreventUpdate,
    DuplicateCallbackOutput,
    CallbackException,
    MissingCallbackContextException,
    InvalidCallbackReturnValue,
    IncorrectTypeException,
    NonExistentIdException,
)

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


def test_date_selection_callback(dash_duo):
    app = Dash(__name__)
    app.layout = html.Div([date_selector(),
                           html.Div(html.Div([1.5, None, "string",
                                              html.Div(id='output-container-date-picker-range')])), ])
    call_count = 0

    @app.callback(
        Output('output-container-date-picker-range', 'children'),
        [Input('my-date-picker-range', 'start_date'),
         Input('my-date-picker-range', 'end_date')])
    def update_output(start_date, end_date):
        if not start_date and not end_date:
            return PreventUpdate
        nonlocal call_count
        call_count += 1

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
            return 'Select a date to see it displayed here'
        else:
            return string_prefix

    dash_duo.start_server(app)
    date_picker = dash_duo.driver.find_element_by_xpath("// *[ @ id ='my-date-picker-range']/div")
    start_input = date_picker.find_element_by_xpath("//*[@id='my-date-picker-range']/div/div/div/div[1]/input")
    start_input.send_keys("09/11/2019")
    end_input = date_picker.find_element_by_xpath("//*[@id='my-date-picker-range']/div/div/div/div[3]/input")
    end_input.send_keys("10/11/2019")

    dash_duo.wait_for_text_to_equal("#output-container-date-picker-range",
                                    "You have selected: Start Date: September 11, 2019 | End Date: October 11, 2019",
                                    timeout=8.0)

    #  and one for selecting the end date and one for selecting the starting date
    assert call_count == 2


def test_crime_type_callback(dash_duo):
    app = Dash(__name__)
    app.layout = html.Div([crime_selector(),
                           html.Div(html.Div([1.5, None, "string", html.Div(id="output-1")])), ])

    call_count = 0

    # Call back from Crime Selector Function to update
    @app.callback(Output("output-1", "children"), [Input("crime-dropdown", "value")])
    def update_output(selectedCrime):
        if not selectedCrime:
            return PreventUpdate
        nonlocal call_count
        call_count += 1
        return selectedCrime

    # Instantiates a Mock Server to run the app
    dash_duo.start_server(app)
    input1 = dash_duo.select_dcc_dropdown("#crime-dropdown", index=0)
    dash_duo.wait_for_text_to_equal("#output-1", "Anti-social behaviour", timeout=5.0)
    dash_duo.percy_snapshot(name="simple-callback-2")

    assert call_count == 1  # Only one for selecting the given crime


def test_location_selection_callback(dash_duo):
    app = Dash(__name__)
    app.layout = html.Div([location_selector(),
                           html.Div(html.Div([1.5, None, "string", html.Div(id="output-1")])), ])

    call_count = 0

    @app.callback(Output("output-1", "children"), [Input("location-dropdown", "value")])
    def update_output(selectedLocation):
        if not selectedLocation:
            return PreventUpdate

        nonlocal call_count
        call_count += 1
        return selectedLocation

    dash_duo.start_server(app)
    input1 = dash_duo.select_dcc_dropdown("#location-dropdown", index=4)
    dash_duo.wait_for_text_to_equal("#output-1", "Bromley", timeout=5.0)
    dash_duo.percy_snapshot(name="simple-callback-2")

    # one for selecting the location (Borough)
    assert call_count == 1
