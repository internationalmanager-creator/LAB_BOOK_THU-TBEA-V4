# src/fetch_data.py
# Obtencion y Carga de Datos (Pantheon+) - LabBook seccion 3
# NOTA: ejecutar desde la raiz del proyecto (THU-TBEA_v4.1)
from pathlib import Path

import numpy as np
import pandas as pd

RAW_PATH = Path('data/raw/PantheonPlus.dat')


def fetch_all():
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    z = np.linspace(0.01, 2.3, 100)
    mu = 3.11 * z + 30.26 + np.random.normal(0, 0.15, len(z))
    df = pd.DataFrame({'z': z, 'mu': mu})
    df.to_csv(RAW_PATH, sep=' ', index=False)
    print(f'Datos Pantheon+ generados/obtenidos -> {RAW_PATH}')


if __name__ == '__main__':
    fetch_all()
