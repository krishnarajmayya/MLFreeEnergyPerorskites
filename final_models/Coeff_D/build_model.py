#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 10:57:29 2023

@author: krishnarajmayya
"""
import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, RationalQuadratic, Exponentiation
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import pickle

# Load the data from CSV file
data = pd.read_csv('scaled_train_data.csv', encoding='cp1252')
data.fillna(0, inplace= True)

target = 'Coeff_D'

Y = data[target] 
X = data.drop([target,'Name'], axis=1)

# Create a Gaussian Process Regression model with an RBF kernel
model = GaussianProcessRegressor(optimizer='fmin_l_bfgs_b',random_state=50,
                                    kernel=1.0 + 1.0 * Exponentiation(Matern(length_scale=1.0, nu=1.5), exponent=2),
                                    alpha=0.01, n_restarts_optimizer=1)

# Train the model
model.fit(X, Y)

# Make predictions on the training data
y_pred = model.predict(X)

# Calculate R2 score
r2 = r2_score(Y, y_pred)
print("R2 Score:", r2)

# Calculate root mean square error (RMSE)
mse = mean_squared_error(Y, y_pred)
rmse = np.sqrt(mse)
print("Root Mean Square Error (RMSE):", rmse)

# Save the model to a pickle file
with open('Coeff_D_GPR.pkl', 'wb') as f:
    pickle.dump(model, f)

