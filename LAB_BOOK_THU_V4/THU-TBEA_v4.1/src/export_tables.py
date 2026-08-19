# src/export_tables.py
# Exporta las tablas de estadisticas a CSV y LaTeX (booktabs) para la tesis.
# Salidas en labbook/tables/. NOTA: ejecutar desde la raiz del proyecto.
import csv
import json
from pathlib import Path

RESULTS = Path('results')
OUT_DIR = Path('labbook/tables')

CAPTIONS = {
    'tabla2_residuos': ('Estadistica completa de los residuos Pantheon+',
                        'Full Pantheon+ residual statistics',
                        'Vollstaendige Pantheon+ Residuenstatistik'),
    'tabla3_mcmc': ('Estadistica posterior del MCMC de torsion',
                    'Torsion MCMC posterior statistics',
                    'MCMC-Posterior-Statistik der Torsion'),
}


def read_json(name):
    p = RESULTS / name
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None


def write_csv(path, header, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def write_tex(path, caption_es, header, rows):
    cols = 'l' * len(header)
    head = ' & '.join(header) + r' \\'
    body = '\n'.join(' & '.join(str(c) for c in r) + r' \\' for r in rows)
    tex = (f"% Generado automaticamente por src/export_tables.py - THU-TBEA v4.1\n"
           f"\\begin{{table}}[htbp]\n  \\centering\n"
           f"  \\caption{{{caption_es}}}\n"
           f"  \\begin{{tabular}}{{{cols}}}\n    \\toprule\n"
           f"    {head}\n    \\midrule\n{body}\n    \\bottomrule\n"
           f"  \\end{{tabular}}\n\\end{{table}}\n")
    path.write_text(tex, encoding='utf-8')


def run():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Tabla 2: residuos ----
    st = read_json('stats_residuals.json')
    if st:
        rows = [(k, f'{v:.6g}' if isinstance(v, float) else v) for k, v in st.items()]
        write_csv(OUT_DIR / 'tabla2_residuos.csv', ['estadistico', 'valor'], rows)
        write_tex(OUT_DIR / 'tabla2_residuos.tex', CAPTIONS['tabla2_residuos'][0],
                  ['Estadistico', 'Valor'], rows)
        print('tabla2_residuos: CSV + LaTeX exportados')

    # ---- Tabla 3: MCMC ----
    st = read_json('stats_mcmc.json')
    if st:
        header = ['parametro', 'media', 'sigma', 'IC68_inf', 'IC68_sup',
                  'IC95_inf', 'IC95_sup', 'inyectado']
        rows = []
        for name, d in st['parametros'].items():
            rows.append([name, f"{d['media']:.5f}", f"{d['desv_est']:.5f}",
                         f"{d['ic68_inf']:.5f}", f"{d['ic68_sup']:.5f}",
                         f"{d['ic95_inf']:.5f}", f"{d['ic95_sup']:.5f}",
                         f"{d['valor_inyectado']:.5f}"])
        rows.append(['significancia_xi [sigma]',
                     f"{st['significancia_xi_sigma']:.2f}", '', '', '', '', '', ''])
        write_csv(OUT_DIR / 'tabla3_mcmc.csv', header, rows)
        write_tex(OUT_DIR / 'tabla3_mcmc.tex', CAPTIONS['tabla3_mcmc'][0],
                  ['Parametro', 'Media', r'$\sigma$', 'IC68 inf', 'IC68 sup',
                   'IC95 inf', 'IC95 sup', 'Inyectado'], rows)
        print('tabla3_mcmc: CSV + LaTeX exportados')

    print(f'Tablas exportadas en {OUT_DIR}/')


if __name__ == '__main__':
    run()
