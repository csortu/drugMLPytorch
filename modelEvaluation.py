#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:54:40 2019

@author: ortutay
"""

import os
import pandas as pd 
import numpy as np
import torch
import torch.nn as nn

#Source: https://www.tutorialspoint.com/pytorch/pytorch_implementing_first_neural_network.htm

drug_wd = '/home/ortutay/Dropbox/Misc/HiDucator/DataScienceAcademy/Courses/Advanced_Python_for_datascience/AdvancedPythonPractice/data'
os.chdir(drug_wd)

drug_preprocessed = pd.read_csv("drug_consumption_preprocessed.csv",
                                index_col = 0)


train, validate, test = np.split(drug_preprocessed.sample(frac=1), 
                                 [int(.8 * len(drug_preprocessed)),
                                  int(.9 * len(drug_preprocessed))])


# Create a model
n_in, n_h, n_out, batch_size = 14, 56, 1, 50

model = nn.Sequential(nn.Linear(n_in, n_h),
   nn.ReLU(),
#   nn.Dropout(0.2),
   nn.Linear(n_h, n_h),
   nn.Linear(n_h, n_out),
   nn.Sigmoid())

# Load the model

model.load_state_dict(torch.load("simpleDrugBinaryClassifierSoftDrugs.bin"))


input_columns = ['age', 'sex', 'edu', 'neuroticism', 'extraversion', 'openness',
                 'agreeableness', 'conscientiousness', 'impulsiveness',
                 'sensationseeking', 'Alcohol', 'Caff', 'Choc', 'Nicotine']

#target_columns = ['hgtarget','sdtarget', 'hdtarget']

target_columns = 'sdtarget'

validate_input_tensor = torch.from_numpy(validate[input_columns].values)
validate_output_tensor = torch.from_numpy(validate[target_columns].values)

validate_pred = model(validate_input_tensor.float())

#validation = pd.DataFrame({'original': validate[target_columns].values,
#                           'prediction': np.log(validate_pred.detach().numpy()[:,0])})

validation = pd.DataFrame({'original': validate[target_columns].values,
                           'prediction': validate_pred.detach().numpy()[:,0]})


# Some binary classification metrics
    
pred = validation.prediction >= 0.5
accuracy = pred.eq(validation.original).sum() / validation.original.size

accuracy_df = pd.DataFrame(columns = ['threshold','accuracy'])

for i in range(1,100):
    thres = i/100
    pred = validation.prediction >= thres
    accuracy = pred.eq(validation.original).sum() / validation.original.size
    accuracy_df = accuracy_df.append({'threshold':thres,
                                      'accuracy':accuracy}, ignore_index=True)
    print("Threshold: %f\tAccuracy:%f" % (thres,accuracy))

accuracy_df.accuracy.plot.line()
    
