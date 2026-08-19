# src/constants.py
# Definicion de Constantes Fisicas (Atractor Aureo) - LabBook seccion 2
import numpy as np

phi = (1 + np.sqrt(5)) / 2
beta0 = 0.3803
H0_ref = 76.0
Om_ref = 0.31
xi_shield = 0.02
theta_phi = 2 * np.pi * (2 - phi)

if __name__ == '__main__':
    print(f'phi (razon aurea)   = {phi:.10f}')
    print(f'beta0               = {beta0}')
    print(f'H0_ref              = {H0_ref} km/s/Mpc')
    print(f'Om_ref              = {Om_ref}')
    print(f'xi_shield           = {xi_shield}')
    print(f'theta_phi           = {theta_phi:.10f} rad')
