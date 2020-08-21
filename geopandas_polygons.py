import pandas as pd
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt
import shapely.speedups

lsoas_london = geopandas.GeoDataFrame.from_file('/homes/mp2418/Downloads/statistical-gis-boundaries-london/ESRI/LSOA_2011_London_gen_MHW.shp')
list_of_points_of_interest = pd.read_csv("/homes/mp2418/Downloads/london_poi_prepared.csv")
london_police_stations = pd.read_csv("/homes/mp2418/Downloads/london_police_stations.csv")
lsoas_london=lsoas_london.to_crs(epsg=4326)


#Creates a geopandas dataframe from poi list
geometry = [Point(xy) for xy in zip(list_of_points_of_interest.longtitude, list_of_points_of_interest.latitude)]
df = list_of_points_of_interest.drop(['longtitude', 'latitude'], axis=1)
crs = {'init': 'epsg:4326'}
poi_coordinates_geo = geopandas.GeoDataFrame(
    df,geometry=geopandas.points_from_xy(list_of_points_of_interest.longtitude,list_of_points_of_interest.latitude))


#Creates a geopandas dataframe from poi list
geometry_police = [Point(xy) for xy in zip(london_police_stations.longtitude, london_police_stations.latitude)]
df = london_police_stations.drop(['longtitude', 'latitude'], axis=1)
crs = {'init': 'epsg:4326'}
police_coordinates_geo = geopandas.GeoDataFrame(
    df,geometry=geopandas.points_from_xy(london_police_stations.longtitude,london_police_stations.latitude))


poi_coordinates = poi_coordinates_geo.copy()
police_coordinates = police_coordinates_geo.copy()
pois_in_lsoas = []
police_in_lsoas = []


poi_per_lsoa = pd.DataFrame()
poi_per_lsoa["LSOA"] = lsoas_london["LSOA11CD"]

#gets the center point of each LSOA code
lsoa_centers = geopandas.GeoDataFrame()
lsoa_centers["x"] = lsoas_london.centroid.x
lsoa_centers["y"] = lsoas_london.centroid.y
poi_per_lsoa["center_x"] = lsoa_centers["x"]
poi_per_lsoa["center_y"] = lsoa_centers["y"]

shapely.speedups.enable()
for i,lsoa in lsoas_london.iterrows():

    poi_in_lsoa = []
    police_in_lsoa = []

    for j,poi in poi_coordinates.iterrows():
        if poi.geometry.within(lsoa.geometry):
            poi_in_lsoa.append(poi.geometry)
            poi_coordinates.drop(j)

    for k,police in police_coordinates.iterrows():
        if police.geometry.within(lsoa.geometry):
            police_in_lsoa.append(police.geometry)
            police_coordinates.drop(k)

    pois_in_lsoas.append(len(poi_in_lsoa))
    police_in_lsoas.append(len(police_in_lsoa))

#save the new csv file
poi_per_lsoa["POIs"] = pois_in_lsoas
poi_per_lsoa["police_stations"] = police_in_lsoas
poi_per_lsoa.to_csv(r'/homes/mp2418/PycharmProjects/geopandas/POI_LSOA.csv')


#code to map out London LSOA's
fig, ax = plt.subplots()
lsoas_london.geometry.plot(ax=ax, facecolor='black')
poi_coordinates_geo["geometry"].plot(ax=ax, facecolor='red')
plt.tight_layout()
plt.show()