"""
KAGGLE - WALMAR RECRUITING - SALES FORECAST
https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting

Questions:
    1. What are the biggest stores? (45)
    2. What are the biggest departments? (98)
    3. How many departments by store?
    4. How is it related with type of store? size or departments in store?
    5. Stores and Dept are seasonal?
    6. What is the holiday impact?
    7. Features: temperature different by store?
    #TODO : check EDA: temperature differnet by store?
    #TODO : check EDA: holiday and date same?    

Objective:
    Minimize WMAE (weighted mean absolute error),
    weight = 5 if holiday, else 1

Modelling
    # TODO: benchmark model: simplistic model: averages
"""


# ========================================================================
# IMPORT LIBRARIES
# ========================================================================
import numpy as np
import pandas as pd


# ========================================================================
# IMPORT DATA
# ========================================================================
print('\n\n>>> IMPORTING DATA SETS')
dftr     = pd.read_csv('train.csv')
dfts     = pd.read_csv('test.csv')
features = pd.read_csv('features.csv')
stores   = pd.read_csv('stores.csv')
holidays = pd.read_csv('holidays.csv')


# ========================================================================
# CREATE DICTIONARIES FROM dfft, stores and holidays
# dict_holidays: {date: holiday}
#                e.g.: dict_holidays['2010-12-02'] returns 'Super_Bowl'
# ========================================================================
print('\n\n>>> CREATING DICTIONARIES FOR HOLIDAYS')
dict_holidays = holidays.set_index('date')['holiday'].to_dict()
features['store_date'] = [str(features.loc[i,'Store'])+'_'+features.loc[i,'Date'] for i in range(len(features))]

# Create list of dates and relate it to holidays
dates = pd.DataFrame(np.unique(dftr['Date']),columns=['date'])
holidays_special = holidays['date']
holidays_all = np.unique(dftr.loc[dftr['IsHoliday']==True,'Date'])
for i in range(len(dates)):
    date = dates.loc[i,'date']
    if date in list(holidays_all):
        output = 'Others'
    else:
        output = 0
    if date in list(holidays_special):
        output = dict_holidays[date]
    dates.loc[i,'Holiday']=output


# ========================================================================
# MAP TEMPERATURE, TYPE, SIZE AND HOLIDAYS TO DATAFRAME 
# ========================================================================
print('\n\n>>> MAPPING: TEMPERATURE, TYPE, SIZE, HOLIDAYS TO DF')

# Map temperature:
dftr['store_date'] = [str(dftr.loc[i,'Store'])+'_'+dftr.loc[i,'Date'] for i in range(len(dftr))]
dftr = pd.merge(dftr, features[['store_date','Temperature','Unemployment',
                                'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']], 
                how='left', left_on='store_date',right_on='store_date')

# Map type and size:
dftr = pd.merge(dftr, stores, how='left', left_on='Store',right_on='Store')

# Map holidays:
dftr = pd.merge(dftr, dates, how='left', left_on='Date', right_on='date')

# Select variables:
var_selected = ['Store','Dept','Date','Weekly_Sales','Temperature','Type','Size','Holiday']
df = dftr[var_selected]

print('>>> Selected dataframe: {}'.format(df.shape))



# ========================================================================
# MAP TEMPERATURE, TYPE, SIZE AND HOLIDAYS TO DATAFRAME 
# ========================================================================
print('\n\n>>> EXPORTING TO CSV: treated_data.csv')
export_file='treated_data.csv'
df.to_csv(export_file)


print('\n\n>>> COMPLETED.')
