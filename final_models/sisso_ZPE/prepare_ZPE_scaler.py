#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 01:10:36 2023

@author: krishnarajmayya
"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

# Load data from CSV file
data = pd.read_csv('ZPE.csv')

column_to_extract = data['Name']
name_df = pd.DataFrame(column_to_extract, columns=['Name'])

# Extract the features (X) and target variable (Y)
X = data.drop(columns=["Name"])

# Min-Max Scaling
scaler_ZPE = MinMaxScaler()
scaled_ZPE = pd.DataFrame(scaler_ZPE.fit_transform(X), columns=X.columns)

# Save MinMaxScaler object
with open("minmax_ZPE_scaler.pkl", "wb") as file:
    pickle.dump(scaler_ZPE, file)

scaled_minmax_ZPE = pd.concat([name_df, scaled_ZPE], axis=1)

scaled_minmax_ZPE.to_csv("scaled_ZPE.csv", index=False)