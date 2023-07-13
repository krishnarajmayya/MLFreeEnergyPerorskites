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
needed_feature_names = ['mean_A2B', 'X_EA', 'X_Z', 'X_IEII', 'X_Rvdw', 'mean_X2X',
                        'A_Rvdw', 'mean_A2X', 'A_IEI', 'E_coh', 'A_ChiA', 'std_A2X',
                        'A_ChiP', 'A_EA', 'B_Hf', 'std_B2X', 'X_G', 'B_MP', 'X_Kappa',
                        'A_MP', 'B_Kappa', 'B_Z', 'OF', 'A_Kappa', 'A_Z', 'B_Ra', 'B_Rho',
                        'A_CvM', 'X_MV', 'A_G', 'B_EA', 'A_B', 'std_X2X', 'B_CvM',
                        'B_ChiP', 'TF', 'std_A2B', 'X_IEI', 'B_IEI', 'B_MV']
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