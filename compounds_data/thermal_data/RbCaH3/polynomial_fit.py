#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 16:29:13 2023

@author: krishnarajmayya
"""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os

def read_thermal_properties(input_file_path):
    try:
        f = open(input_file_path, 'r')
    except FileNotFoundError:
        print("Error: occurred in the current directory '{}'.".format(os.getcwd()))
        print("Error: File '{}' not found.".format(input_file_path))
        return None, None

    try:
        temp = []
        e_free = []

        lines = f.readlines()

        n = float(lines[8].split()[1]) / 5.0

        for i in range(len(lines)):
            if i >= 17:
                if "temperature" in lines[i]:
                    temp.append(float(lines[i].split()[2]))
                if "free_energy" in lines[i]:
                    e_free.append((float(lines[i].split()[1])) / n)

        f.close()

        temp = np.array(temp)
        efree = np.array(e_free)

        return temp, efree

    except Exception as e:
        print("Error: {} occurred in the current directory '{}'.".format(str(e), os.getcwd()))
        print("Error:", str(e))
        return None, None


def second_fit(temp, efree, output_file_path):
    if temp is None or efree is None:
        return

    try:
        Ef_T = np.zeros(len(temp))
        Ef_c = np.zeros(len(temp))

        # Curve fitting
        def polynom(x, a, b, c):
            return a * x**2 + b * x + c

        paramPoly, param_covPoly = curve_fit(polynom, temp, efree)
        freePoly = polynom(temp, paramPoly[0], paramPoly[1], paramPoly[2])

        with open(output_file_path, 'w') as f1:
            for i in range(len(temp)):
                f1.write(str(temp[i]) + ',')
            f1.write('\n')
            for i in range(len(temp)):
                f1.write(str(efree[i]) + ',')
            f1.write('\n')
            for i in range(len(temp)):
                f1.write(str(freePoly[i]) + ',')

        with open("second_coefficients.dat", 'w') as f2:
            f2.write(str(paramPoly[0]) + "," + str(paramPoly[1]) + "," + str(paramPoly[2]))

        plt.plot(temp, efree, '-k', label='Free energy')
        plt.plot(temp, freePoly, '-r', label='poly fit')

        plt.xlabel("Temperature (K)")
        plt.ylabel("Energy (eV)")
        plt.title("Free Energy vs Temperature")
        plt.xlim([0, 1000])
        plt.legend(loc=4)
        plt.savefig("free_energy_2nd.png")

    except Exception as e:
        print("Error: {} occurred in the current directory '{}'.".format(str(e), os.getcwd()))
        print("Error:", str(e))

def third_fit(temp, efree, output_file_path):
    if temp is None or efree is None:
        return

    try:
        Ef_T = np.zeros(len(temp))
        Ef_c = np.zeros(len(temp))

        # curve fitting
        def polynom(x, a, b, c, d):
            return a * x**3 + b * x**2 + c * x + d

        paramPoly, param_covPoly = curve_fit(polynom, temp, efree)

        freePoly = polynom(temp, paramPoly[0], paramPoly[1], paramPoly[2], paramPoly[3])
        
        with open(output_file_path, 'w') as f1:
            for i in range(len(temp)):
                f1.write(str(temp[i]) + ',')
            f1.write('\n')
            for i in range(len(temp)):
                f1.write(str(efree[i]) + ',')
            f1.write('\n')
            for i in range(len(temp)):
                f1.write(str(freePoly[i]) + ',')

        with open("third_coefficients.dat", 'w') as f1:
            f1.write(str(paramPoly[0]) + "," + str(paramPoly[1]) + "," + str(paramPoly[2]) + "," + str(paramPoly[3]))

        plt.plot(temp, efree, '-k', label='Free energy')
        plt.plot(temp, freePoly, '-r', label='poly fit')

        plt.xlabel("Temperature (K)")
        plt.ylabel("Energy (eV)")
        plt.title("Free Energy vs Temperature")
        plt.xlim([0, 1000])
        plt.legend(loc=4)
        plt.savefig("free_energy_3rd.png")


    except Exception as e:
        print("Error: {} occurred in the current directory '{}'.".format(str(e), os.getcwd()))
        print("Error:", str(e))


def main():
    input_file_path = "thermal_properties.yaml"
    temp, efree = read_thermal_properties(input_file_path)
    second_fit(temp, efree, "Tf_2nd_data.dat")
    third_fit(temp, efree, "Tf_3rd_data.dat")


if __name__ == '__main__':
    main()
