# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 08:00:45 2022

@author: steve
"""

import pandas as pd
import matplotlib.pyplot as plt

destin = pd.read_csv('international_transfers.csv', dtype=str)

# Clean and explode the data.

destin['declared_safeguards'] = destin['declared_safeguards'].str.replace(r'[','', regex=True)
destin['declared_safeguards'] = destin['declared_safeguards'].str.replace(r']','', regex=True)
destin['declared_safeguards'] = destin['declared_safeguards'].str.replace(r"'", "", regex=True)

destin['declared_safeguards'] = destin['declared_safeguards'].str.split(', ')

int_indiv_safe = destin.explode('declared_safeguards')

#%%

# Calculate how many data transfers to all countries without adequate decision 
# failed to disclose the transfer intentions, destination countries, and copy 
# means of the safeguard.

int_dp_clause = int_indiv_safe.query("declared_safeguards == 'dp_clause'")

noncomply_transfers = int_dp_clause.query("compliance == 'False'")

int_dp_clause = int_dp_clause.query("declared_safeguards == 'dp_clause'")
int_num_dp_clause = int_dp_clause.shape[0]

int_num_fail_intent = int_dp_clause['intention'].value_counts()['True']
int_rate_fail_intent = 1-(int_num_fail_intent/int_num_dp_clause)
print(f'\nRate of apps using standard data protection clauses noncompliant with the transfer intentions requirement: {1-(int_num_fail_intent/int_num_dp_clause)}')

int_num_fail_country = int_dp_clause['countries'].value_counts()['False']
int_rate_fail_country = int_num_fail_country/int_num_dp_clause
print(f'\nRate of apps using standard data protection clauses noncompliant with the destination country disclosure requirement: {int_num_fail_country/int_num_dp_clause}')

int_num_fail_copy = int_dp_clause['copy'].value_counts()['False']
int_rate_fail_copy = int_num_fail_copy/int_num_dp_clause
print(f'\nRate of apps using standard data protection clauses noncompliant with the copy means requirement: {int_num_fail_copy/int_num_dp_clause}')

#%%

colors = ['#648FFF','#785EF0', '#DC267F']
trans_elem = ['Transfer Intentions', 'Destination Countries', 'Copy Means']
values = [int_rate_fail_intent, int_rate_fail_country, int_rate_fail_copy]

fig1, ax1 = plt.subplots(dpi=300, figsize=(12,15))
plt.bar(trans_elem, values, color=colors)
ax1.set_title("Rates of all apps with standard data protection not complying with other GDPR requirements")
plt.xlabel("Transparency Elements")
plt.ylabel("Rate")
fig1.tight_layout()
fig1.savefig('int_fail_reasons.png')