#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:32:28 2023

@author: krishnarajmayya
"""

from data_preparation.collect_all_data import process_compounds
from data_preparation.merge_shannon import merge_shannon
from data_preparation.collect_shannon_radii.fill_shannon_radii import process_csv_file
from data_preparation.collect_shannon_radii.merge_csv import merge
from data_preparation.collect_shannon_radii.collect_unique_compounds import find_unique
import models.Coeff_A.predict as coeffA
import models.Coeff_B.predict as coeffB
import models.Coeff_C.predict as coeffC
import models.Coeff_D.predict as coeffD
from merge_coeff import merge_coeff

# File paths
input_file = 'input.csv'
shannon_file = 'data_preparation/shannon_radii.csv'
compound_file = 'data_preparation/compounds.csv'
elements_file = 'data_preparation/elements_all.csv'
combined_data_file = 'Combined_All.csv'
poscar_path = 'data_preparation/poscars/'

distinct_compounds_file = 'data_preparation/collect_shannon_radii/input_unique.csv'
shannon_json_file_path = 'data_preparation/collect_shannon_radii/shannon-radii.json'
temp_shannon_file = 'data_preparation/collect_shannon_radii/temp.csv'

print("Step 1: Finding unique compounds")
find_unique(input_file, distinct_compounds_file)
print("Step 1 completed.")

print("Step 2: Merging shannon radii for A, B, and X sites")
merge(distinct_compounds_file, 'data_preparation/collect_shannon_radii/A_site.csv', 'A_site', temp_shannon_file)
merge(temp_shannon_file, 'data_preparation/collect_shannon_radii/B_site.csv', 'B_site', temp_shannon_file)
merge(temp_shannon_file, 'data_preparation/collect_shannon_radii/X_site.csv', 'X_site', temp_shannon_file)
print("Step 2 completed.")

print("Step 3: Processing shannon radii CSV to JSON")
process_csv_file(temp_shannon_file, shannon_json_file_path, shannon_file)
print("Step 3 completed.")

print("Step 4: Merging shannon radii with compounds")
merge_shannon(input_file, shannon_file, compound_file)
print("Step 4 completed.")

print("Step 5: Processing compounds and generating combined data")
process_compounds(compound_file, poscar_path, elements_file, combined_data_file)
print("Step 5 completed.")

coefficients = {
    coeffA: {
        'input_file': 'models/Coeff_A/input.csv',
        'model_file': 'models/Coeff_A/Coeff_A_GPR.pkl',
        'feature_scaler_file': 'models/Coeff_A/std_scaler.pkl',
        'scaler_file': 'models/Coeff_A/standard_Coeff_A_scaler.pkl',
        'output_file': 'output_coeff_A.csv'
    },
    coeffB: {
        'input_file': 'models/Coeff_B/input.csv',
        'model_file': 'models/Coeff_B/Coeff_B_GPR.pkl',
        'feature_scaler_file': 'models/Coeff_B/std_scaler.pkl',
        'scaler_file': 'models/Coeff_B/standard_Coeff_B_scaler.pkl',
        'output_file': 'output_coeff_B.csv'
    },
    coeffC: {
        'input_file': 'models/Coeff_C/input.csv',
        'model_file': 'models/Coeff_C/Coeff_C_GPR.pkl',
        'feature_scaler_file': 'models/Coeff_C/std_scaler.pkl',
        'scaler_file': 'models/Coeff_C/standard_Coeff_C_scaler.pkl',
        'output_file': 'output_coeff_C.csv'
    },
    coeffD: {
        'input_file': 'models/Coeff_D/input.csv',
        'model_file': 'models/Coeff_D/Coeff_D_GPR.pkl',
        'feature_scaler_file': 'models/Coeff_D/std_scaler.pkl',
        'scaler_file': 'models/Coeff_D/standard_Coeff_D_scaler.pkl',
        'output_file': 'output_coeff_D.csv'
    }
}

print("Step 6: Performing predictions")
for i, (coeff, info) in enumerate(coefficients.items(), 1):
    input_file = info['input_file']
    model_file = info['model_file']
    feature_scaler_file = info['feature_scaler_file']
    scaler_file = info['scaler_file']
    output_file = info['output_file']

    # Prepare input data
    coeff_obj = getattr(coeff, 'prepare_input')
    coeff_obj(combined_data_file, input_file)

    # Make predictions
    coeff_obj = getattr(coeff, 'make_predictions')
    coeff_obj(input_file, feature_scaler_file, model_file, scaler_file, output_file)

    print(f"Predictions completed. ({i}/{len(coefficients)})")
print("Step 6 completed.")

print("Step 7: Merging the coefficients to a combined file")
merge_coeff(combined_data_file, 'output_coeff_A.csv', combined_data_file)
merge_coeff(combined_data_file, 'output_coeff_B.csv', combined_data_file)
merge_coeff(combined_data_file, 'output_coeff_C.csv', combined_data_file)
merge_coeff(combined_data_file, 'output_coeff_D.csv', combined_data_file)
print("Step 7 completed.")
