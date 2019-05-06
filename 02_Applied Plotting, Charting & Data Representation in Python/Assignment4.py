
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **economic activity or measures** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **economic activity or measures**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **economic activity or measures**?  For this category you might look at the inputs or outputs to the given economy, or major changes in the economy compared to other regions.
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[8]:

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# read datafile and cleaning
df_obese = pd.read_csv('DP_LIVE_01032019110831162.csv', index_col=False, skiprows=0)
df_obese.set_index('LOCATION',inplace=True)

df_sugar = pd.read_excel('Sugar Consumption Per Capita.xlsx', sheet_name=None, skiprows=1)
df_sugar.set_index('Yearly Data',inplace=True)
df_sugar = df_sugar.iloc[:,-8:-3]

# creat a dictionary to match the country names in both datafiles
Dict_countryname = {'AUS':'Australia','CAN':'Canada','FIN':'Finland','HUN':'Hungary',
        'IRL':'Ireland','JPN':'Japan','KOR':'South Korea','LUX':'Luxembourg',
        'MEX':'Mexico','NZL':'New Zealand','SVK':'Slovakia','GBR':'United Kingdom',
        'USA':'USA','CHL':'Chile','CZE':'Czech Republic','TUR':'Turkey'}
df_obese.index = df_obese.index.to_series().map(Dict_countryname)
df_obese = df_obese.iloc[:,-3:-1]

# extract the years information from datafile because of the incompleteness in obesepopulation datafile
series_years = pd.unique(df_obese.loc[:,'TIME']) 
series_years.sort()

# plot the sugar consumption and the obese population precent of every country through years
for year in series_years:    
    df_obese_each = df_obese.loc[df_obese['TIME'] == year]
    df_sugar_each = df_sugar.loc[:,year].to_frame()
    
    df_year = df_obese_each.merge(df_sugar_each,left_index=True,right_index=True)
    df_year = df_year.rename(columns = {'Value':'Obenepopulation'})
    df_year = df_year.rename(columns = {year:'Sugarintake'})
    df_year.sort_values(by=['Sugarintake'],inplace=True)
    print(df_year)
    plt.plot(df_year.loc[:,'Sugarintake'], df_year.loc[:,'Obenepopulation'], '-o')
    plt.grid(axis='y')
    # add country name at every data point
    #for index, row in df_year.iterrows():
        #plt.annotate(index, (row['Sugarintake'],row['Obenepopulation']))
    
plt.xlabel('Sugar Consumption(Kg per year)')
plt.ylabel('obese population(aged 15+)%')
plt.legend([str(x) for x in series_years])
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.title('Sugar Cosumption and Obese Population of countries')
#plt.show()
plt.savefig('assignment4.png')





# In[ ]:



