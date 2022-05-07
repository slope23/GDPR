# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:47:02 2022

@author: steve
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

type3 = pd.read_csv('T3_results.csv', dtype=str, sep=';')

type3.drop(columns='Unnamed: 0', inplace=True)

#%% 

# Create a new dataframe, compli, with just the requirements of the GDPR for 
# third-party transfers in absence of adequacy decision. 

col = ['apk', 'intention', 'transferred_countries', 'declared_safeguards', 'explicit_consent', 'countries', 'safeguard', 'copy']

compli_test = type3[col]

# Add a column testing for if the apps comply with the all of the GDPR 
# requirements.

conditions = (compli_test['intention'] == 'True') & (compli_test['countries'] == 'True') & (((compli_test['safeguard'] == 'True') & (compli_test['copy'] == 'True')) | (compli_test['explicit_consent'] == 'True'))

compli_test['compliance'] = np.where(conditions, True, False)

#%% 

# Create a new dataframe, destin, with each list item under 
# 'transferred_countries' being its own separate row.

destin = compli_test.copy()

destin['transferred_countries'] = destin['transferred_countries'].str.replace(r'[','', regex=True)
destin['transferred_countries'] = destin['transferred_countries'].str.replace(r']','', regex=True)
destin['transferred_countries'] = destin['transferred_countries'].str.replace(r"'", "", regex=True)

destin['transferred_countries'] = destin['transferred_countries'].str.split(', ')

destin = destin.explode('transferred_countries')

#%% 

# Compare the number of data transfers to each country. Create a bar graph 
# showing this.

int_transfers = destin['transferred_countries'].value_counts()

print(f'International Data Transfers to each Country: \n{int_transfers}\n')

fig1, ax1 = plt.subplots(dpi=300, figsize=(8,10))
int_transfers.plot.bar()
ax1.set_title("International Data Transfers to each Country")
plt.xlabel("Destination Countries")
plt.ylabel("Data Transfers")
fig1.tight_layout()
fig1.savefig('destination_countries.png')

# Create a dataframe, comply_transfers, with only the apps that comply with 
# GDPR requirements for data transfers. Duplicate destin and drop all
# entries with False values for the 'compliance' column. 

comply_transfers = destin.query("compliance == True")

# Count the number of compliant data transfers to each country. Calculate the 
# compliance rate for each country.

country_compli = comply_transfers['transferred_countries'].value_counts()

print(f'International Data Transfers Compliant with the GDPR per Destination Country: \n{country_compli}\n')

compli_rate = country_compli/int_transfers*100

print(f'Compliance Rates per Country: \n{round(compli_rate, 2)}\n')

#%%

comply_transfers.to_csv('us_complied_transfers.csv', index=False)

# Because the compliance rate for transfers to all the other countries is 
# 0.00%, I will be analyzing the relationship between safeguards and an app's
# likelihood of complying with the GDPR for only data transfers to the United 
# States

us_transfers = destin.query("transferred_countries == 'United States'")

destin.to_csv('international_transfers.csv', index=False)