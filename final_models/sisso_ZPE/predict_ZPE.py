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
name_df = pd.DataFrame(column_to_extract, columns=['Name'])

# Extract the features (X) and target variable (Y)
X = data.drop(columns=["Name"])
    
# Load the scaling model from a pickle file
with open('minmax_scaler.pkl', 'rb') as file:
    scaler_minmax = pickle.load(file)

scaled_features_minmax = pd.DataFrame(scaler_minmax.transform(X), columns=X.columns)

in_data = pd.concat([name_df, scaled_features_minmax], axis=1)

coefficients = np.array([-0.3297018893E+00, 0.1752629704E+00, 0.5786606463E-01, -0.1261624918E+00,
                -0.7020834723E-03, 0.1735423341E+01, 0.3905682439E-02])

in_data['desc1'] = np.sqrt((in_data['B_Ra'] + in_data['mean_A2X'])) * (np.exp(in_data['X_G']) + np.exp(-in_data['std_A2X']))
in_data['desc2'] = np.abs(((in_data['B_Rc'] + in_data['A_Rvdw']) - in_data['mean_A2X']) - ((in_data['B_Rvdw'] + in_data['std_A2X']) / np.exp(in_data['X_EA'])))
in_data['desc3'] = ((in_data['A_EA'] * in_data['X_EA']) / (in_data['B_Rvdw'] - in_data['mean_A2X'])) * (np.abs(in_data['B_Rc'] - in_data['mean_A2X']) - np.abs(in_data['mean_A2B'] - in_data['mean_X2X']))
in_data['desc4'] = np.abs(np.abs((in_data['A_Rvdw'] + in_data['X_Rvdw']) - (in_data['B_Rc'] + in_data['mean_X2X'])) - np.abs((in_data['X_Rvdw'] + in_data['std_A2X']) - (in_data['mean_A2B'] + in_data['mean_X2X'])))
in_data['desc5'] = ((in_data['B_Rc'] * in_data['B_CvM']) / (in_data['B_Rc'] - in_data['mean_A2X'])) / (np.abs(in_data['A_Rvdw'] - in_data['mean_X2X']) - np.abs(in_data['std_A2B'] - in_data['mean_A2B']))
in_data['desc6'] = ((in_data['A_ChiA'] ** 2 * (in_data['A_MP'] * in_data['B_MP'])) * ((in_data['std_B2X'] - in_data['mean_A2B']) - np.abs(in_data['B_Ra'] - in_data['std_A2B'])))
in_data['desc7'] = (np.abs(in_data['A_Rvdw'] - in_data['X_Rvdw']) - np.abs(in_data['B_Ra'] - in_data['X_Rvdw'])) / ((in_data['B_Rvdw'] - in_data['std_A2B']) - np.abs(in_data['std_B2X'] - in_data['mean_A2B']))

# Perform operations on a column and save it as a new column
zpe = []
for index, row in in_data.iterrows():
    result = np.dot(coefficients, row[['desc1', 'desc2', 'desc3', 'desc4', 'desc5', 'desc6', 'desc7']]) + 0.1491558366E+01
    zpe.append(result)

in_data['ZPE'] = zpe

output_columns = in_data[['Name','desc1', 'desc2', 'desc3', 'desc4', 'desc5', 
                          'desc6', 'desc7','ZPE']]  
output = pd.DataFrame(output_columns, 
                      columns=['Name','desc1', 'desc2', 'desc3', 'desc4', 'desc5', 
                               'desc6', 'desc7','ZPE'])

with open('minmax_ZPE_scaler.pkl', 'rb') as file:
    scaler_model = pickle.load(file)

scaled_column = output[['ZPE']]
unscaled_column = scaler_model.inverse_transform(scaled_column)

output['unscaled_ZPE'] = unscaled_column

output.to_csv('output.csv',index=False)