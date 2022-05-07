# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 15:42:41 2022

@author: steve
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

us_transfers = pd.read_csv('us_data_transfers.csv', dtype=str)

us_transfers['declared_safeguards'] = us_transfers['declared_safeguards'].str.replace(r'[','', regex=True)
us_transfers['declared_safeguards'] = us_transfers['declared_safeguards'].str.replace(r']','', regex=True)
us_transfers['declared_safeguards'] = us_transfers['declared_safeguards'].str.replace(r"'", "", regex=True)

# Determine how many applications declared at least one safeguard in their 
# privacy policy.

num_decl_safe = us_transfers['safeguard'].value_counts()['True']

print(f'Count of applications that declared at least one safeguard in their privacy policy: {num_decl_safe}')

# Compute how many applications that declared safeguards for international 
# tranfers also provided means of copies of the safeguard.  

num_copy = us_transfers['copy'].value_counts()['True']

print(f'\nCount of applications that also provided means of copies for its safeguards: {num_copy}')

# Create a pie chart showing the shares of apps that did not declare 
# safeguards, did declare safeguards but had no copy means, and did declare 
# safeguards and had copy means.

num_no_safe = us_transfers['safeguard'].value_counts()['False']

num_decl_safe_no_copy = num_decl_safe - num_copy

colors = ['#648FFF','#785EF0', '#DC267F']
labels = ['Did Not Declare Safeguards', 'Declared Safeguards but did not Provide Copy Means', 'Declared Safeguards and Provided Copy Means']
data = [num_no_safe, num_decl_safe_no_copy, num_copy]

fig1, ax1 = plt.subplots(dpi=300, figsize=(12,5))
plt.pie(data, labels=labels, colors=colors, autopct='%1.00f%%')
ax1.set_title("Analysis of Data Transfers to the US with Declared Safeguards and Copy Means")
fig1.tight_layout()
fig1.savefig('safeguard_composite.png')

# Calculate the number of apps that complied with the GDPR through explicit 
# consent, rather than through declared safeguards. 

us_complied_transfers = pd.read_csv("us_complied_transfers.csv", dtype=str)

comply_by_safe_copy = us_complied_transfers.query("explicit_consent == 'False' & copy == 'True'")

num_safe_copy_compl = comply_by_safe_copy.shape[0]

# Calculate the number of apps that complied with the GDPR through just 
# safeguards and copy means, and not through explicit consent? 

comply_by_consent = us_complied_transfers.query("explicit_consent == 'True' & copy == 'False'")

num_consent_compl = comply_by_consent.shape[0]

# Calculate the number of apps that complied with the GDPR through both 
# practices? 

comply_by_both = us_complied_transfers.query("explicit_consent == 'True' & copy == 'True'")

num_comply_both = comply_by_both.shape[0]

# Create a pie chart that shows how many compliant apps decided to implement 
# transfer safeguards, ask for the user's explicit consent, or used both 
# transparency elements.

elements = ['Safeguards', 'Explicit Consent', 'Safeguards and Excplicit Consent']
data = [num_safe_copy_compl, num_consent_compl, num_comply_both]

fig2, ax1 = plt.subplots(dpi=300, figsize=(12,5))
plt.pie(data, labels=elements, colors=colors, autopct='%1.00f%%')
ax1.set_title("Transparency Elements Used by Compliant Apps")
fig2.tight_layout()
fig2.savefig('compliance_analysis.png')

# Sum the number of apps that declared safeguards and met the other 
# GDPR requirements to comply. 

total_safe_copy_compl = num_safe_copy_compl + num_comply_both
print(f'Total compliant apps that declared safeguards: {total_safe_copy_compl}')

#%%

# Count how many of each sole and combined safeguards were implemented.

us_transfers.replace('', np.nan, inplace=True)

us_transfers.dropna(subset=['declared_safeguards'], inplace=True)

decl_safe = us_transfers['declared_safeguards'].value_counts()

print(f'\nFrequency of each safeguard combination implemented: \n{decl_safe}')

# Calculate the compliance rate of each sole and combined safeguard.

compl_safe = us_transfers.query("compliance == 'True'")

num_compl_safe = compl_safe['declared_safeguards'].value_counts()

safe_compl_rate = num_compl_safe/decl_safe*100

print(f'\nCompliance rate of each safeguard combination implemented: \n{safe_compl_rate}')

# Create stacked bar graphs for sole safeguards and combined safeguards. 

fig3, ax1 = plt.subplots(dpi=300, figsize=(5,8))
us_transfers.groupby('declared_safeguards')['compliance'].value_counts().unstack().plot.bar(ax=ax1, stacked=True, color=colors)
ax1.set_title("Sole and Combined Safeguards")
fig3.tight_layout()
fig3.savefig('combined_safeguards.png')

#%%

# Explode the declared_safeguards column to only show one safeguard for each 
# app. If on app has multiple safeguards, it will show as multiple entries with
# a different safeguard each time.

us_transfers['declared_safeguards'] = us_transfers['declared_safeguards'].str.split(', ')

indiv_safe = us_transfers.explode('declared_safeguards')

decl_safe = indiv_safe['declared_safeguards'].value_counts()

print(f'\nFrequency of each safeguard implemented: \n{decl_safe}')

# Calculate the compliance rate of each sole safeguard.

compl_safe = indiv_safe.query("compliance == 'True'")

num_compl_safe = compl_safe['declared_safeguards'].value_counts()

safe_compl_rate = num_compl_safe/decl_safe*100

print(f'\nCompliance rate of each safeguard implemented: \n{safe_compl_rate}')

# Create stacked bar graphs for sole safeguards safeguards. 

fig4, ax1 = plt.subplots(dpi=300, figsize=(5,8))
indiv_safe.groupby('declared_safeguards')['compliance'].value_counts().unstack().plot.bar(ax=ax1, stacked=True, color=colors)
ax1.set_title("Sole Safeguards")
fig4.tight_layout()
fig4.savefig('sole_safeguards.png')

#%%

# Calculate how many data transfers to the United States failed to disclose the
# transfer intentions, destination countries, and copy means of the safeguard.

dp_clause = indiv_safe.query("compliance == 'False'")

dp_clause = dp_clause.query("declared_safeguards == 'dp_clause'")
num_dp_clause = dp_clause.shape[0]

num_fail_intent = dp_clause['intention'].value_counts()['True']
rate_fail_intent = 1-(num_fail_intent/num_dp_clause)
print(f'\nRate of apps using standard data protection clauses noncompliant with the transfer intentions requirement: {rate_fail_intent}')

num_fail_country = dp_clause['countries'].value_counts()['False']
rate_fail_country = num_fail_country/num_dp_clause
print(f'\nRate of apps using standard data protection clauses noncompliant with the destination country disclosure requirement: {rate_fail_country}')

num_fail_copy = dp_clause['copy'].value_counts()['False']
rate_fail_copy = num_fail_copy/num_dp_clause
print(f'\nRate of apps using standard data protection clauses noncompliant with the copy means requirement: {rate_fail_copy}')

trans_elem = ['Transfer Intentions', 'Destination Countries', 'Copy Means']
values = [rate_fail_intent, rate_fail_country, rate_fail_copy]

fig5, ax1 = plt.subplots(dpi=300, figsize=(12,15))
plt.bar(trans_elem, values, color=colors)
ax1.set_title("Rates of apps transferring data to the the US with standard data protection not complying with other GDPR requirements")
plt.xlabel("Transparency Elements")
plt.ylabel("Rate")
fig5.tight_layout()
fig5.savefig('us_fail_reasons.png')