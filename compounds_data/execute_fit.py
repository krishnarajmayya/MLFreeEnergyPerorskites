#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:17:03 2023

@author: krishnarajmayya
"""

import os
import shutil
import subprocess

def run_in_child_folders(source_folder, python_file):
    try:
        # Get the current working directory
        current_dir = os.getcwd()

        # Get the path for the source folder
        source_folder_path = os.path.join(current_dir, source_folder)

        if not os.path.exists(source_folder_path):
            raise ValueError("Source folder '{}' does not exist.".format(source_folder))

        # Get the list of subfolders in the source folder
        subfolders = [f.path for f in os.scandir(source_folder_path) if f.is_dir()]

        if not subfolders:
            print("No subfolders found in '{}'.".format(source_folder))
            return

        # Iterate over the subfolders
        for subfolder_path in subfolders:
            try:
                # Move to the subfolder
                os.chdir(subfolder_path)

                # Copy the Python file from the source folder to the subfolder
                shutil.copy2(os.path.join(current_dir, python_file), subfolder_path)

                # Run the Python file
                subprocess.run(['python', python_file])

            except Exception as e:
                print("Error occurred while processing subfolder '{}': {}".format(subfolder_path, str(e)))

    except Exception as e:
        print("Error:", str(e))

    finally:
        # Move back to the original directory
        os.chdir(current_dir)

# Example usage:
source_folder = "thermal_data"
python_file = "polynomial_fit.py"

run_in_child_folders(source_folder, python_file)

