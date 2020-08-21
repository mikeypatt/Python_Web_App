import numpy as np
import pandas as pd
import geopandas
from pandapower.plotting import cmap_logarithmic,cmap_continuous
from shapely.geometry import Point
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import shapely.speedups
from matplotlib import colors
lsoas_london = geopandas.GeoDataFrame.from_file('/Users/michaelpatterson/PycharmProjects/group_project/LSOA_2011_London_gen_MHW.shp')
january_stats = pd.read_csv('/Users/michaelpatterson/PycharmProjects/group_project/january.csv')
february_stats = pd.read_csv('/Users/michaelpatterson/PycharmProjects/group_project/february.csv')
london_boroughs = geopandas.GeoDataFrame.from_file('/Users/michaelpatterson/PycharmProjects/group_project/London_Borough_Excluding_MHW.shp')

january_stats["errors"] = (abs(january_stats["prediction"].astype(int)-january_stats["month_12"])/january_stats["month_12"])
print(len(lsoas_london))
errors_merged = lsoas_london.set_index('LSOA11CD').join(january_stats.set_index('lsoa_code'),how='left')
errors_merged["errors"].replace([np.inf, -np.inf], np.nan, inplace=True)
errors_merged["errors"].fillna(0.01, inplace=True)
errors_merged.replace(0, 0.01, inplace=True)

vmin = errors_merged["errors"].min()
vmax = errors_merged["errors"].max()
print(vmin)
print(vmax)
fig, ax = plt.subplots(1, figsize=(10, 6))
variable = 'errors'
colors = ["blue", "purple", "red"]
cmap,norm = cmap_logarithmic(vmin ,vmax, colors)
cmap = 'PuRd'

norm=plt.Normalize(vmin=vmin, vmax=vmax)
errors_merged.plot(column=variable,cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8')
sm = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)
cbar.set_label('Relative Error %')
ax.axis('off')
fig.savefig("borough_feb_error.png", dpi=500)
plt.show()


london_boroughs=london_boroughs.to_crs(epsg=4326)
#Creates a geopandas dataframe from february predictions
geometry = [Point(xy) for xy in zip(february_stats.center_x, february_stats.center_y)]
df = february_stats.drop(['center_x', 'center_y'], axis=1)
crs = {'init': 'epsg:4326'}
feb_prediction_geo = geopandas.GeoDataFrame(
    df,geometry=geopandas.points_from_xy(february_stats.center_x,february_stats.center_y))

feb_prediction = feb_prediction_geo.copy()

borough_prediction_counts = np.zeros(33)
shapely.speedups.enable()
for i,borough in london_boroughs.iterrows():
    for j,predictions in feb_prediction.iterrows():
        if predictions.geometry.within(borough.geometry):
            borough_prediction_counts[i]+= february_stats['prediction'].iloc[j]

borough_data = pd.DataFrame(data=borough_prediction_counts)
london_boroughs["predicted"] = borough_data
variable = 'predicted'
colors = ["blue","purple","yellow", "red"]
vmin = london_boroughs["predicted"].min()
vmax = london_boroughs["predicted"].max()
cmap,norm = cmap_logarithmic(vmin ,vmax, colors)
fig, ax = plt.subplots(1, figsize=(25,25))
london_boroughs.plot(column=variable,cmap=cmap,norm=norm, linewidth=0.8, ax=ax, edgecolor='0.8')
ax.axis('off')
fig.savefig("borough_feb.png", dpi=500)
plt.show()



february_stats['prediction'][february_stats['prediction']< 0] = 0.1
predicted_merged = lsoas_london.set_index('LSOA11CD').join(february_stats.set_index('lsoa_code'),how='left')

vmin = predicted_merged['prediction'].min()
vmax = predicted_merged['prediction'].max()
predicted_merged['normalised_prediction'] = 0.1 + (((predicted_merged['prediction']-vmin)*(50-0.1))/(50-0.1))
# set a variable that will call whatever column we want to visualise on the map
vmin = 0.1
vmax = 50
variable = 'normalised_prediction'
# # set the range for the choropleth
colors = ["blue", "purple", "red"]
cmap,norm = cmap_logarithmic(vmin ,vmax, colors)
fig, ax = plt.subplots(1, figsize=(25,25))
sm = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
predicted_merged.plot(column=variable,cmap=cmap,norm=norm, linewidth=0.8, ax=ax, edgecolor='0.8')
ax.axis('off')
cbar = fig.colorbar(sm,ax=ax,orientation="horizontal",pad=0)
ax.set_aspect('auto')
cbar.set_label('Predicted Crime Rates (Logarithmic)', size=25, weight='bold')
cbar.ax.tick_params(labelsize=25)
plt.tight_layout()
ax.axis('off')
fig.savefig("lsoa_map_feb.png", dpi=450)
plt.show()



