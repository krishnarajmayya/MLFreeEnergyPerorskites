#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 01:00:45 2023

@author: krishnarajmayya
"""

import os

def combine_fitting_data(parent_folder, fit_values_file):
    try:
        absolute_path = os.path.join(os.getcwd(), parent_folder)

        with open(fit_values_file, "w") as fit_file:
            for foldername in os.listdir(absolute_path):
                folder_path = os.path.join(absolute_path, foldername)

                if os.path.isdir(folder_path):
                    os.chdir(folder_path)

                    fit = ""

                    try:
                        with open("third_coefficients.dat") as fit_data_file:
                            fit = fit_data_file.readline().strip()
                    except FileNotFoundError:
                        print(f"Error: third_coefficients.dat not found in {folder_path}")

                    if fit:
                        fit_file.write(foldername + "," + fit + "\n")


                    os.chdir("..")
    except Exception as e:
        print("Error:", str(e))

# Example usage:
parent_folder = "thermal_data"
fit_values_file = "fit_values_3rd.dat"

combine_fitting_data(parent_folder, fit_values_file)

