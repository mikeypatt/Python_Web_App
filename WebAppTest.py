import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_html_components as html
from pytest_dash import wait_for
from pytest_dash.application_runners import import_app

def test_application(dash_threaded):

    driver = dash_threaded.driver
    app = import_app('webApp')

    counts = {'clicks': 0}

    dash_threaded(app)

    btn = wait_for.wait_for_element_by_css_selector(driver, '#date-picker')
    btn.click()


    wait_for.wait_for_text_to_equal(driver, '#out', '')
    # assert counts['clicks'] == 2

    #app = import_app('my_app')



    #
    # app.layout = html.Div([
    #     html.Div('My test layout', id='out'),
    #     html.Button('click me', id='click-me')
    # ])
    #
    # @app.callback(
    #     Output('out', 'children'),
    #     [Input('click-me', 'n_clicks')]
    # )
    # def on_click(n_clicks):
    #     if n_clicks is None:
    #         raise PreventUpdate
    #
    #     counts['clicks'] += 1
    #     return 'Clicked: {}'.format(n_clicks)
    #
    # dash_threaded(app)
    #