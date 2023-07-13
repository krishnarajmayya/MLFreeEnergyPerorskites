#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 00:26:48 2023

@author: krishnarajmayya
"""

import csv
import json
import tempfile
import shutil
import math
import roman

def find_optimum_combination(data, a_site, b_site, v_X):
    # Find the optimum combination of v_A and v_B satisfying v_A + v_B - v_X * 3 = 0
    optimum_combination = None
    min_distance = float('inf')

    for v_A in data[a_site].keys():
        v_B = v_X * -3 - int(v_A)
        if str(v_B) in data[b_site]:
            distance = abs(int(v_A) + int(v_B) + v_X * 3)
            if distance < min_distance:
                min_distance = distance
                optimum_combination = (v_A, str(v_B))

    # If no combination satisfies the equation, find the nearest combination
    if optimum_combination is None:
        nearest_combination = None
        min_difference = float('inf')

        for v_A in data[a_site].keys():
            for v_B in data[b_site].keys():
                difference = abs(int(v_A) + int(v_B) + v_X * 3)
                if difference < min_difference:
                    min_difference = difference
                    nearest_combination = (v_A, str(v_B))

        optimum_combination = nearest_combination
    print(optimum_combination)

    return optimum_combination

def find_nearest_value(data, key, target, col_key):
    print(target)
    # Find the nearest value in the list of values
    if col_key == 'v_A':
        values = [int(value) for value in data[key].keys()]
    elif col_key == 'c_A':
        target = int(roman.fromRoman(target))
        values = [
            int(roman.fromRoman(value[:-2])) if value.endswith('PY') or value.endswith('SQ') else
            int(roman.fromRoman(value))
            for value in data[key].keys()
            if value and value != ''
        ]
    nearest_value = min(values, key=lambda x: abs(x - target))
    if col_key == 'v_A':
        return str(nearest_value)
    elif col_key == 'c_A':
        nearest_roman = roman.toRoman(nearest_value)
        if nearest_roman in data[key].keys():
            return nearest_roman
        elif nearest_roman + 'SQ' in data[key].keys():
            return nearest_roman + 'SQ'
        elif nearest_roman + 'PY' in data[key].keys():
            return nearest_roman + 'PY'
        else:
            return nearest_roman


def process_csv_file(file_path, json_file_path):
    # Define the columns to check for emptiness
    radii_to_calculate = ['s_A', 's_B']

    # Define the columns to use for calculation
    oxidation_states = ['v_A', 'v_B', 'v_X']

    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)  # Read all rows into a list

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    for row in rows:
        # Check if both columns to check are empty
        print(row['A_site'],row['B_site'])
        
        # Define the variables for calculation
        v_A = 0
        v_B = 0
        v_X = 0
        
        c_A = 'XII'
        c_B = 'VI'
        
        if row['s_A'].strip() == '' and row['s_B'].strip() == '':
            # Find the optimum combination of v_A and v_B satisfying v_A + v_B - v_X * 3 = 0
            v_X = int(float(row['v_X']))
            v_A, v_B = find_optimum_combination(data, row['A_site'], row['B_site'], v_X)

            # Fill in the empty columns based on the variable values
            c_A = find_nearest_value(data[row['A_site']], v_A, c_A, 'c_A')
            c_B = find_nearest_value(data[row['B_site']], v_B, c_B, 'c_A')
            row['s_A'] = data[row['A_site']][v_A][c_A]['r_ionic']
            row['s_B'] = data[row['B_site']][v_B][c_B]['r_ionic']
            row['v_A'] = v_A
            row['v_B'] = v_B

        # Check if either column is empty
        elif row['s_A'].strip() == '':
            # Calculate variables based on values in calculation columns
            v_A = abs(int(float(row['v_X'])) * -3 - int(float(row['v_B'])))
            v_X = int(float(row['v_X']))

            # Fill in the empty column based on the variable values
            v_A = find_nearest_value(data, row['A_site'], v_A, 'v_A')
            c_A = find_nearest_value(data[row['A_site']], v_A, c_A, 'c_A')
            row['s_A'] = data[row['A_site']][v_A][c_A]['r_ionic']
            row['v_A'] = v_A

        elif row['s_B'].strip() == '':
            # Calculate variables based on values in calculation columns
            v_B = abs(int(float(row['v_X'])) * -3 - int(float(row['v_A'])))
            v_X = int(float(row['v_X']))

            # Fill in the empty column based on the variable values
            v_B = find_nearest_value(data, row['B_site'], v_B, 'v_A')
            c_B = find_nearest_value(data[row['B_site']], v_B, c_B, 'c_A')
            row['s_B'] = data[row['B_site']][v_B][c_B]['r_ionic']
            row['v_B'] = v_B

    # Save the updated data back to the same CSV file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        temp_file_path = temp_file.name

    # Replace the original file with the updated data
    shutil.move(temp_file_path, file_path)

# Usage
csv_file_path = 'shannon_radii.csv'  # Replace with the actual CSV file path
json_file_path = 'shannon-radii.json'  # Replace with the actual JSON file path
process_csv_file(csv_file_path, json_file_path)