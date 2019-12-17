#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 13:32:14 2019

@author: ortutay
"""

import pandas as pd 
import numpy as np

link = 'http://bit.ly/uforeports'
ufo = pd.read_csv(link)

# We split 60-20-20% tran-validation-test sets

train, validate, test = np.split(ufo.sample(frac=1), 
                                 [int(.6*len(ufo)),int(.8*len(ufo))])


a = pd.DataFrame({'col1': np.arange(1, 21),'col2': np.arange(21,41)})

train, validate, test = np.split(a.sample(frac=1), [int(.8 * len(a)), int(.9 * len(a))])