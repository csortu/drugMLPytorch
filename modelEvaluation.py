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
import matplotlib.pyplot as plt

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

ax = accuracy_df.accuracy.plot.line(title = "Model accuracy with different thresholds")
ax.set(xlabel="Threshold [%]", ylabel="Accuracy [%]")
ax.axvline(x=50, alpha = 0.6)

# More classification metrics
# See: https://en.wikipedia.org/wiki/Evaluation_of_binary_classifiers
# The basic metrics:

tp = (pred.eq(True) & validation.original.eq(True)).sum()
tn = (pred.eq(False) & validation.original.eq(False)).sum()
fp = (pred.eq(True) & validation.original.eq(False)).sum()
fn = (pred.eq(False) & validation.original.eq(True)).sum()

print("True positives: %i\nTrue negatives: %i\nFalse positives: %i\n False negatives %i" % (tp,tn,fp,fn))

# Compound metrics:

acc = (tp + tn) / (tp + tn + fp + fn).sum()
pre = tp / (tp + fp)
rec = tp / (tp + fn)
f1 = (2.0 * tp) / (2.0 * tp + fp + fn)

print("Accuracy: %2.2f\nPrecision: %2.2f\nRecall: %2.2f\nBalanced F-score: %2.2f" % (100*acc,100*pre,100*rec,100*f1))

metrics_df = pd.DataFrame(columns = ['tp',
                                     'tn',
                                     'fp',
                                     'fn',
                                     'acc',
                                     'sens',
                                     'spec',
                                     'pre',
                                     'rec',
                                     'f1'])

for i in range(1,100):
    thres = i/100
    pred = validation.prediction >= thres
    tp = (pred.eq(True) & validation.original.eq(True)).sum()
    tn = (pred.eq(False) & validation.original.eq(False)).sum()
    fp = (pred.eq(True) & validation.original.eq(False)).sum()
    fn = (pred.eq(False) & validation.original.eq(True)).sum()
    print("Threshold: %1.2f True positives: %i True negatives: %i False positives: %i False negatives %i" % (thres,tp,tn,fp,fn))
    acc = (tp + tn) / (tp + tn + fp + fn).sum()
    pre = tp / (tp + fp)
    rec = tp / (tp + fn)
    f1 = (2.0 * tp) / (2.0 * tp + fp + fn)
    sens = tp / (tp + fn)
    spec = tn / (tn + fp)
    
    metrics_df = metrics_df.append({'tp': tp,
                                    'tn': tn,
                                    'fp': fp,
                                    'fn': fn,
                                    'acc': 100*acc,
                                    'sens': 100*sens,
                                    'spec': 100*spec,
                                    'pre': 100*pre,
                                    'rec': 100*rec,
                                    'f1': 100*f1}, ignore_index=True)

    
ax = metrics_df.plot.line(title = "Model metrics with different thresholds")
ax.set(xlabel="Threshold [%]", ylabel="[%]")
ax.axvline(x=50, alpha = 0.6)

# Roc curve
# True positive rate (tpr) == sensitivity
# False positive rate (fpr) == fall-out

# See https://www.displayr.com/what-is-a-roc-curve-how-to-interpret-it/

roc_df = pd.DataFrame({'tpr': metrics_df.tp / (metrics_df.tp + metrics_df.fn),
                       'fpr': metrics_df.fp / (metrics_df.fp + metrics_df.tn)})

roc_df.plot.scatter(x = 'fpr',
                    y = 'tpr')

plt.plot( 'fpr', 'tpr', data=roc_df, linestyle='-', marker='o')

