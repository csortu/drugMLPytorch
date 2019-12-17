#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 09:48:53 2019

@author: ortutay
"""

import os
import pandas as pd 

drug_wd = '/home/ortutay/Dropbox/Misc/HiDucator/DataScienceAcademy/Courses/Advanced_Python_for_datascience/AdvancedPythonPractice/data'
os.chdir(drug_wd)

drug_transformed = pd.read_csv("drug_consumption_transformed.csv",
                            index_col = 0)
#drug_original = pd.read_csv("drug_consumption_original.csv",
#                            index_col = 0) 

# We won't use the id column, as it is just replacement for names
# Country and ethnicity are biased by the sampling (UK) we drop them too
# Additionally the distribution of country and ethnicity is very uneven


drug_transformed['country'].value_counts().plot.bar()
drug_transformed['ethnicity'].value_counts().plot.bar()

# Let's drop all these columns

drug_preprocessed = drug_transformed.drop(columns =['id','country',
                                                     'ethnicity'])

# There are 4 kinds of drugs in the study:
#ND: Non-drug: 'Alcohol','Caff','Choc','Nicotine'    and Semeron which is a non-existing drug
#SD: Soft drug: 'Amyl','Benzos','VSA'
#HD: Hard drug: 'Amphet','Coke','Crack','Ecstasy','Heroin','Ketamine'
#HG: Hallucinogen: 'Cannabis','Legalh','LSD','Meth','Mushrooms'

# Non-drugs will be used as input data
# We will build a model predicting the probability of hallucinogen, soft-drug
# and hard-drug usage 
# Therefore we will create HG, SD, and HD columns which will be our targets
# The original data, drug usage is described with the following categories:
# CL0 Never Used
# CL1 Used over a Decade Ago
# CL2 Used in Last Decade
# CL3 Used in Last Year
# CL4 Used in Last Month
# CL5 Used in Last Week 
# CL6 Used in Last Day
# This will be simplified as someone who used a drug last year or later 
# is a user 1, others are non-users 0

hgdrugs = ['Cannabis','Legalh','LSD','Meth','Mushrooms']
sdrugs =['Amyl','Benzos','VSA']
hdrugs = ['Amphet','Coke','Crack','Ecstasy','Heroin','Ketamine']

drugdf = drug_transformed[hdrugs]
drugdf['hdval'] = drug_transformed[hdrugs].max(axis = 1)
drugdf[sdrugs] = drug_transformed[sdrugs]
drugdf['sdval'] = drug_transformed[sdrugs].max(axis = 1)
drugdf[hgdrugs] = drug_transformed[hgdrugs]
drugdf['hgval'] = drug_transformed[hgdrugs].max(axis = 1)

drugdf['hdtarget'] = 0
drugdf.hdtarget[drugdf['hdval']>2] = 1

drugdf['sdtarget'] = 0
drugdf.sdtarget[drugdf['sdval']>2] = 1

drugdf['hgtarget'] = 0
drugdf.hgtarget[drugdf['hgval']>2] = 1

d = drugdf[['hdval','hdtarget','sdval','sdtarget','hgval','hgtarget']]

drug_preprocessed[['hgtarget','sdtarget','hdtarget']] = drugdf[['hgtarget','sdtarget','hdtarget']]

# Now that we have the targets, we have to drop the original drug columns

drug_preprocessed = drug_preprocessed.drop(columns = hgdrugs + sdrugs + hdrugs)

 # Plus we have to standardize the non-drug substance columns
 
for colname in ['Alcohol','Caff','Choc','Nicotine']:
    newcol = drug_preprocessed[colname]
    colmean = newcol.mean()
    colsd = newcol.std()
    newcol = (newcol - colmean)/colsd
    drug_preprocessed[colname] = newcol

# Semeron is a non-existing drug name used for finding liars in the dataset
# Let's drop those answers yes to Semeron

drug_preprocessed['Semeron'].value_counts()
drug_preprocessed['Semeron']!=0
drug_preprocessed[drug_preprocessed['Semeron']!=0]
drug_preprocessed[drug_preprocessed['Semeron']!=0].index
drug_preprocessed = drug_preprocessed.drop(drug_preprocessed[drug_preprocessed['Semeron']!=0].index)

#drug_preprocessed = drug_preprocessed[drug_preprocessed['Semeron']==0]

# Now drom the Semeron column and preprocessing is done
drug_preprocessed = drug_preprocessed.drop(columns = ['Semeron'])

drug_preprocessed.to_csv("drug_consumption_preprocessed.csv")
