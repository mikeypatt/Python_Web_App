import json

import dash
import dash_core_components as dcc
import geopandas
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import plotly.graph_objs as go
import numpy as np
import dash_daq as daq
from urllib.request import urlopen
import json

#from webApp import cache
from pandapower.plotting import cmap_logarithmic

from server import cache
from Database import Connection

from dateutil.rrule import rrule, MONTHLY

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
    "Other crime": 13,
    "Violent crime":14,
    "Public disorder and weapons":15
}

crime_mapping_reverse = dict([[v,k] for k,v in crime_mapping.items()])

borough_sizes = {
    "Barking and Dagenham": 36078534,
    "Barnet": 86738702,
    "Bexley": 60553922,
    "Brent": 43252801,
    "Bromley": 150141611,
    "Camden":21755900,
    "Croydon": 86531503,
    "Ealing": 55529345,
    "Enfield": 82206223,
    "Greenwich": 47344983,
    "Hackney": 19062312,
    "Hammmersmith and Fulham":16394625 ,
    "Haringey": 29577664,
    "Harrow": 50478868,
    "Havering": 112275985,
    "Hillingdon": 115694769,
    "Hounslow": 55969643,
    "Islington": 14866532,
    "Kensington and Chelsea":12121144 ,
    "Kingston upon Thames": 37244029,
    "Lambeth":26832277 ,
    "Lewisham": 35146139,
    "Merton": 37606627,
    "Newham": 36208034,
    "Redbridge": 56409941,
    "Richmond upon Thames": 57420036,
    "Southwark": 28852468,
    "Sutton": 43848499,
    "Tower Hamlets": 19761609,
    "Waltham Forest": 38823922,
    "Wandsworth": 34265543,
    "Westminster": 21471001,
    "City of London": 3082086,
    "Greater London": 1573547276,
}

location_codes = {
    "Barking and Dagenham": 0,
    "Barnet":1,
    "Bexley":2,
    "Brent":3,
    "Bromley":4,
    "Camden":5,
    "City of London":6,
    "Croydon": 7,
    "Ealing":8,
    "Enfield":9,
    "Greenwich":10,
    "Hackney":11,
    "Hammersmith and Fulham":12,
    "Haringey":13,
    "Harrow":14,
    "Havering": 15,
    "Hillingdon":16,
    "Hounslow":17,
    "Islington": 18,
    "Kensington and Chelsea": 19,
    "Kingston upon Thames": 20,
    "Lambeth": 21,
    "Lewisham":22,
    "Merton": 23,
    "Newham": 24,
    "Redbridge": 25,
    "Richmond upon Thames":26,
    "Southwark": 27,
    "Sutton":28,
    "Tower Hamlets":29,
    "Waltham Forest": 30,
    "Wandsworth": 31,
    "Westminster": 32
}

location_mapping_reverse = dict([[v,k] for k,v in location_codes.items()])

list_of_locations = {
    "Barking and Dagenham": {"lat": 51.5607, "lon": 0.1557},
    "Barnet": {"lat": 51.6252, "lon": -0.1517},
    "Bexley": {"lat": 51.4549, "lon": 0.1505},
    "Brent": {"lat": 51.5588, "lon": -0.2817},
    "Bromley": {"lat": 51.4039, "lon": 0.0198},
    "Camden": {"lat": 51.5290, "lon": -0.1255},
    "City of London": {"lat": 51.5155, "lon": -0.0922},
    "Croydon": {"lat": 51.3714, "lon": -0.0977},
    "Ealing": {"lat": 51.5130, "lon": -0.3089},
    "Enfield": {"lat": 51.6538, "lon": -0.0799},
    "Greenwich": {"lat": 51.4892, "lon": 0.0648},
    "Hackney": {"lat": 51.5450, "lon": -0.0553},
    "Hammersmith and Fulham": {"lat": 51.4927, "lon": -0.2339},
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

def date_interval(start_date, end_date):
    """
    Returns a tuple showing the time interval in (days, months) between the
    chosen dates. 1 month taken to = 30.4375 days (weighted average)
    e.g. print(date_interval("2020-08-01", "2020-09-05"))
    returns(days, months)
    """
    start = dt.strptime(start_date, "%Y-%m-%d")
    end = dt.strptime(end_date, "%Y-%m-%d")
    days_per_month = 30.4375

    months = (end.year - start.year)*12 + (end.month - start.month) + 1

    days = days_per_month*months

    return (days, months)

def prediction_pull(database):

    database.connect()
    query = 'SELECT * from public."CRIME_PREDICTION_predictions"'
    ans = pd.read_sql(query, database.connection)
    database.disconnect()
    return ans

def display_predictions():

    mapbox_key = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

    database = Connection()
    predicted_merged_2 = prediction_pull(database)
    colors = ["blue", "purple", "red"]
    with urlopen('https://raw.githubusercontent.com/mikeypatt/json_file_crime/master/LSOA_2011.json') as response:
        j_file = json.load(response)

    i = 1
    for feature in j_file["features"]:
        feature['id'] = str(i).zfill(2)
        i += 1

    print(j_file["features"])
    print(predicted_merged_2['id'])

    fig = go.Figure(go.Choroplethmapbox(geojson=j_file, locations=predicted_merged_2.id,
                                        z=predicted_merged_2.prediction,
                                        showscale=False,
                                        colorscale=colors, zmin=0, zmax=20, ids=predicted_merged_2.LSOA11NM,
                                        text=predicted_merged_2.LSOA11NM, hoverinfo='z+text'))
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=mapbox_key,
                      mapbox_zoom=10, mapbox_center={"lat": 51.5074, "lon": -0.1278})
    fig.update_layout(autosize=True,height=1300, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig



def months(start_month, start_year, end_month, end_year):
    """
    Returns a list of stings conatining all month/ years between these dates
    e.g. print months(11, 2010, 2, 2011)
    returns: ['2010-11-01', '2010-12-01', '2011-01-01', '2011-02-01']
    """
    start = dt(start_year, start_month, 1)
    end = dt(end_year, end_month, 1)
    dates = []
    for d in rrule(MONTHLY, dtstart=start, until=end):
        if d.month < 10:
            dates.append(str("{}-0{}-01").format(d.year, d.month))  
        else:
            dates.append(str("{}-{}-01").format(d.year, d.month))

    return dates

@cache.memoize(timeout=300)
def timeline_database_pull(start_date, end_date, selectedCrime, selectedLocation, database):
    
    if start_date and end_date:
        start = start_date[:-2]+"01"
        end = end_date[:-2]+"01"
     
    if not start_date and not end_date:
        query = "SELECT date, count(*) "\
              "FROM nick_crime_data "\
              "group by date "\
              "order by date asc "
        query2 = 0

    elif selectedCrime and not selectedLocation:
        query = "SELECT date, count(*) "\
              "FROM nick_crime_data "\
              "where crime_type ={} "\
              "group by date "\
              "order by date asc ".format(selectedCrime)
        
        query2 = "select avg(count) from (SELECT count(*) "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= "\
              "'{}'::date and crime_type ={} "\
              "group by date) as foo ".format(start, end, selectedCrime)


    elif selectedCrime and selectedLocation:
        query = "SELECT date, count(*) "\
              "FROM nick_crime_data "\
              "where crime_type ={} and lsoa_name = {} "\
              "group by date "\
              "order by date asc ".format(selectedCrime, selectedLocation)
        
        query2 = "select avg(count) from (SELECT count(*) "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= "\
              "'{}'::date and crime_type ={} and lsoa_name = {} "\
              "group by date) as foo ".format(start, end, selectedCrime,
              selectedLocation)


    elif selectedLocation and not selectedCrime:
        query = "SELECT date, count(*) "\
              "FROM nick_crime_data "\
              "where lsoa_name ={} "\
              "group by date "\
              "order by date asc ".format(selectedLocation)
        
        query2 = "select avg(count) from (SELECT count(*) "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= "\
              "'{}'::date and lsoa_name ={} "\
              "group by date) as foo ".format(start, end, selectedLocation)



    elif not selectedLocation and not selectedCrime:
        query = "SELECT date, count(*) "\
              "FROM nick_crime_data "\
              "group by date "\
              "order by date asc "
        
        query2 = "select avg(count) from (SELECT count(*) "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= "\
              "'{}'::date "\
              "group by date) as foo ".format(start, end)
      


    database.connect()
    timeline = pd.read_sql(query, database.connection)
    if query2 != 0:
        curr_value = pd.read_sql(query2, database.connection)
    else:
      curr_value = 0
    database.disconnect()
    return timeline, curr_value




@cache.memoize(timeout=300)
def barchart_database_pull(start_date, end_date, selectedCrime, database):
    start = start_date[:-2]+"01"
    end = end_date[:-2]+"01"

    if selectedCrime:
        query = "SELECT lsoa_name, count(*) "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= '{}'::date and crime_type ={} "\
              "group by lsoa_name "\
              "order by count(*) desc "\
              "limit 5 ".format(start, end, selectedCrime)
    else:
        query = "SELECT lsoa_name, count(*) "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= '{}'::date "\
              "group by lsoa_name "\
              "order by count(*) desc "\
              "limit 5 ".format(start, end)
    database.connect()
    ans = pd.read_sql(query, database.connection)
    database.disconnect()
    return ans

@cache.memoize(timeout=300)
def database_pull_accelerated(start_date, end_date, selectedCrime, selectedLocation, database):
    start = start_date[:-2]+"01"
    end = end_date[:-2]+"01"
    
    if selectedCrime and not selectedLocation:
         query = "SELECT crime_type, date, latitude, longitude "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= '{}'::date "\
              "and crime_type = {} "\
              .format(start, end, selectedCrime)

    elif selectedCrime and selectedLocation:
        query = "SELECT crime_type, date, latitude, longitude "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= '{}'::date "\
              "and crime_type = {} and lsoa_name = {}"\
              .format(start, end, selectedCrime, selectedLocation)

    elif selectedLocation and not selectedCrime:
        query = "SELECT crime_type, date, latitude, longitude "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= '{}'::date "\
              "and lsoa_name = {} "\
              .format(start, end, selectedLocation)


    elif not selectedLocation and not selectedCrime:
       query = "SELECT crime_type, date, latitude, longitude "\
              "FROM nick_crime_data "\
              "where date >= '{}'::date and date <= '{}'::date "\
              .format(start, end, selectedCrime)

    database.connect()
    print(query)
    ans = pd.read_sql(query, database.connection)
    database.disconnect()
    return ans


@cache.memoize(timeout=300)
def database_pull(start_date, end_date, selectedCrime, selectedLocation, database):
    #database = Connection()
    start_date_string = dt.strptime(start_date, "%Y-%m-%d")
    end_date_string = dt.strptime(end_date, "%Y-%m-%d")

    start_yearPicked = start_date_string.year
    start_monthPicked = start_date_string.month
    start_dayPicked = start_date_string.day

    end_yearPicked = end_date_string.year
    end_monthPicked = end_date_string.month
    end_dayPicked = end_date_string.day

    # List of dates
    dates = months(start_monthPicked, start_yearPicked, end_monthPicked,
    end_yearPicked)  


    
    query_list = []

    if selectedCrime and not selectedLocation:
        for date in dates:
            for location in range(33):
                # Database Query
                query_code = (date, selectedCrime, location)
                query_list.append(query_code)

    elif selectedCrime and selectedLocation:
        for date in dates:
            # Database Query
            query_code = (date, selectedCrime, selectedLocation)
            query_list.append(query_code)



    elif selectedLocation and not selectedCrime:
        for date in dates:
            for crime in range(16):
                # Database Query
                query_code = (date, crime, selectedLocation)
                query_list.append(query_code)



    elif not selectedLocation and not selectedCrime:
        for date in dates:
            for crime in range(16):
                for location in range(33):
                    # Database Query
                    query_code = (date, crime, location)
                    query_list.append(query_code)




    database.crime_date_queried = True
    dataframe_list = []
    database.connect()
    for query_code in query_list:
        dataset = query_database(query_code, database)
        dataframe_list.append(dataset)
    database.disconnect()
   
    if len(dataframe_list) > 0:
        return pd.concat(dataframe_list)

@cache.memoize(timeout=300)
def query_database(query_code, database):
    query = "SELECT crime_type, date, latitude, longitude from nick_crime_data"\
    " WHERE date(date) = date('{}') AND"\
    " crime_type = {} AND lsoa_name = {} ".format(query_code[0], query_code[1],
    query_code[2])
    ans = pd.read_sql(query, database.connection)
    return ans

# Function to enable selection of the given crime type from the database
def crime_selector():
    return dcc.Dropdown(id="crime-dropdown",
                        options=[{"label": i, "value": i} for i in crime_mapping],
                        placeholder="All Crimes")


# Function to enable selection of the London Borough from the database
def location_selector():
    return dcc.Dropdown(id="location-dropdown",
                        options=[{"label": i, "value": i} for i in list_of_locations],
                        placeholder="London")

def fut_crime_selector():
    return dcc.Dropdown(
                        id = "crime-dropdown-future",
                        options=[{"label": i, "value": i} for i in crime_mapping],
                        placeholder="All Crimes")


# Function to enable selection of the London Borough from the database
def fut_location_selector():
    return dcc.Dropdown(
                        id ="location-dropdown-future",
                        options=[{"label": i, "value": i} for i in list_of_locations],
                        placeholder="London")

# Function to enable selection of date of crimes to be displayed
def date_selector_past():
    return dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(2019, 1, 1),
        max_date_allowed=dt(2020, 1, 31),
        initial_visible_month=dt(2019, 9, 1),
        day_size=52,
        with_portal=True,
        style={"border": "0px solid black",
               "background-color": '#343332'})

def date_selector_future():
    return dcc.DatePickerRange(
        id='my-date-picker-range-2',
        min_date_allowed=dt(2020, 2, 1),
        max_date_allowed=dt(2020, 2, 29),
        initial_visible_month=dt(2020, 2, 1),
        day_size=52,
        with_portal=True,
        style={"border": "0px solid black",
               "background-color": '#343332'})

