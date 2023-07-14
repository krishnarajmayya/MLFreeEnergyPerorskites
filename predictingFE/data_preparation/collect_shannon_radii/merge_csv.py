#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:38:07 2023

@author: krishnarajmayya
"""

import pandas as pd

def merge(f1,f2,key,out):
    # Read the first CSV file into a data frame
    df1 = pd.read_csv(f1)

    # Read the second CSV file into another data frame
    df2 = pd.read_csv(f2)

    # Perform an outer merge
    merged_df = pd.merge(df1, df2, on=key, how='outer')

    # Print the merged data frame
    merged_df.to_csv(out, index=False)
