#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 12:17:18 2019

@author: ortutay
"""

import os
import pandas as pd 
import matplotlib.pyplot as plt

drug_wd = '/home/ortutay/Dropbox/Misc/HiDucator/DataScienceAcademy/Courses/Advanced_Python_for_datascience/AdvancedPythonPractice/data'
os.chdir(drug_wd)

# Read in data from CSV file

drug_original = pd.read_csv("drug_consumption_original.csv",
                            index_col = 0) 

# Convert category to numeric
# pd.Categorical() == as.factor() in R

a = pd.Categorical(drug_original['age']).codes

print(pd.Categorical(drug_original['age'])[0:10])
print(a[0:10])

drug_original['age'].value_counts().plot.bar()
plt.hist(a)

# center around 0 and spread to 1 standard deviation: technically this is standardization

b = (a - a.mean())/a.std()

plt.hist(b)

b.mean()
b.std()
pd.Series(b).describe()

# Lets convert all categorial data to numeric

categories = ['age','sex','edu','country','ethnicity']
drugs = ['Alcohol', 'Amphet', 'Amyl',
         'Benzos', 'Caff', 'Cannabis', 'Choc', 'Coke', 'Crack', 'Ecstasy',
         'Heroin', 'Ketamine', 'Legalh', 'LSD', 'Meth', 'Mushrooms', 
         'Nicotine','Semeron', 'VSA']
newdf = pd.DataFrame()

# Let's do standardization so that each vectors are centered to zero and that it's standard deviation is 1
# This removes scalin bias of the different variables when we use the data

c = drug_original['Alcohol'].str.extract('(\d+)').astype(int)

for colname in drug_original.columns:
    if colname == 'id':
        newdf['id'] = drug_original['id']
        continue
    newcol = drug_original[colname]
    if colname in categories:
        print('Converting ' + colname)
        newcol = pd.Categorical(drug_original[colname]).codes
    if colname in drugs:
        print('converting ' + colname + ' drug')
        newcol = drug_original[colname].str.extract('(\d+)').astype(int)
        newdf[colname] = newcol
        continue
    colmean = newcol.mean()
    colsd = newcol.std()
    newcol = (newcol - colmean)/colsd
    newdf[colname] = newcol

# Let's check if that has worked
        
for colname in newdf.columns:
    if colname == 'id':
        continue
#    print(colname)
#    print(newdf[colname].mean())
#    print("%s: Mean: %s, standard deviation: %s" % (colname,newdf[colname].mean(),newdf[colname].std()))
    print("%s: Mean: %4.2f, standard deviation: %4.2f" % (colname,newdf[colname].mean(),newdf[colname].std()))


# Check visually

drug_original.iloc[:,6:11].plot.hist(alpha = 0.4)
newdf.iloc[:,6:11].plot.hist(alpha = 0.4)

drug_original.iloc[:,6:12].boxplot()
newdf.iloc[:,6:12].boxplot()

newdf.iloc[:,1:].boxplot()

# Whats up wit Semeron?

drug_original['Semeron'].value_counts()
newdf['Semeron'].value_counts()
drug_original['Semeron'].value_counts().plot.bar()

# Well, let's save the transformed data frame

newdf.to_csv("drug_consumption_transformed.csv")
