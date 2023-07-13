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
    base_url = "https://api.materialsproject.org/materials/tasks/"
    fields = "/?_fields=chemsys%2Ctask_type%2Coutput%2Ctask_label&_all_fields=false"

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
            'chemsys': [],
            'density': [],
            'energy': [],
            'energy_per_atom': []
        }

        # Extract data from the JSON and populate the dictionary
        item = input_data['data'][0]
        template['mp-id'].append(mpid)
        template['chemsys'].append(item['chemsys'])
        template['density'].append(item['output']['density'])
        template['energy'].append(item['output']['energy'])
        template['energy_per_atom'].append(item['output']['energy_per_atom'])

        # Create a DataFrame from the collected data
        df = pd.DataFrame(template)

        # Read the structure object from the JSON
        structure_data = item['output']['structure']

        # Create a pymatgen Structure object
        structure = Structure.from_dict(structure_data)

        return df,structure

    except subprocess.CalledProcessError as e:
        print("Command execution failed.")
        print("Error:", e)
        return None

# Specify the CSV file path
csv_file = 'output_filtered.csv'  # Replace with your CSV file path

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
        df2,structure = retrieve_material_data(value)
        if df2 is not None:
            dataframes = [all_df, df2]
            # Merge rows of the DataFrames
            all_df = pd.concat(dataframes, ignore_index=True)
        
        # Save the Structure as a VASP POSCAR file
        poscar_file = f"poscars/{value}.poscar"
        Poscar(structure).write_file(poscar_file)
        print(f"Structure has been saved as {poscar_file}.")

# Save the data to a CSV file
all_df.to_csv("tasks_output.csv", index=False)