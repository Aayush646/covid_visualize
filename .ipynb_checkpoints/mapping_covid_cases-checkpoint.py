import pandas as pd
import geopandas as gpd
import PIL
import io



print("Reading in the csv data")
data = pd.read_csv('time_series_covid19_confirmed_global.csv')

print("Group the data by the country")
data = data.groupby('Country/Region').sum()

print("Drop Lat and Lon columns")
data = data.drop(columns=['Lat', 'Long'])

print("Create a transpose of the dataframe")
data_transposed= data.T

#data_transposed.plot(y= ['Nepal','India','China'], use_index= True, figsize= (10,10), marker='*')

print("Read in the world map shapefile")
world = gpd.read_file('World_Map.shp')

world.replace('Brunei Darussalam','Brunei', inplace = True)
world.replace('Cabo Verde','Cabo Verde',inplace = True)
world.replace('Congo','Congo (Brazzaville)',inplace = True)
world.replace('Democratic Republic of the Congo', 'Congo (Kinshasa)', inplace = True)
world.replace('Czech Republic', 'Czechia', inplace = True)
world.replace('Swaziland', 'Eswatini', inplace = True)
world.replace('Iran (Islamic Republic of)', 'Iran', inplace = True)
world.replace('Korea, Republic of','Korea South', inplace = True)
world.replace("Lao People's democratic Republic", 'Laos', inplace = True)
world.replace('Libyan Arab Jamahiriya', 'Libiya', inplace = True)
world.replace('Republic of Moldova','Moldova', inplace = True)
world.replace('The former Yugoslav Republic of Mecedonia','North Macedonia', inplace = True)
world.replace('Syrian Arab Republic','Syria', inplace = True)
world.replace('Taiwan','Taiwan*', inplace = True)
world.replace('United Republic of Tanzania','Tanzania', inplace = True)
world.replace('United States','US', inplace = True)
world.replace('Paleatine','West Bank and Gaza', inplace = True)

#Checking the names of the countries for any discrepancies
# =============================================================================
# for index, row in data.iterrows():
#     if index not in world['NAME'].to_list():
#         print(index+' is not in the list')
#     else:
#         pass
# 
# =============================================================================
print("Merging the data with world")
merge = world.join(data, on = 'NAME', how = 'right')
image_frames=[] 
for dates in merge.columns.to_list()[60:68]:
    #print(dates)

    #Plot
    ax = merge.plot(column=dates, 
                    cmap = 'OrRd',
                    figsize=(10,10),
                    legend = True,
                    scheme = 'user_defined', 
                    classification_kwds = {'bins':[10, 20, 50, 100, 500, 1000, 5000, 10000, 500000]},
                    edgecolor='black',
                    linewidth = 0.4)
#  Add a title to the map
    ax.set_title('Total Confirmed Coronavirus Cases:'+ dates, fontdict =
            {'fontsize': 20},pad = 12.5)

    #Removing the axis
    ax.set_axis_off()
    
    #Move the legend
    ax.get_legend().set_bbox_to_anchor((0.18,0.6))
    
    img = ax.get_figure()
    
    f = io.BytesIO()
    img.savefig(f, format = 'png',bbox_inches = 'tight')
    f.seek(0)
    image_frames.append(PIL.Image.open(f))
    
#GIF file
image_frames[0].save('Dynamicc Map.gif', format= 'GIF',
                      append_images = image_frames[1:],
                      save_all = True, duration = 300,
                      loop = 3)
f.close()  