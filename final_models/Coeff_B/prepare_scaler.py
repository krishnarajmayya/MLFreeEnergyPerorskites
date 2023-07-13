#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 20:48:45 2023

@author: krishnarajmayya
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

# Load data from CSV file
data = pd.read_csv('Combined_All.csv')

column_to_extract = data['Name']
needed_feature_names = ['X_EA', 'mean_A2B', 'X_Z', 'X_Rvdw', 'X_IEII', 'mean_X2X',
                        'A_Rvdw', 'mean_A2X', 'A_IEI', 'E_coh', 'A_ChiA', 'B_Hf', 'X_G',
                        'A_EA', 'std_A2X', 'A_ChiP', 'B_MP', 'std_B2X', 'OF', 'A_MP',
                        'B_Z', 'X_Kappa', 'A_Kappa', 'B_Kappa', 'B_Ra', 'A_Z', 'B_Rho',
                        'X_MV', 'A_CvM', 'A_G', 'B_EA', 'B_CvM', 'TF', 'std_X2X', 'A_B',
                        'std_A2B', 'B_ChiP', 'X_IEI', 'B_MV', 'B_IEI']
needed_features = data[needed_feature_names]  
name_df = pd.DataFrame(column_to_extract, columns=['Name'])
input_df = pd.DataFrame(needed_features, columns=needed_feature_names)


# Min-Max Scaling
scaler_std = StandardScaler()
scaled_data_std = pd.DataFrame(scaler_std.fit_transform(input_df),
                                  columns=input_df.columns)

# Save MinMaxScaler object
with open("std_scaler.pkl", "wb") as file:
    pickle.dump(scaler_std, file)
    
scaled_std_data = pd.concat([name_df, scaled_data_std], axis=1)

scaled_std_data.to_csv('scaled_train_features.csv',index=False)

input_template = pd.concat([name_df, input_df], axis=1)

input_template.to_csv('input.csv',index=False)