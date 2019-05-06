
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[24]:

get_ipython().magic('matplotlib notebook')
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv',parse_dates=[1])

df['Year'] = df['Date'].map(lambda t: t.to_datetime().year)
df['Month'] = df['Date'].map(lambda t: t.to_datetime().month)
df["Day"] = df['Date'].map(lambda t: t.to_datetime().day)

df['Exactday'] = pd.to_datetime(df[['Year','Month','Day']]).dt.dayofyear
df['Exactday'] = df['Exactday'].astype(int)

df.drop(df['Exactday']==60)
df['Exactday'] = df['Exactday'].apply(lambda x: x-1 if x > 60 else x)

df_2015 = df[df['Year'] == 2015]
df = df[df['Year'] < 2015]

df_MAX = df[df['Element']=='TMAX']
df_MIN = df[df['Element']=='TMIN']

df_MAX.sort_values(by='Exactday',inplace=True)
df_MIN.sort_values(by='Exactday',inplace=True)
df_MAX = df_MAX.reset_index(drop=True)
df_MIN = df_MIN.reset_index(drop=True)

df2_MAX = df_MAX.iloc[df_MAX.groupby(['Exactday']).apply(lambda x: x['Data_Value'].idxmax())]
df2_MIN = df_MIN.iloc[df_MIN.groupby(['Exactday']).apply(lambda x: x['Data_Value'].idxmin())]

for index, row in df_2015.iterrows():
    d = row['Exactday']    
    if (row['Data_Value']<df2_MAX[df2_MAX['Exactday']==d].Data_Value.values) and (row['Data_Value']>df2_MIN[df2_MIN['Exactday']==d].Data_Value.values):
        df_2015.drop([index],inplace=True)

plt.figure()
plt.plot(df2_MAX['Data_Value'].values,'-b',df2_MIN['Data_Value'].values,'-g')
plt.scatter(df_2015['Exactday'].values, df_2015['Data_Value'].values,c='r', marker='.')

plt.xlabel('record high and low temperatures by day of the year over the period 2005-2014')
plt.ylabel('temperature (tenths of degrees C)')
plt.title('contrast of record high and low temperatures(2015 and past 10 years)')
plt.legend(['record high', 'record low', 'broken values in 2015'])
plt.gca().fill_between(range(len(df2_MAX)), df2_MAX['Data_Value'].values, df2_MIN['Data_Value'].values, facecolor='grey', alpha=0.25)

