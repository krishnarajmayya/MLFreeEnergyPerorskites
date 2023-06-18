#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 18:45:24 2023

@author: krishnarajmayya
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle

# Load data from CSV file
data = pd.read_csv('non_corelated_features.csv')

column_to_extract = data['Name']  
name_df = pd.DataFrame(column_to_extract, columns=['Name'])

# Extract the features (X) and target variable (Y)
X = data.drop(columns=["Name"])

# Standard Scaling
scaler_standard = StandardScaler()
scaled_features_standard = pd.DataFrame(scaler_standard.fit_transform(X), columns=X.columns)


# Save StandardScaler object
with open("standard_feature_scaler.pkl", "wb") as file:
    pickle.dump(scaler_standard, file)


# Min-Max Scaling
scaler_minmax = MinMaxScaler()
scaled_features_minmax = pd.DataFrame(scaler_minmax.fit_transform(X), columns=X.columns)

# Save MinMaxScaler object
with open("minmax_feature_scaler.pkl", "wb") as file:
    pickle.dump(scaler_minmax, file)
    
scaled_standard_features = pd.concat([name_df, scaled_features_standard], axis=1)
scaled_minmax_features = pd.concat([name_df, scaled_features_minmax], axis=1)

scaled_standard_features.to_csv('scaled_standard_features.csv',index=False)
scaled_minmax_features.to_csv('scaled_minmax_features.csv',index=False)