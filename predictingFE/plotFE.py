#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 19:59:44 2023

@author: krishnarajmayya
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Read the CSV file into a DataFrame
data = pd.read_csv('Combined_All_out.csv')

# Specify the column names for the coefficients and group
coefficient_columns = ['Coeff_A', 'Coeff_B', 'Coeff_C', 'Coeff_D']
name_column = 'Name'  # Assuming 'Name' is the column name for grouping
group_column = 'Spacegroup'  # Assuming 'SpaceGroup' is the column name

# Get unique name values
name_values = data[name_column].unique()

# Generate x-values for the plot
x = np.linspace(0, 1000, 100)

# Create a folder to save the plots
os.makedirs('FE_plots', exist_ok=True)

# Loop over name values and create separate plots
for name_value in name_values:
    # Create a new figure for each name value
    fig, ax = plt.subplots(figsize=(6, 6))

    # Filter data for the current name value
    group_data = data[data[name_column] == name_value]

    # Create an empty list for legend labels
    legend_labels = []

    # Plot each polynomial for the current name value
    for _, row in group_data.iterrows():
        coefficients = row[coefficient_columns]
        space_group = row[group_column]
        y = np.polyval(coefficients, x)
        ax.plot(x, y)
        legend_labels.append(space_group)

    # Set labels and title for the plot
    ax.set_xlabel('Temperature')
    ax.set_ylabel('$F_\mathrm{H}$')
    ax.set_title(f'Name: {name_value}')

    # Add a legend based on space group
    ax.legend(legend_labels)

    # Save the plot in the name_plots folder
    plot_filename = f'FE_plots/{name_value}.jpeg'
    plt.savefig(plot_filename, format='jpeg', dpi=720)

    # Close the figure to release memory
    plt.close(fig)
