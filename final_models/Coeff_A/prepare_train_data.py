#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 01:10:36 2023

@author: krishnarajmayya
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle

data = pd.read_csv('Coeff_A.csv')

scaled_standard_features = pd.read_csv('scaled_train_features.csv')

# Extract the features (X) and target variable (Y)
X = data.drop(columns=["Name"])
    
# Load the scaling model from a pickle file
with open('standard_Coeff_A_scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

scaled_target = pd.DataFrame(scaler.transform(X), columns=X.columns)

in_data = pd.concat([scaled_standard_features, scaled_target], axis=1)

in_data.to_csv('scaled_train_data.csv',index=False)

