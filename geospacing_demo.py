import pandas as pd
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt
import shapely.speedups


london_boroughs = geopandas.GeoDataFrame.from_file('/Users/michaelpatterson/PycharmProjects/group_project/London_Borough_Excluding_MHW.shp')
crimes = pd.read_csv('/Users/michaelpatterson/PycharmProjects/group_project/polygon_demo.csv')
london_boroughs=london_boroughs.to_crs(epsg=4326)
demo_borough = london_boroughs[london_boroughs['NAME'].str.contains('Kensington', regex=False)]
print(demo_borough)


#Creates a geopandas dataframe from february predictions
geometry = [Point(xy) for xy in zip(crimes.center_x, crimes.center_y)]
df = crimes.drop(['center_x', 'center_y'], axis=1)
crs = {'init': 'epsg:4326'}
crimes_geo = geopandas.GeoDataFrame(
    df,geometry=geopandas.points_from_xy(crimes.center_x,crimes.center_y))

inside_borough = []
outside_borough = []

shapely.speedups.enable()
for i,borough in london_boroughs.iterrows():
    if i != 23:
        continue
    for j,point in crimes_geo.iterrows():
        if point.geometry.within(borough.geometry):
            inside_borough.append(point)
        else:
            outside_borough.append(point)

inside = geopandas.GeoDataFrame(inside_borough)
outside = geopandas.GeoDataFrame(outside_borough)


#code to map out London LSOA's
fig, ax = plt.subplots()
ax.axis('off')
demo_borough.geometry.plot(ax=ax, facecolor='black')
inside["geometry"].plot(ax=ax, facecolor='red')
outside["geometry"].plot(ax=ax, facecolor='blue')
plt.tight_layout()
plt.show()