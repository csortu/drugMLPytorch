#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 12:58:21 2019

@author: ortutay
@source: https://www.tutorialspoint.com/python_pandas/python_pandas_descriptive_statistics.htm
"""
import os
import pandas as pd 
from pandas.plotting import scatter_matrix

drug_wd = '/home/ortutay/Dropbox/Misc/HiDucator/DataScienceAcademy/Courses/Advanced_Python_for_datascience/AdvancedPythonPractice/data'
os.chdir(drug_wd)

# Read in data from CSV file

drug_original = pd.read_csv("drug_consumption_original.csv",
                            index_col = 0) 

# Get general information about the data

drug_original.info()

drug_original.head()

drug_original.sum()

drug_original.describe()

drug_original.describe(include = ['object'])

drug_original.columns

# Descriptive statistics of categorical columns

drug_original['country']
drug_original['country'].value_counts()
drug_original['country'].value_counts().plot.bar()


drug_original.groupby(['country','age']).size()
drug_original.groupby(['country','age']).size().unstack().fillna(0)
pd.crosstab(drug_original.country,drug_original.age)
pd.crosstab(drug_original.country,drug_original.age, margins=True, margins_name="Total")


drug_original.groupby(['country','sex']).size()
drug_original.groupby(['country','sex']).size().plot.bar()

pd.crosstab(drug_original.country,[drug_original.age,drug_original.sex], margins=True, margins_name="Total")

pd.crosstab(drug_original.country,[drug_original.age,drug_original.sex]).plot(kind='bar',
           stacked=False, color=['red','blue'], grid=False)

# Descriptive statistics on numeric columns

drug_original['neuroticism'].plot.hist()
drug_original['extraversion'].plot.hist()
drug_original['agreeableness'].plot.hist()
drug_original['openness'].plot.hist()
drug_original['conscientiousness'].plot.hist()

drug_original['neuroticism'].mean()
drug_original['neuroticism'].median()
drug_original['neuroticism'].std()
drug_original[['neuroticism','extraversion']].boxplot()

drug_original.iloc[:,6:12]
drug_original.iloc[:,6:12].boxplot()

drug_original.iloc[:,6:11].plot.hist(alpha = 0.4)
drug_original.iloc[:,6:11].plot.hist(stacked = True)
drug_original.iloc[:,6:12].hist()

# Some correlation analysis
drug_original[['sex','neuroticism','extraversion']].boxplot(by='sex')


drug_original.plot.scatter(x = 'neuroticism',
                           y = 'extraversion')

drug_original.plot.scatter(x = 'neuroticism',
                           y = 'agreeableness',
                           c = 'extraversion')

drug_original.plot.hexbin(x = 'neuroticism',
                          y = 'extraversion',
                          gridsize = 25)

scatter_matrix(drug_original.iloc[:,6:11],diagonal='kde')
