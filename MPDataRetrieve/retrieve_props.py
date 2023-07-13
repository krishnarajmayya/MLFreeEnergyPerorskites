#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 19:01:17 2023

@author: krishnarajmayya
"""

import subprocess
import pandas as pd
from pymatgen.core.structure import Structure
from pymatgen.io.vasp.inputs import Poscar
import json
import csv

def retrieve_material_data(mpid):
    base_url = "https://api.materialsproject.org/materials/summary/"
    fields = "/?_fields=energy_above_hull%2Ck_vrh%2Ck_voigt%2Ck_reuss&_all_fields=false"

    # Combine the URL parts
    url = base_url + mpid + fields

    # Specify the curl command
    api_key = "X-API-KEY: y2JUaVoZsveEGztql8NGJwdwazCvUstX"
    curl_command = f'curl -X GET "{url}" -H "accept: application/json" -H "{api_key}"'

    try:
        # Execute the curl command and capture the output
        output = subprocess.check_output(curl_command, shell=True)
        json_output = output.decode()
        input_data = json.loads(json_output)

        # Prepare a dictionary to store the data
        template = {
            'mp-id': [],
            'energy_above_hull': [],
            'k_voigt': [],
            'k_reuss': [],
            'k_vrh': []
        }

        # Extract data from the JSON and populate the dictionary
        item = input_data['data'][0]
        template['mp-id'].append(mpid)
        template['energy_above_hull'].append(item['energy_above_hull'])
        template['k_voigt'].append(item['k_voigt'])
        template['k_reuss'].append(item['k_reuss'])
        template['k_vrh'].append(item['k_vrh'])

        # Create a DataFrame from the collected data
        df = pd.DataFrame(template)

        return df

    except subprocess.CalledProcessError as e:
        print("Command execution failed.")
        print("Error:", e)
        return None

# Specify the CSV file path
csv_file = 'input.csv'  # Replace with your CSV file path

# Specify the column name to extract values from
column_name = 'material_id'  # Replace with the desired column name

all_df = pd.DataFrame()

# Read the CSV file and iterate through each row
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Extract the value from the specified column
        value = row[column_name]

        # Pass the value to the processing method
        df2 = retrieve_material_data(value)
        if df2 is not None:
            dataframes = [all_df, df2]
            # Merge rows of the DataFrames
            all_df = pd.concat(dataframes, ignore_index=True)
        
# Save the data to a CSV file
all_df.to_csv("props_output.csv", index=False)
