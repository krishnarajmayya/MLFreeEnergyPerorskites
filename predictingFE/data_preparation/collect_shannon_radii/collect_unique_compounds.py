#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 17:43:31 2023

@author: krishnarajmayya
"""
import pandas as pd

def find_unique(input_path,output_path):
    # Read the input CSV file
    df = pd.read_csv(input_path)

    # Extract four columns into a new DataFrame
    df_new = df[['Name', 'A_site', 'B_site', 'X_site']]

    # Keep only the unique rows in the new DataFrame
    df_unique = df_new.drop_duplicates()

    # Save the unique rows to a new CSV file
    df_unique.to_csv(output_path, index=False)
