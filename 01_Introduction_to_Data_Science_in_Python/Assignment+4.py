
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[9]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[10]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[66]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    #1.read the txt
    #2.iterate in state
    #3.iterate in uni   
    data = []   
    with open('university_towns.txt', 'r') as f:
        for line in f:
            if line.find('[edit]') > -1:
                state = line[:line.index('[')]
                continue
            if line[-2] == ':':
                continue
            if '('in line:
                region = line[:line.index('(')-1]
                data.append([state, region])
            elif ','in line:
                region = line[:line.index(',')-1]
                data.append([state, region])
            else:
                region = line
                data.append([state, region])
    df = pd.DataFrame(data,columns = ["State", "RegionName"])
    return df

get_list_of_university_towns()


# In[64]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    data = pd.read_excel(io='gdplev.xls',skiprows=219)
    data.drop(data.columns[[0,1,2,3,5,7]],axis=1,inplace=True)
    data.columns = ['Year','GDP']
 
    start = []
    for num in range(len(data)-2):
        #if data.iloc[num][1] > data.iloc[num+1][1]:
            #print('<-')
        #else:
            #print('->') 
        if (data.iloc[num][1] > data.iloc[num+1][1]) & (data.iloc[num+1][1] > data.iloc[num+2][1]):
            return data.iloc[num][0]

get_recession_start()


# In[55]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    data = pd.read_excel(io='gdplev.xls',skiprows=219)
    data.drop(data.columns[[0,1,2,3,5,7]],axis=1,inplace=True)
    data.columns = ['Year','GDP']
    
    start = get_recession_start()
    start_index = data[data['Year'].isin([start])].index.tolist()[0]
    for num in range(start_index, len(data)-2):
        if (data.iloc[num][1] < data.iloc[num+1][1]) & (data.iloc[num+1][1] < data.iloc[num+2][1]):
            return data.iloc[num+2][0]

get_recession_end()


# In[56]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    data = pd.read_excel(io='gdplev.xls',skiprows=219)
    data.drop(data.columns[[0,1,2,3,5,7]],axis=1,inplace=True)
    data.columns = ['Year','GDP']
    
    start = get_recession_start()
    start_index = data[data['Year'].isin([start])].index.tolist()[0]
    end = get_recession_end()
    end_index = data[data['Year'].isin([end])].index.tolist()[0]
    bottom = data[start_index:end_index]['GDP'].idxmin(axis=1)
    
    return data.iloc[bottom][0]

get_recession_bottom()


# In[57]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    data = pd.read_csv('City_Zhvi_AllHomes.csv')
    data.drop(data.columns[[0,3,4,5]],axis=1,inplace=True)
    data['State'] = data['State'].map(states)
    data.set_index(['State','RegionName'],inplace=True)
    for i in range(3,len(data.columns)):
        if data.columns[i-1].find('2000') > -1:
            break 
    #data = data.iloc[:,(i-1):]
    col = list(data.columns)
    col = col[0:i-1]
    data.drop(col,axis=1,inplace=1)

    quarter_hausprice = pd.DataFrame(index=data.index, columns=[])
    for i in range (len(data.columns)//3):
        col_name = str(2000 + (i//4)) + 'q' + str(i%4+1)
        quarter_hausprice[col_name] = data.iloc[:,(i*3):(i*3+3)].mean(axis=1)
    if len(data.columns)%3 >0:
        col_name = str(2000 + (i//4)) + 'q' + str(i%4+2)
        quarter_hausprice[col_name] = data.iloc[:,(i*3+4):].mean(axis=1)
    
    return quarter_hausprice

convert_housing_data_to_quarters()


# In[58]:

#stats.ttest_ind?

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    
    data = pd.read_excel(io='gdplev.xls',skiprows=219)
    data.drop(data.columns[[0,1,2,3,5,7]],axis=1,inplace=True)
    data.columns = ['Year','GDP']
    
    #1.choose the house price list between recession from house_data
    quarter_hausprice = convert_housing_data_to_quarters()
    start = get_recession_start()
    end = get_recession_bottom()
    recession_hausprice = pd.DataFrame(index=quarter_hausprice.index, columns=[])
    recession_hausprice = quarter_hausprice.loc[:,start:end]
    uni_towns = get_list_of_university_towns()

    temp = [tuple(i) for i in uni_towns.values.tolist()]   
    uni_towns_price = recession_hausprice.loc[recession_hausprice.index.isin(temp)]
    non_uni_towns_price = recession_hausprice.loc[~recession_hausprice.index.isin(temp)]
    
    uni_towns_price['mean'] = (uni_towns_price.iloc[:,0] - uni_towns_price.iloc[:,-1])/uni_towns_price.iloc[:,0]
    non_uni_towns_price['mean'] = (non_uni_towns_price.iloc[:,0] - non_uni_towns_price.iloc[:,-1])/non_uni_towns_price.iloc[:,0]
    is_uni = uni_towns_price['mean'].dropna()
    not_uni = non_uni_towns_price['mean'].dropna()
    p = ttest_ind(is_uni,not_uni)[1] 
    
    different = True if p<0.01 else False
    better = 'university town' if is_uni.mean()< not_uni.mean() else 'non-university town'
    
    return (different,p,better)

run_ttest()


# In[ ]:




# In[ ]:



