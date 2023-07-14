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
    needed_feature_names = ['X_EA', 'mean_A2B', 'X_Z', 'X_Rvdw', 'X_IEII', 'mean_X2X',
                            'A_Rvdw', 'mean_A2X', 'A_IEI', 'E_coh', 'A_ChiA', 'B_Hf', 'X_G',
                            'A_EA', 'std_A2X', 'A_ChiP', 'B_MP', 'std_B2X', 'OF', 'A_MP',
                            'B_Z', 'X_Kappa', 'A_Kappa', 'B_Kappa', 'B_Ra', 'A_Z', 'B_Rho',
                            'X_MV', 'A_CvM', 'A_G', 'B_EA', 'B_CvM', 'TF', 'std_X2X', 'A_B',
                            'std_A2B', 'B_ChiP', 'X_IEI', 'B_MV', 'B_IEI']
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
    output['Coeff_B'] = y_pred

    with open(coeff_scaler, 'rb') as file:
        scaler_model = pickle.load(file)

    scaled_column = output[['Coeff_B']]
    unscaled_column = scaler_model.inverse_transform(scaled_column)

    output['unscaled_Coeff_B'] = unscaled_column

    output.to_csv(output_file_path, index=False)
