# Appropriate Safeguards and the GDPR

## About

The General Data Protection Regulation (GDPR) aims to ensure that all personal data processing activities are fair and transparent for the European Union (EU) citizens, regardless of whether these are carried out within the EU or anywhere else. To this end, it sets strict requirements to transfer personal data outside the EU. The GDPR recognizes three possible coss-border transfer types. This project will be focusing on third-party data transfers to countries that do not have data protection regulations that are equivalent to the GDPR, as determined by the European Commission. These transfers are known as international transfers without adequacy decision. For international transfers without adequacy decisions to comply with the GDPR, apps need to disclose their intentions for transfering personal data and the destination countries the data is being sent to. Apps then must either adopt "appropriate safeguards" for international transfer and provide means to obtain a copy the safeguard(s), or they may require the explicit consent of the data subject to transfer their data through an affirmative action. The GDPR defines the following four safeguards as assurance mechanisms for international transfers: Standard Data Protection Clauses, Binding Corporate Rules, Approved Codes of Conduct and Approved Certification Schemes. 

I am interested in finding a relationship between each appropriate safeguard for international data transfers and the likelihood of one of the Android appscomplying with the GDPR. This project will first reveal the number of data transfers to each country analyzed apps are sending personal data to and compare the compliance rates of data transfers per country. Next, I will analyze the use of safeguards by compliant and noncompliant apps. Lastly, this project will determine the most common reasons for an app with at least one declared safeguard not complying with the GDPR.

## Data Source

To access the data used in this analysis, visit the following site:
https://data.mendeley.com/datasets/drx5nc3hr4/

Click and download the 'T3_results.csv' file. 

This data comes from one of three files, each for the different data transfer types, analyzing a total of 100 Android apps for a study by Danny S. Guamán, Xavier Ferrer, Jose M. del Alamo, and Jose Such from the Polytechnic University of Madrid. The 100 analyzed apps and their privacy polices are derived from two sources: a subset of 44 policies from the APP-350 corpus and a subset of 56 policies of popular Android apps, making this sample not representative of all Android apps. Therefore, this will be a study of only the analyzed apps, with a purpose of testing the methodology to repeat this study with a more representative sample of Android apps. No conclusions about Android apps and their compliance with the GDPR should be reached from this analysis. 

## Order of Running the Scripts

#### 1) destin_countries.py:
This script begins to clean and select only the necessary data from the *'T3_results.csv'* file for this analysis. Using the information from each of the requirement columns, a compliance column was created to clarify if an app met all of the GDPR's requirements for data transfers. The dataset also includes what countries the data is being sent to and the appropriate safeguards used for data transfers, if any. The script goes on to calculate the compliance rates of data transfers to each country. This comparison is visually shown in *destination_countries.png*. After noticing all compliant data transfers from the analyzed apps are to the United States, a new csv file, *'us_complied_transfers.csv'*, was created for further analysis in the second script, **safeguard_analysis.py**. *'international_transfers.csv'* is another output file meant to analyze data transfers to all countries for the third script, **sdp_analysis.py**. 

#### 2) safeguard_analysis.py: 
The purpose of this script is to analyze the relationship between the use of appropriate safeguards for data transfers to the United States and the likelihood of an app's compliance with the GDPR. After cleaning the 'declared_safeguards' column from the *'us_complied_transfers.csv'* file, I found how many apps declared safeguards and provided copy means (*safeguard_composite.png*), compared the use of appropriate safeguards and explcit consent among compliant apps (*compliance_analysis.png*), and calculated the compliance rate for each safeguard(s) (*combined_safeguards.png* and *sole_safeguards.png*). Because the majority of the analyzed apps with declared safeguards used Standard Data Protection Clauses, this script goes on to determine how many of these apps failed to disclose the transfer intentions, target countries, and/or copy means of the safeguard (*us_fail_reasons.png*).  

#### 3) sdp_analysis.py: 
Like in the second script (**safeguard_analysis.py**), this script will determine why apps that implemented Standard Data Protection Clauses failed to comply with the GDPR, but for data transfers to all countries. The input file for this script is *'us_complied_transfers.csv'*, one of the csv files made from the first script, **destin_countries.py**. The output file for this script is *int_fail_reasons.png*.

## Results

The following are major findings from analyzing the selected apps for this study:
* Most international data transfers without adequacy decision and all compliant data transfer are to the United States. (See [*destination_countries.png*](destination_countries.png).)
* Most data transfers to the United States did not declare safeguards. (See [*safeguard_composite.png*](safeguard_composite.png).)
* Appropriate safeguards are a much more popular transparency element than explicit consent. (See [*compliance_analysis.png*](compliance_analysis.png).)
* Standard Data Protection Clauses are by far the most used appropriate safeguards by the analyzed Android apps sending personal data to a third party in the United States. (See [*combined_safeguards.png*](combined_safeguards.png) and [*sole_safeguards.png*](sole_safeguards.png).)
* For both data transfers to just the United States and all non-adequacy decision countries, the most common reason for the analyzed Android apps not complying with the GDPR is because they did not provide means to obtain a copy the safeguard(s). (See [*us_fail_reasons.png*](us_fail_reasons.png) and [*int_fail_reasons.png*](int_fail_reasons.png).)