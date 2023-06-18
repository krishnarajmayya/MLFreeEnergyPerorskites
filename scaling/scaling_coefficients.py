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
    
    scaled_standard_features = pd.read_csv('scaled_standard_features.csv')
    scaled_minmax_features = pd.read_csv('scaled_minmax_features.csv')

    column_to_extract = data['Name']
    name_df = pd.DataFrame(column_to_extract, columns=['Name'])

    # Extract the features (X) and target variable (Y)
    X = data.drop(columns=["Name"])

    # Standard Scaling
    scaler_standard = StandardScaler()
    scaled_standard = pd.DataFrame(scaler_standard.fit_transform(X), columns=X.columns)

    # Save StandardScaler object
    with open("standard_"+name_string+"_scaler.pkl", "wb") as file:
        pickle.dump(scaler_standard, file)

    # Min-Max Scaling
    scaler_minmax = MinMaxScaler()
    scaled_minmax = pd.DataFrame(scaler_minmax.fit_transform(X), columns=X.columns)

    # Save MinMaxScaler object
    with open("minmax_"+name_string+"_scaler.pkl", "wb") as file:
        pickle.dump(scaler_minmax, file)

    scaled_standard_df = pd.concat([scaled_standard_features, scaled_standard], axis=1)
    scaled_minmax_df = pd.concat([scaled_minmax_features, scaled_minmax], axis=1)

    scaled_standard_df.to_csv(f"scaled_standard_{name_string}.csv", index=False)
    scaled_minmax_df.to_csv(f"scaled_minmax_{name_string}.csv", index=False)



scale_and_save_features('Coeff_A.csv', 'Coeff_A')
scale_and_save_features('Coeff_B.csv', 'Coeff_B')
scale_and_save_features('Coeff_C.csv', 'Coeff_C')
scale_and_save_features('Coeff_D.csv', 'Coeff_D')
