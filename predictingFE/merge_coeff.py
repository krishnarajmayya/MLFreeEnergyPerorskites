#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:38:07 2023

@author: krishnarajmayya
"""

import pandas as pd

def merge_coeff(input_file,coeff_file,output_file):

    # Read the first CSV file into a data frame
    df1 = pd.read_csv(input_file)

    # Read the second CSV file into another data frame
    df2 = pd.read_csv(coeff_file)
    
    df2 = df2.drop(['Name'],axis=1)

    # Perform an outer merge
    merged_df = pd.merge(df1, df2, on='material_id', how='outer')

    # Print the merged data frame
    merged_df.to_csv(output_file, index=False)
