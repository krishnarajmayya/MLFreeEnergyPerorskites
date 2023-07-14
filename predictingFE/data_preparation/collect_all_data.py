#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:19:50 2023

@author: krishnarajmayya
"""

import pandas as pd
import numpy as np
from pymatgen.core.periodic_table import Element
from pymatgen.io.vasp.inputs import Poscar
from pymatgen.core.structure import Structure
from pymatgen.core.lattice import Lattice
from statistics import mean, pstdev

def process_compounds(compounds_file,poscar_path,elements_file,output_file):
    # Read compounds.csv
    compounds = pd.read_csv(compounds_file, sep=',')

    # Get the shape of compounds DataFrame
    compounds_shape = compounds.shape

    # Loop over compounds
    for i in range(len(compounds)):
        # Read POSCAR file
        poscar = Poscar.from_file(poscar_path + compounds.loc[i, "material_id"] + ".poscar",
                                  check_for_POTCAR=False,
                                  read_velocities=False)
        structure = poscar.structure
        lattice = structure.lattice

        # Calculate density
        compounds.loc[i, 'density'] = structure.density

        # Get elements
        A_element = Element(compounds.loc[i, 'A_site'])
        B_element = Element(compounds.loc[i, 'B_site'])
        X_element = Element(compounds.loc[i, 'X_site'])

        sites = structure.sites
        A2B = []
        A2X = []
        B2X = []
        X2X = []

        # Calculate distances between atomic sites
        for j in sites:
            for k in sites:
                if j != k:
                    if j.species.elements[0] == A_element and k.species.elements[0] == B_element and j.distance(k) < 6:
                        A2B.append(j.distance(k))
                    elif j.species.elements[0] == A_element and k.species.elements[0] == X_element and j.distance(k) < 5:
                        A2X.append(j.distance(k))
                    elif j.species.elements[0] == B_element and k.species.elements[0] == X_element and j.distance(k) < 5:
                        B2X.append(j.distance(k))
                    elif j.species.elements[0] == X_element and k.species.elements[0] == X_element and j.distance(k) < 5:
                        X2X.append(j.distance(k))

        # Calculate means and standard deviations
        compounds.loc[i, 'mean_A2B'] = mean(A2B)
        compounds.loc[i, 'mean_A2X'] = mean(A2X)
        compounds.loc[i, 'mean_B2X'] = mean(B2X)
        compounds.loc[i, 'mean_X2X'] = mean(X2X)
        compounds.loc[i, 'std_A2B'] = pstdev(A2B)
        compounds.loc[i, 'std_A2X'] = pstdev(A2X)
        compounds.loc[i, 'std_B2X'] = pstdev(B2X)
        compounds.loc[i, 'std_X2X'] = pstdev(X2X)

    # Read elements_all.csv
    elements = pd.read_csv(elements_file, sep=',')

    # Calculate additional properties
    for i in range(len(compounds)):
        A_element = elements.index[elements['Name'] == compounds.loc[i, 'A_site']]
        B_element = elements.index[elements['Name'] == compounds.loc[i, 'B_site']]
        X_element = elements.index[elements['Name'] == compounds.loc[i, 'X_site']]
        compounds.loc[i, 'E_coh'] = compounds.loc[i, 'Energy'] - elements.at[A_element[0], 'Energy'] - \
                                    elements.at[B_element[0], 'Energy'] - 3 * elements.at[X_element[0], 'Energy']
        compounds.loc[i, 'TF'] = (compounds.loc[i, 's_A'] + compounds.loc[i, 's_X']) / (
                np.sqrt(2) * (compounds.loc[i, 's_B'] + compounds.loc[i, 's_X']))
        compounds.loc[i, 'OF'] = compounds.loc[i, 's_B'] / compounds.loc[i, 's_X']

    # Define elemental properties
    elemental_properties = ['Z', 'M', 'G', 'IEI', 'IEII', 'EA', 'ChiP', 'ChiA',
                            'Rvdw', 'Rc', 'Ra', 'MP', 'BP', 'Rho', 'MV', 'Hf', 'Hv',
                            'Kappa', 'CvM', 'B', 'MendeleevNo']

    # Calculate elemental properties for compounds
    for i in range(len(compounds)):
        for j in elemental_properties:
            compounds.loc[i, 'A_' + j] = elements.at[
                elements.index[elements['Name'] == compounds.loc[i, 'A_site']][0], j]
            compounds.loc[i, 'B_' + j] = elements.at[
                elements.index[elements['Name'] == compounds.loc[i, 'B_site']][0], j]
            compounds.loc[i, 'X_' + j] = elements.at[
                elements.index[elements['Name'] == compounds.loc[i, 'X_site']][0], j]

    # Save compounds DataFrame to Material_prop_all.csv
    compounds.to_csv(output_file, index=False)

