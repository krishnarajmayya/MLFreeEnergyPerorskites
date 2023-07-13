#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 20:48:45 2023

@author: krishnarajmayya
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

# Load data from CSV file
data = pd.read_csv('Combined_All.csv')

column_to_extract = data['Name']
needed_features = data[['B_Ra','B_Rc','B_Rvdw','A_Rvdw','X_Rvdw','mean_A2X','mean_A2B',
                       'mean_X2X','std_A2X','std_A2B','std_B2X','X_G','X_EA','A_EA',
                       'B_CvM','A_ChiA','A_MP','B_MP']]  
name_df = pd.DataFrame(column_to_extract, columns=['Name'])
input_df = pd.DataFrame(needed_features, columns=['B_Ra','B_Rc','B_Rvdw','A_Rvdw','X_Rvdw',
                                                  'mean_A2X','mean_A2B','mean_X2X',
                                                  'std_A2X','std_A2B','std_B2X',
                                                  'X_G','X_EA','A_EA','B_CvM',
                                                  'A_ChiA','A_MP','B_MP'])


# Min-Max Scaling
scaler_minmax = MinMaxScaler()
scaled_data_minmax = pd.DataFrame(scaler_minmax.fit_transform(input_df),
                                  columns=input_df.columns)

# Save MinMaxScaler object
with open("minmax_scaler.pkl", "wb") as file:
    pickle.dump(scaler_minmax, file)
    
scaled_minmax_data = pd.concat([name_df, scaled_data_minmax], axis=1)

scaled_minmax_data.to_csv('scaled_train_data.csv',index=False)

input_template = pd.concat([name_df, input_df], axis=1)

input_template.to_csv('input.csv',index=False)