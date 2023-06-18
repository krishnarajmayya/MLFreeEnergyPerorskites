#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 23:36:29 2023

@author: krishnarajmayya
"""

import os
import numpy as np

def run_in_child_folders(relative_path):
    # Get the current working directory
    current_dir = os.getcwd()
    absolute_path = os.path.join(os.getcwd(), relative_path)
    destination_file_path = os.path.join(absolute_path, "Temp_vs_fe.dat")

    subfolders = [f.path for f in os.scandir(absolute_path) if f.is_dir()]

    # Iterate over the subfolders
    for subfolder_path in subfolders:
        try:
            # Move to the subfolder
            os.chdir(subfolder_path)

            # Execute the method in the subfolder
            process_thermal_properties()
            
            copy_and_append("Temp_vs_fe.dat", destination_file_path)

        except Exception as e:
            print("An error occurred in folder '{}':".format(subfolder_path), str(e))

        finally:
            # Move back to the original directory
            os.chdir(current_dir)

def process_thermal_properties():
    input_file_path = "thermal_properties.yaml"
    output_file_path = "Temp_vs_fe.dat"

    try:
        # Get the current working directory
        current_dir = os.getcwd()
        
        parent_dir = os.path.basename(current_dir)

        # Set the path for the input file
        input_file_path = os.path.join(current_dir, input_file_path)

        # Set the path for the output file
        output_file_path = os.path.join(current_dir, output_file_path)

        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        temp = []
        e_free = []

        n = float(lines[8].split()[1]) / 5.0

        for i in range(len(lines)):
            if i >= 17:
                if "temperature" in lines[i]:
                    temp.append(float(lines[i].split()[2]))
                if "free_energy" in lines[i]:
                    e_free.append(float(lines[i].split()[1]) / n)

        temp = np.array(temp)
        efree = np.array(e_free)

        with open(output_file_path, 'w') as f1:
            for i in range(len(temp)):
                f1.write(parent_dir + ',' + str(temp[i]) + ',' + str(efree[i]) + '\n')

        print("Data saved successfully in folder '{}'.".format(current_dir))

    except FileNotFoundError:
        print("Error: File '{}' not found in folder '{}'.".format(input_file_path, current_dir))

    except Exception as e:
        print("An error occurred in folder '{}':".format(current_dir), str(e))


def copy_and_append(source_file_path, destination_file_path):
    try:
        with open(source_file_path, 'r') as source_file, open(destination_file_path, 'a') as destination_file:
            # Read the contents of the source file
            contents = source_file.read()
            
            # Append the contents to the destination file
            destination_file.write(contents)
        
        print("Contents copied and appended successfully!")
        
    except FileNotFoundError:
        print(f"Error: File '{source_file_path}' not found.")
        
    except Exception as e:
        print("An error occurred:", str(e))


# Call the method to run in child folders
run_in_child_folders('thermal_data')
