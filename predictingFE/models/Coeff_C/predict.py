#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 22:00:48 2023

@author: krishnarajmayya
"""
import pandas as pd
import numpy as np
import pickle


def prepare_input(input_file_path, output_file_path):
    # Load data from CSV file
    data = pd.read_csv(input_file_path)

    column_to_extract = data[['material_id','Name']]
    needed_feature_names = ['mean_A2B', 'X_IEII', 'X_Z', 'mean_X2X', 'mean_A2X', 'X_Rvdw',
                            'A_Rvdw', 'X_EA', 'E_coh', 'X_Kappa', 'B_Kappa', 'A_IEI', 'A_ChiA',
                            'X_IEI', 'B_EA', 'X_MV', 'X_ChiP', 'std_A2X', 'A_Z', 'A_ChiP',
                            'A_Kappa', 'A_MP', 'B_ChiP', 'std_B2X', 'B_Z', 'B_MP', 'A_CvM',
                            'A_EA', 'B_Rho', 'B_IEI', 'B_Hf', 'density', 'A_B', 'OF', 'A_G',
                            'TF', 'X_Rho', 'B_MV', 'std_A2B', 'B_CvM']
    needed_features = data[needed_feature_names]  
    name_df = pd.DataFrame(column_to_extract, columns=['material_id','Name'])
    input_df = pd.DataFrame(needed_features, columns=needed_feature_names)

    input_file = pd.concat([name_df, input_df], axis=1)

    # Save the preprocessed data to a new CSV file
    input_file.to_csv(output_file_path, index=False)
    
def make_predictions(input_file_path,feature_scaler,model_file,coeff_scaler,output_file_path):
    # Load data from CSV file
    data = pd.read_csv(input_file_path)

    column_to_extract = data[['material_id','Name']]  
    output = pd.DataFrame(column_to_extract, columns=['material_id','Name'])

    # Extract the features (X) and target variable (Y)
    X = data.drop(columns=['material_id','Name'])

    # Load the scaling model from a pickle file
    with open(feature_scaler, 'rb') as file:
        scaler = pickle.load(file)

    scaled_features = pd.DataFrame(scaler.transform(X), columns=X.columns)
    scaled_features.fillna(0, inplace=True)

    # Load the GPR model from a pickle file
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    
    # Make predictions on the data
    y_pred = model.predict(scaled_features)

    # Add predictions to the DataFrame
    output['Coeff_C'] = y_pred

    with open(coeff_scaler, 'rb') as file:
        scaler_model = pickle.load(file)

    scaled_column = output[['Coeff_C']]
    unscaled_column = scaler_model.inverse_transform(scaled_column)

    output['unscaled_Coeff_C'] = unscaled_column

    output.to_csv(output_file_path, index=False)
