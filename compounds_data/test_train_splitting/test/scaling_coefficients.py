#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 22:25:55 2023

@author: krishnarajmayya
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle

def scale_and_save_features(input_file, name_string):
    # Load data from CSV file
    data = pd.read_csv(input_file)
    
    scaled_standard_features = pd.read_csv('scaled_standard_features_test.csv')
    scaled_minmax_features = pd.read_csv('scaled_minmax_features_test.csv')

    column_to_extract = data['Name']
    name_df = pd.DataFrame(column_to_extract, columns=['Name'])

    # Extract the features (X) and target variable (Y)
    X = data.drop(columns=["Name"])

    # Standard Scaling
    # Load the scaling model from a pickle file
    with open("standard_"+name_string+"_scaler.pkl", 'rb') as file:
        scaler_standard = pickle.load(file)
    
    scaled_standard = pd.DataFrame(scaler_standard.transform(X), columns=X.columns)

    # Min-Max Scaling
    # Load the scaling model from a pickle file
    with open("minmax_"+name_string+"_scaler.pkl", 'rb') as file:
        scaler_minmax = pickle.load(file)
    scaled_minmax = pd.DataFrame(scaler_minmax.transform(X), columns=X.columns)

    scaled_standard_df = pd.concat([scaled_standard_features, scaled_standard], axis=1)
    scaled_minmax_df = pd.concat([scaled_minmax_features, scaled_minmax], axis=1)

    scaled_standard_df.to_csv(f"scaled_standard_{name_string}_test.csv", index=False)
    scaled_minmax_df.to_csv(f"scaled_minmax_{name_string}_test.csv", index=False)



scale_and_save_features('test_Coeff_A.csv', 'Coeff_A')
scale_and_save_features('test_Coeff_B.csv', 'Coeff_B')
scale_and_save_features('test_Coeff_C.csv', 'Coeff_C')
scale_and_save_features('test_Coeff_D.csv', 'Coeff_D')
