#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 22:00:48 2023

@author: krishnarajmayya
"""
import pandas as pd
import numpy as np
import pickle

# Load data from CSV file
data = pd.read_csv('input.csv')

column_to_extract = data['Name']  
output = pd.DataFrame(column_to_extract, columns=['Name'])

# Extract the features (X) and target variable (Y)
X = data.drop(columns=["Name"])
    
# Load the scaling model from a pickle file
with open('std_scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

scaled_features = pd.DataFrame(scaler.transform(X), columns=X.columns)
scaled_features.fillna(0, inplace= True)

# Load the GPR model from pickle file
with open('Coeff_B_GPR.pkl', 'rb') as f:
    model = pickle.load(f)
# Make predictions on the data
y_pred = model.predict(scaled_features)

# Add predictions to the DataFrame
output['prediction'] = y_pred

with open('standard_Coeff_B_scaler.pkl', 'rb') as file:
    scaler_model = pickle.load(file)

scaled_column = output[['prediction']]
unscaled_column = scaler_model.inverse_transform(scaled_column)

output['unscaled_prediction'] = unscaled_column

output.to_csv('output.csv',index=False)