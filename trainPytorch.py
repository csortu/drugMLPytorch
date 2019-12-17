#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:15:34 2019

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

# Split original dataset to 60-20-20% tran-validation-test sets

train, validate, test = np.split(drug_preprocessed.sample(frac=1), 
                                 [int(.8 * len(drug_preprocessed)),
                                  int(.9 * len(drug_preprocessed))])

drug_preprocessed = train

input_columns = ['age', 'sex', 'edu', 'neuroticism', 'extraversion', 'openness',
                 'agreeableness', 'conscientiousness', 'impulsiveness',
                 'sensationseeking', 'Alcohol', 'Caff', 'Choc', 'Nicotine']

#target_columns = ['hgtarget','sdtarget', 'hdtarget']

target_columns = 'sdtarget'


drug_preprocessed[input_columns].values

# Defining input size, hidden layer size, output size and batch size respectively
n_in, n_h, n_out, batch_size = 14, 56, 1, 50

#x = torch.randn(batch_size, n_in)

input_tensor = torch.from_numpy(drug_preprocessed[input_columns].values)
output_tensor = torch.BoolTensor(drug_preprocessed[target_columns].values)

output_tensor = output_tensor.view(-1,1)

# Create a model
model = nn.Sequential(nn.Linear(n_in, n_h),
   nn.ReLU(),
#   nn.Dropout(0.2),
   nn.Linear(n_h, n_h),
   nn.Linear(n_h, n_out),
   nn.Sigmoid())

#Construct the loss function
#criterion = torch.nn.MSELoss()

criterion = torch.nn.BCELoss()

# Construct the optimizer (Stochastic Gradient Descent in this case)
optimizer = torch.optim.SGD(model.parameters(), lr = 0.05)

# Gradient Descent training
for epoch in range(10000):
   # Forward pass: Compute predicted y by passing x to the model
   y_pred = model(input_tensor.float())

   # Compute and print loss
   loss = criterion(y_pred, output_tensor.float())
   print('epoch: ', epoch,' loss: ', loss.item())

   # Zero gradients, perform a backward pass, and update the weights.
   optimizer.zero_grad()

   # perform a backward pass (backpropagation)
   loss.backward()
   
   # Stop optimizatio if loss is below 0.1
   
   if loss.item() < 0.1:
       break

   # Update the parameters
   optimizer.step()
   
validate_input_tensor = torch.from_numpy(validate[input_columns].values)
validate_output_tensor = torch.from_numpy(validate[target_columns].values)

validate_pred = model(validate_input_tensor.float())

#validation = pd.DataFrame({'original': validate[target_columns].values,
#                           'prediction': np.log(validate_pred.detach().numpy()[:,0])})

validation = pd.DataFrame({'original': validate[target_columns].values,
                           'prediction': validate_pred.detach().numpy()[:,0]})

    
validation.boxplot('prediction',by = 'original')

model.state_dict()

torch.save(model.state_dict(), "simpleDrugBinaryClassifierSoftDrugs.bin")
