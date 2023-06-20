#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 18:49:41 2023

@author: krishnarajmayya
"""

import pandas as pd

# Read the CSV file as a DataFrame
df = pd.read_csv('test.csv')

# List of columns to drop
# =============================================================================
# columns_to_drop = [
#     "A_Rc","A_Ra","A_M","A_MP","A_MV","A_MendeleevNo","A_Hf","A_Hv",
#     "B_Rc","B_Rvdw","B_M","B_BP","B_MendeleevNo","B_Hv",
#     "X_Rc","X_Rvdw","X_M","X_BP","X_MP","X_MendeleevNo","X_Hf",
#     "X_Hv","X_G","X_B","X_CvM","X_ChiP", "OF", 'A_site', 
#     'B_site', 'X_site', 'Spacegroup', 'Ehull','BulkModulus', 'Energy',
#     's_A','s_B','s_X','ZPE', 'Coeff_A','Coeff_B', 'Coeff_C', 'Coeff_D'
#     ]
# =============================================================================

columns_to_drop = [
    'A_BP', 'A_Hf', 'A_Hv', 'A_M', 'A_MV', 'A_MendeleevNo', 'A_Ra', 
    'A_Rc', 'B_BP', 'B_Hv', 'B_M', 'X_BP', 'X_B', 'X_ChiA', 'X_CvM', 
    'X_Hf', 'X_Hv', 'X_MP', 'X_M', 'X_MendeleevNo', 'X_Ra', 'X_Rc',
    'A_site', 'B_site', 'X_site', 'Spacegroup', 'Ehull','BulkModulus', 
    'Energy','s_A','s_B','s_X','ZPE','Coeff_A','Coeff_B', 'Coeff_C', 'Coeff_D'
    ]

# Drop the specified columns
df_dropped = df.drop(columns=columns_to_drop)

# Write the modified DataFrame to a new CSV file
df_dropped.to_csv('test_features.csv', index=False)

# Load data from CSV file
data = pd.read_csv('test.csv')

# Extract the 'Coeff_A' column into a new DataFrame
Coeff_A = data[['Name', 'Coeff_A']].copy()

# Write the modified DataFrame to a new CSV file
Coeff_A.to_csv('test_Coeff_A.csv', index=False)

# Load data from CSV file
data = pd.read_csv('test.csv')

# Extract the 'Coeff_A' column into a new DataFrame
Coeff_B = data[['Name', 'Coeff_B']].copy()

# Write the modified DataFrame to a new CSV file
Coeff_B.to_csv('test_Coeff_B.csv', index=False)

# Load data from CSV file
data = pd.read_csv('test.csv')

# Extract the 'Coeff_A' column into a new DataFrame
Coeff_C = data[['Name', 'Coeff_C']].copy()

# Write the modified DataFrame to a new CSV file
Coeff_C.to_csv('test_Coeff_C.csv', index=False)

# Load data from CSV file
data = pd.read_csv('test.csv')

# Extract the 'Coeff_A' column into a new DataFrame
Coeff_D = data[['Name', 'Coeff_D']].copy()

# Write the modified DataFrame to a new CSV file
Coeff_D.to_csv('test_Coeff_D.csv', index=False)