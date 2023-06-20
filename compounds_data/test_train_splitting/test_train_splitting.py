#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:34:13 2023

@author: krishnarajmayya
"""

import pandas as pd
from sklearn.model_selection import train_test_split

# Read the CSV file into a dataframe
df = pd.read_csv('Combined_All.csv')

# Splitting into training and testing sets
df_train, df_test = train_test_split(df, train_size=0.8, 
                                     test_size=0.2, 
                                     random_state=50)

# Save train and test data as CSV files
df_train.to_csv('train.csv', index=False)
df_test.to_csv('test.csv', index=False)

