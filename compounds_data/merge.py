#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:38:07 2023

@author: krishnarajmayya
"""

import pandas as pd

# Read the first CSV file into a data frame
df1 = pd.read_csv('Material_prop_all.csv')

# Read the second CSV file into another data frame
df2 = pd.read_csv('fit_coefficients.csv')

# Perform an outer merge
merged_df = pd.merge(df1, df2, on='Name', how='outer')

# Print the merged data frame
merged_df.to_csv('Combined_All.csv', index=False)