# src/analyze_residuals.py
# Analisis de Residuos e Irregularidades - LabBook seccion 4 (ampliada)
# Genera: dispersion Pantheon+, histograma de residuos, QQ-plot
# y exporta toda la estadistica a results/stats_residuals.json
# NOTA: ejecutar desde la raiz del proyecto (THU-TBEA_v4.1)
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import save_fig  # noqa: E402

RAW_PATH = Path('data/raw/PantheonPlus.dat')
FIG_DIR = Path('figures')
STATS_PATH = Path('results/stats_residuals.json')
SIGMA_MU = 0.15  # dispersion instrumental usada en fetch_data.py


def analyze():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    STATS_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_PATH, sep=' ')
    modelo = 3.11 * df['z'] + 30.26
    res = df['mu'] - modelo

    # ---- Estadistica completa ----
    k2, p_dagostino = stats.normaltest(res)
    w_shapiro, p_shapiro = stats.shapiro(res)
    anderson = stats.anderson(res, dist='norm')
    chi2_red = float(np.sum((res / SIGMA_MU) ** 2) / (len(res) - 2))

    stats_dict = {
        'n': int(len(res)),
        'media': float(res.mean()),
        'mediana': float(res.median()),
        'desv_est': float(res.std(ddof=1)),
        'error_estandar': float(res.std(ddof=1) / np.sqrt(len(res))),
        'asimetria': float(stats.skew(res)),
        'curtosis': float(stats.kurtosis(res)),  # exceso de curtosis
        'min': float(res.min()),
        'max': float(res.max()),
        'rms': float(np.sqrt(np.mean(res ** 2))),
        'dagostino_k2': float(k2),
        'dagostino_p': float(p_dagostino),
        'shapiro_w': float(w_shapiro),
        'shapiro_p': float(p_shapiro),
        'anderson_A2': float(anderson.statistic),
        'anderson_crit_5pct': float(anderson.critical_values[2]),
        'chi2_red': chi2_red,
    }
    STATS_PATH.write_text(json.dumps(stats_dict, indent=2, ensure_ascii=False),
                          encoding='utf-8')
    print(f"Test Normalidad (D'Agostino) p-valor: {p_dagostino:.4e}")
    print(f'Test Shapiro-Wilk p-valor:            {p_shapiro:.4e}')
    print(f'Chi2 reducido:                        {chi2_red:.4f}')
    print(f'Estadisticas -> {STATS_PATH}')

    # ---- Figura 1: dispersion Pantheon+ con modelo ----
    plt.figure(figsize=(8, 5))
    plt.scatter(df['z'], df['mu'], s=18, color='teal', alpha=0.75,
                label='Pantheon+ (sintetico)')
    z_sorted = np.sort(df['z'])
    plt.plot(z_sorted, 3.11 * z_sorted + 30.26, color='crimson', lw=2,
             label=r'Modelo $\mu(z)=3.11\,z+30.26$')
    plt.xlabel('Corrimiento al rojo $z$')
    plt.ylabel(r'Modulo de distancia $\mu$ [mag]')
    plt.title('Diagrama de Hubble Pantheon+')
    plt.legend()
    plt.tight_layout()
    save_fig(plt.gcf(), FIG_DIR / 'pantheon_scatter_plot.png', dpi=150)
    plt.close()

    # ---- Figura 2: histograma de residuos ----
    plt.figure(figsize=(8, 5))
    sns.histplot(res, kde=True, color='teal', stat='density',
                 label='Residuos')
    x = np.linspace(res.min(), res.max(), 200)
    plt.plot(x, stats.norm.pdf(x, res.mean(), res.std(ddof=1)),
             color='crimson', lw=2, label='Gaussiana ajustada')
    plt.title('Distribucion de Residuos Pantheon+')
    plt.xlabel(r'Residuo $r_i = \mu_{obs} - \mu_{modelo}$ [mag]')
    plt.legend()
    plt.tight_layout()
    save_fig(plt.gcf(), FIG_DIR / 'pantheon_residuals_hist.png', dpi=150)
    plt.close()

    # ---- Figura 3: QQ-plot de normalidad ----
    plt.figure(figsize=(6, 6))
    stats.probplot(res, dist='norm', plot=plt)
    plt.title('QQ-plot de los Residuos vs. Normal')
    plt.tight_layout()
    save_fig(plt.gcf(), FIG_DIR / 'pantheon_residuals_qq.png', dpi=150)
    plt.close()

    print(f'Figuras guardadas en {FIG_DIR}/')
    return stats_dict


if __name__ == '__main__':
    analyze()
