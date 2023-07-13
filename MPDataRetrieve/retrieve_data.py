#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 03:32:00 2023

@author: krishnarajmayya
"""

import subprocess
import pandas as pd
import json

def retrieve_material_data(formula):
    base_url = "https://api.materialsproject.org/materials/summary/?"
    formula_param = "formula={formula}&"
    param1 = "deprecated=false"
    param2 = "_per_page=1000"
    param3 = "_skip=0"
    param4 = "_limit=1000"
    param5 = "_fields=material_id%2Cformula_pretty%2Cdatabase_IDs%2Cvolume%2Cdensity%2Csymmetry%2Cenergy_per_atom%2Ce_total%2Ce_electronic%2Cnsites%2Cnelements%2Cformation_energy_per_atom"
    param6 = "_all_fields=false"

    # Combine the URL parts
    url = base_url + formula_param + param1 + "&" + param2 + "&" + param3 + "&" + param4 + "&" + param5 + "&" + param6

    # Specify the curl command
    api_key = "X-API-KEY: y2JUaVoZsveEGztql8NGJwdwazCvUstX"
    curl_command = f'curl -X GET "{url}" -H "accept: application/json" -H "{api_key}"'

    curl_command = curl_command.format(formula=formula)

    try:
        # Execute the curl command and capture the output
        output = subprocess.check_output(curl_command, shell=True)
        json_output = output.decode()
        input_data = json.loads(json_output)

        # Prepare a dictionary to store the data
        template = {
            'nsites': [],
            'nelements': [],
            'formula_pretty': [],
            'volume': [],
            'density': [],
            'crystal_system': [],
            'symbol': [],
            'number': [],
            'point_group': [],
            'symprec': [],
            'version': [],
            'material_id': [],
            'energy_per_atom': [],
            'formation_energy_per_atom': [],
            'e_total': [],
            'e_electronic': [],
            'icsd': []
        }

        # Extract data from the API response and populate the dictionary
        for item in input_data['data']:
            template['nsites'].append(item['nsites'])
            template['nelements'].append(item['nelements'])
            template['formula_pretty'].append(item['formula_pretty'])
            template['volume'].append(item['volume'])
            template['density'].append(item['density'])
            template['crystal_system'].append(item['symmetry']['crystal_system'])
            template['symbol'].append(item['symmetry']['symbol'])
            template['number'].append(item['symmetry']['number'])
            template['point_group'].append(item['symmetry']['point_group'])
            template['symprec'].append(item['symmetry']['symprec'])
            template['version'].append(item['symmetry']['version'])
            template['material_id'].append(item['material_id'])
            template['energy_per_atom'].append(item['energy_per_atom'])
            template['formation_energy_per_atom'].append(item['formation_energy_per_atom'])
            template['e_total'].append(item['e_total'])
            template['e_electronic'].append(item['e_electronic'])
            template['icsd'].append(item['database_IDs'].get('icsd', ''))

        # Create a DataFrame from the collected data
        df = pd.DataFrame(template)
        return df

    except subprocess.CalledProcessError as e:
        print("Command execution failed.")
        print("Error:", e)
        return None


element_A = ['Li', 'Be', 'B', 'C', 'Na', 'Mg', 'Al', 'Si', 'P', 'K',
            'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu',
            'Zn', 'Ga', 'Ge', 'As', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo',
            'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Cs',
            'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb',
            'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re',
            'Os', 'Ir', 'Pt', 'Au', 'Tl', 'Pb', 'Bi', 'Po', 'Fr', 'Ra',
            'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu']

element_B = ['Li', 'Be', 'B', 'C', 'Na', 'Mg', 'Al', 'Si', 'P', 'K',
            'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu',
            'Zn', 'Ga', 'Ge', 'As', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo',
            'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Cs',
            'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb',
            'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re',
            'Os', 'Ir', 'Pt', 'Au', 'Tl', 'Pb', 'Bi', 'Po', 'Fr', 'Ra',
            'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu']

element_X = ['H', 'N', 'O', 'F', 'S', 'Cl', 'Se', 'Br', 'I']

all_df = pd.DataFrame()

# Iterate over combinations of elements to generate formulas
for element_1 in element_A:
    for element_2 in element_B:
        for element_3 in element_X:
            formula = element_1 + element_2 + element_3 + '3'
            df2 = retrieve_material_data(formula)
            if df2 is not None:
                dataframes = [all_df, df2]
                # Merge rows of the DataFrames
                all_df = pd.concat(dataframes, ignore_index=True)

# Save the data to a CSV file
all_df.to_csv("output.csv", index=False)
