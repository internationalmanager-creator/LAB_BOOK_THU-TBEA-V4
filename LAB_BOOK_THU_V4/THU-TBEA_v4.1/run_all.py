# run_all.py
# Ejecuta el pipeline completo del LabBook THU-TBEA v4.1 (secciones 2 a 6)
# Uso:  python run_all.py        (desde la raiz del proyecto)
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STEPS = [
    ('Seccion 2 - Constantes fisicas', [sys.executable, 'src/constants.py']),
    ('Seccion 3 - Datos Pantheon+', [sys.executable, 'src/fetch_data.py']),
    ('Seccion 4 - Analisis de residuos + estadistica completa',
     [sys.executable, 'src/analyze_residuals.py']),
    ('Seccion 5 - MCMC de torsion + estadistica posterior',
     [sys.executable, 'scripts/run_mcmc_torsion.py']),
    ('Seccion 5b - Figuras del Atractor Aureo',
     [sys.executable, 'src/generate_golden_figures.py']),
    ('Seccion 6 - Atlas Tecnico trilingue',
     [sys.executable, 'src/generate_labbook.py']),
    ('Seccion 7 - Exportar tablas (CSV + LaTeX)',
     [sys.executable, 'src/export_tables.py']),
]


def main():
    for titulo, cmd in STEPS:
        print('=' * 60)
        print(titulo)
        print('=' * 60)
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            print(f'ERROR en: {titulo}')
            sys.exit(result.returncode)
        print()
    print('Pipeline completado. Abre labbook/Atlas_Tecnico_THU-TBEA.html en tu navegador.')


if __name__ == '__main__':
    main()
