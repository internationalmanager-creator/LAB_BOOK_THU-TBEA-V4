# src/generate_golden_figures.py
# Figuras del Atractor Aureo: helice aurea 3D (fig_01) y flujo RG (fig_07)
# NOTA: ejecutar desde la raiz del proyecto (THU-TBEA_v4.1)
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from constants import phi, beta0, theta_phi  # noqa: E402
from utils import save_fig  # noqa: E402

FIG_DIR = Path('figures')


def golden_helix():
    """fig_01: Helice aurea 3D. Radio con crecimiento de espiral aurea
    r = phi^(2*theta/pi) y paso angular dado por el angulo aureo theta_phi."""
    theta = np.linspace(0, 6 * np.pi, 800)
    r = phi ** (2 * theta / np.pi)
    r = r / r.max()  # normalizado a [0, 1]
    x, y = r * np.cos(theta), r * np.sin(theta)
    z = theta / theta.max()

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, color='darkgoldenrod', lw=1.6)
    ax.scatter(x[::40], y[::40], z[::40], color='teal', s=12)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel(r'$z$ (parametro RG)')
    ax.set_title(r'Helice Aurea 3D:  $\theta_\varphi = 2\pi(2-\varphi)$'
                 f' = {theta_phi:.6f} rad')
    fig.tight_layout()
    save_fig(fig, FIG_DIR / 'fig_01_golden_helix.png', dpi=150)
    plt.close(fig)


def rg_attractor():
    """fig_07: Flujo del grupo de renormalizacion hacia el punto fijo beta0.
    beta(beta) = -beta*(beta - beta0) -> todas las trayectorias convergen a beta0."""
    lnmu = np.linspace(0, 8, 400)
    fig, ax = plt.subplots(figsize=(8, 5))
    for b_ini in [0.05, 0.15, 0.30, 0.55, 0.70]:
        # Solucion de dbeta/dlnmu = -beta(beta-beta0)
        b = beta0 / (1 - (1 - beta0 / b_ini) * np.exp(-beta0 * lnmu))
        ax.plot(lnmu, b, lw=1.6, label=rf'$\beta_0^{{ini}}={b_ini}$')
    ax.axhline(beta0, color='crimson', ls='--', lw=2,
               label=rf'Punto fijo $\beta_0 = {beta0}$')
    ax.set_xlabel(r'$\ln(\mu/\mu_0)$')
    ax.set_ylabel(r'$\beta$')
    ax.set_title('Atractor del Grupo de Renormalizacion')
    ax.legend(fontsize=8)
    fig.tight_layout()
    save_fig(fig, FIG_DIR / 'fig_07_rg_attractor.png', dpi=150)
    plt.close(fig)


def run():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    golden_helix()
    rg_attractor()
    print(f'Figuras del Atractor Aureo guardadas en {FIG_DIR}/')


if __name__ == '__main__':
    run()
