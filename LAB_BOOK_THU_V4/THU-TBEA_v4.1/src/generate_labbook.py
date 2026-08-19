# src/generate_labbook.py
# Generador del Atlas Tecnico Interactivo - LabBook seccion 6 (ampliada)
# Atlas TRILINGUE (ES/EN/DE) con:
#   - toda la estadistica del pipeline (tablas auto-generadas desde JSON)
#   - debajo de cada figura: explicacion teorica + ecuacion matematica (KaTeX)
#   - selector de idioma ES / EN / DE
# NOTA: ejecutar desde la raiz del proyecto; requiere internet para KaTeX (CDN).
import base64
import datetime
import json
from pathlib import Path

from jinja2 import Template

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from constants import phi, beta0, H0_ref, Om_ref, xi_shield, theta_phi  # noqa: E402

FIG_DIR = Path('figures')
RESULTS = Path('results')
OUT_PATH = Path('labbook/Atlas_Tecnico_THU-TBEA.html')

# ============================================================
#  CONTENIDO TRILINGUE DEL ATLAS
# ============================================================
# Cada seccion: titulo, teoria (3 idiomas), ecuaciones LaTeX y figuras.
SECTIONS = [
    {
        'id': 'datos',
        'titulo': {'es': '1. Diagrama de Hubble Pantheon+',
                   'en': '1. Pantheon+ Hubble Diagram',
                   'de': '1. Pantheon+ Hubble-Diagramm'},
        'figuras': ['pantheon_scatter_plot.png'],
        'ecuaciones': [
            r'\mu(z) = 5\,\log_{10}\!\left(\frac{D_L(z)}{10\ \mathrm{pc}}\right)',
            r'D_L(z) = c\,(1+z)\int_0^{z}\frac{dz^{\prime}}{H(z^{\prime})}',
        ],
        'teoria': {
            'es': ('El modulo de distancia mu(z) relaciona el brillo observado de las '
                   'supernovas Ia con su distancia de luminosidad D_L. La dispersion alrededor '
                   'del modelo ajustado (linea roja) cuantifica la componente no explicada por '
                   'la ley de Hubble de bajo corrimiento y constituye la senal de partida para '
                   'el analisis de torsion espaciotemporal.'),
            'en': ('The distance modulus mu(z) relates the observed brightness of Type Ia '
                   'supernovae to their luminosity distance D_L. The scatter around the fitted '
                   'model (red line) quantifies the component not explained by the low-redshift '
                   'Hubble law and is the starting signal for the spacetime torsion analysis.'),
            'de': ('Der Entfernungsmodul mu(z) verknuepft die beobachtete Helligkeit von '
                   'Supernovae Typ Ia mit ihrer Leuchtkraftentfernung D_L. Die Streuung um das '
                   'angepasste Modell (rote Linie) quantifiziert den Anteil, der nicht durch das '
                   'Hubble-Gesetz bei niedriger Rotverschiebung erklaert wird, und bildet das '
                   'Ausgangssignal fuer die Analyse der Raumzeit-Torsion.'),
        },
    },
    {
        'id': 'residuos',
        'titulo': {'es': '2. Analisis Estadistico de Residuos',
                   'en': '2. Statistical Residual Analysis',
                   'de': '2. Statistische Residuenanalyse'},
        'figuras': ['pantheon_residuals_hist.png', 'pantheon_residuals_qq.png'],
        'ecuaciones': [
            r'r_i = \mu_{\mathrm{obs},i} - \mu_{\mathrm{modelo}}(z_i;\,\hat{\theta})',
            r"K^2 = Z_1^2(g_1) + Z_2^2(g_2) \quad (\mathrm{D'Agostino\text{-}Pearson})",
            r'\chi^2_{\mathrm{red}} = \frac{1}{N-k}\sum_{i=1}^{N}\frac{r_i^2}{\sigma_i^2}',
        ],
        'teoria': {
            'es': ('Los residuos r_i miden la desviacion de cada supernova respecto al modelo. '
                   'El histograma con la gaussiana ajustada y el QQ-plot verifican la hipotesis '
                   'de gaussianidad: el test de D\'Agostino-Pearson combina asimetria (g1) y '
                   'curtosis (g2) en el estadistico K^2, mientras que el chi-cuadrado reducido '
                   'cercano a 1 indica que las barras de error estan bien calibradas. Toda la '
                   'estadistica se resume en la Tabla 2.'),
            'en': ('The residuals r_i measure the deviation of each supernova from the model. '
                   'The histogram with the fitted Gaussian and the QQ-plot test the Gaussianity '
                   'hypothesis: the D\'Agostino-Pearson test combines skewness (g1) and kurtosis '
                   '(g2) into the K^2 statistic, while a reduced chi-squared close to 1 indicates '
                   'well-calibrated error bars. All statistics are summarized in Table 2.'),
            'de': ('Die Residuen r_i messen die Abweichung jeder Supernova vom Modell. Das '
                   'Histogramm mit der angepassten Gausskurve und der QQ-Plot pruefen die '
                   'Gauss-Hypothese: Der D\'Agostino-Pearson-Test kombiniert Schiefe (g1) und '
                   'Kurtosis (g2) zur Statistik K^2, waehrend ein reduziertes Chi-Quadrat nahe 1 '
                   'auf gut kalibrierte Fehlerbalken hinweist. Alle Statistiken sind in '
                   'Tabelle 2 zusammengefasst.'),
        },
    },
    {
        'id': 'mcmc',
        'titulo': {'es': '3. Muestreo MCMC de la Torsion Fermionica',
                   'en': '3. MCMC Sampling of Fermionic Torsion',
                   'de': '3. MCMC-Sampling der Fermionischen Torsion'},
        'figuras': ['mcmc_corner_plot.png', 'mcmc_traces.png'],
        'ecuaciones': [
            r'p(\theta \mid D) \propto \mathcal{L}(D \mid \theta)\;\pi(\theta),'
            r'\qquad \theta = \{H_0,\ \Omega_m,\ \xi\}',
            r'E^2(z) = \Omega_m(1+z)^3 + \Omega_\Lambda + \xi\,(1+z)^4'
            r'\quad (\mathrm{ansatz\ de\ torsion\ THU\text{-}TBEA})',
            r'S(\xi) = \frac{\langle \xi \rangle}{\sigma_\xi} \;\;\Rightarrow\;\;'
            r'\text{significancia de deteccion}',
        ],
        'teoria': {
            'es': ('El teorema de Bayes combina la verosimilitud de los datos con los priors '
                   'para obtener la posterior de los parametros. En el modelo THU-TBEA la '
                   'torsion fermionica xi entra como una componente efectiva que escala como '
                   '(1+z)^4. El corner plot muestra las posteriori marginales y las '
                   'correlaciones; las trazas verifican la mezcla de la cadena. La significancia '
                   'S = <xi>/sigma_xi (Tabla 3) cuantifica la deteccion de la torsion.'),
            'en': ('Bayes\' theorem combines the data likelihood with the priors to yield the '
                   'parameter posterior. In the THU-TBEA model the fermionic torsion xi enters '
                   'as an effective component scaling as (1+z)^4. The corner plot shows the '
                   'marginal posteriors and correlations; the traces verify chain mixing. The '
                   'significance S = <xi>/sigma_xi (Table 3) quantifies the torsion detection.'),
            'de': ('Das Bayes-Theorem kombiniert die Likelihood der Daten mit den Priors und '
                   'liefert die Posterior-Verteilung der Parameter. Im THU-TBEA-Modell geht die '
                   'fermionische Torsion xi als effektive Komponente ein, die wie (1+z)^4 '
                   'skaliert. Der Corner-Plot zeigt die marginalen Posteriors und '
                   'Korrelationen; die Traces pruefen das Mischen der Kette. Die Signifikanz '
                   'S = <xi>/sigma_xi (Tabelle 3) quantifiziert den Torsionsnachweis.'),
        },
    },
    {
        'id': 'atractor',
        'titulo': {'es': '4. El Atractor Aureo y el Grupo de Renormalizacion',
                   'en': '4. The Golden Attractor and the Renormalization Group',
                   'de': '4. Der Goldene Attraktor und die Renormierungsgruppe'},
        'figuras': ['fig_01_golden_helix.png', 'fig_07_rg_attractor.png'],
        'ecuaciones': [
            r'\varphi = \frac{1+\sqrt{5}}{2}, \qquad'
            r'\theta_\varphi = 2\pi(2-\varphi) \approx 2.399963\ \mathrm{rad}',
            r'\frac{d\beta}{d\ln\mu} = -\beta\,(\beta - \beta_0),'
            r'\qquad \beta_0 = 0.3803',
        ],
        'teoria': {
            'es': ('La helice aurea 3D visualiza la trayectoria de acoplo con paso angular '
                   'igual al angulo aureo theta_phi, lo que garantiza la maxima uniformidad '
                   'espectral del muestreo. El flujo del grupo de renormalizacion muestra que '
                   'cualquier condicion inicial converge al punto fijo beta0 = 0.3803: el '
                   'atractor aureo del modelo (Tabla 1).'),
            'en': ('The 3D golden helix visualizes the coupling trajectory with an angular step '
                   'equal to the golden angle theta_phi, ensuring maximum spectral uniformity '
                   'of the sampling. The renormalization group flow shows that any initial '
                   'condition converges to the fixed point beta0 = 0.3803: the golden attractor '
                   'of the model (Table 1).'),
            'de': ('Die 3D-Goldene Helix visualisiert die Kopplungstrajektorie mit einem '
                   'Winkelschritt gleich dem Goldenen Winkel theta_phi, was maximale spektrale '
                   'Gleichmaessigkeit der Abtastung garantiert. Der Renormierungsgruppenfluss '
                   'zeigt, dass jede Anfangsbedingung zum Fixpunkt beta0 = 0.3803 konvergiert: '
                   'dem Goldenen Attraktor des Modells (Tabelle 1).'),
        },
    },
]

# ---- Etiquetas trilingues de las tablas de estadisticas ----
LBL = {
    'tabla1': {'es': 'Tabla 1. Constantes fisicas del modelo',
               'en': 'Table 1. Physical constants of the model',
               'de': 'Tabelle 1. Physikalische Konstanten des Modells'},
    'tabla2': {'es': 'Tabla 2. Estadistica completa de los residuos',
               'en': 'Table 2. Full residual statistics',
               'de': 'Tabelle 2. Vollstaendige Residuenstatistik'},
    'tabla3': {'es': 'Tabla 3. Estadistica posterior MCMC',
               'en': 'Table 3. MCMC posterior statistics',
               'de': 'Tabelle 3. MCMC-Posterior-Statistik'},
    'simbolo': {'es': 'Simbolo', 'en': 'Symbol', 'de': 'Symbol'},
    'valor': {'es': 'Valor', 'en': 'Value', 'de': 'Wert'},
    'descripcion': {'es': 'Descripcion', 'en': 'Description', 'de': 'Beschreibung'},
    'estadistico': {'es': 'Estadistico', 'en': 'Statistic', 'de': 'Statistik'},
    'parametro': {'es': 'Parametro', 'en': 'Parameter', 'de': 'Parameter'},
    'media_std': {'es': 'Media ± sigma', 'en': 'Mean ± sigma', 'de': 'Mittel ± sigma'},
    'ic68': {'es': 'IC 68%', 'en': '68% CI', 'de': '68%-KI'},
    'ic95': {'es': 'IC 95%', 'en': '95% CI', 'de': '95%-KI'},
    'inyectado': {'es': 'Valor inyectado', 'en': 'Injected value', 'de': 'Injizierter Wert'},
    'significancia': {
        'es': 'Significancia de la torsion xi',
        'en': 'Torsion xi significance',
        'de': 'Signifikanz der Torsion xi'},
}

RESIDUAL_ROWS = [
    ('n', 'N', {'es': 'Numero de supernovas', 'en': 'Number of supernovae', 'de': 'Anzahl der Supernovae'}, '{:d}'),
    ('media', 'mean(r)', {'es': 'Media de los residuos', 'en': 'Residual mean', 'de': 'Mittelwert der Residuen'}, '{:+.5f}'),
    ('mediana', 'median(r)', {'es': 'Mediana', 'en': 'Median', 'de': 'Median'}, '{:+.5f}'),
    ('desv_est', 'sigma(r)', {'es': 'Desviacion estandar', 'en': 'Standard deviation', 'de': 'Standardabweichung'}, '{:.5f}'),
    ('error_estandar', 'SE', {'es': 'Error estandar de la media', 'en': 'Standard error of the mean', 'de': 'Standardfehler des Mittelwerts'}, '{:.5f}'),
    ('rms', 'RMS', {'es': 'Raiz cuadratica media', 'en': 'Root mean square', 'de': 'Effektivwert (RMS)'}, '{:.5f}'),
    ('asimetria', 'g1', {'es': 'Asimetria (skewness)', 'en': 'Skewness', 'de': 'Schiefe'}, '{:+.4f}'),
    ('curtosis', 'g2', {'es': 'Exceso de curtosis', 'en': 'Excess kurtosis', 'de': 'Exzess-Kurtosis'}, '{:+.4f}'),
    ('min', 'min(r)', {'es': 'Residuo minimo', 'en': 'Minimum residual', 'de': 'Minimales Residuum'}, '{:+.5f}'),
    ('max', 'max(r)', {'es': 'Residuo maximo', 'en': 'Maximum residual', 'de': 'Maximales Residuum'}, '{:+.5f}'),
    ('dagostino_k2', 'K^2', {'es': "Estadistico D'Agostino-Pearson", 'en': "D'Agostino-Pearson statistic", 'de': "D'Agostino-Pearson-Statistik"}, '{:.4f}'),
    ('dagostino_p', 'p(DA)', {'es': "p-valor D'Agostino-Pearson", 'en': "D'Agostino-Pearson p-value", 'de': "D'Agostino-Pearson p-Wert"}, '{:.4e}'),
    ('shapiro_w', 'W', {'es': 'Estadistico Shapiro-Wilk', 'en': 'Shapiro-Wilk statistic', 'de': 'Shapiro-Wilk-Statistik'}, '{:.4f}'),
    ('shapiro_p', 'p(SW)', {'es': 'p-valor Shapiro-Wilk', 'en': 'Shapiro-Wilk p-value', 'de': 'Shapiro-Wilk p-Wert'}, '{:.4e}'),
    ('anderson_A2', 'A^2', {'es': 'Estadistico Anderson-Darling', 'en': 'Anderson-Darling statistic', 'de': 'Anderson-Darling-Statistik'}, '{:.4f}'),
    ('anderson_crit_5pct', 'A^2_{5%}', {'es': 'Valor critico Anderson-Darling (5%)', 'en': 'Anderson-Darling critical value (5%)', 'de': 'Anderson-Darling kritischer Wert (5%)'}, '{:.4f}'),
    ('chi2_red', 'chi2_red', {'es': 'Chi-cuadrado reducido', 'en': 'Reduced chi-squared', 'de': 'Reduziertes Chi-Quadrat'}, '{:.4f}'),
]

CONSTANT_ROWS = [
    ('phi', r'$\varphi$', {'es': 'Razon aurea', 'en': 'Golden ratio', 'de': 'Goldener Schnitt'}, f'{phi:.10f}'),
    ('theta_phi', r'$\theta_\varphi$', {'es': 'Angulo aureo [rad]', 'en': 'Golden angle [rad]', 'de': 'Goldener Winkel [rad]'}, f'{theta_phi:.10f}'),
    ('beta0', r'$\beta_0$', {'es': 'Punto fijo del atractor RG', 'en': 'RG attractor fixed point', 'de': 'RG-Attraktor-Fixpunkt'}, f'{beta0}'),
    ('H0_ref', r'$H_0$', {'es': 'Constante de Hubble de referencia [km/s/Mpc]', 'en': 'Reference Hubble constant [km/s/Mpc]', 'de': 'Referenz-Hubble-Konstante [km/s/Mpc]'}, f'{H0_ref}'),
    ('Om_ref', r'$\Omega_m$', {'es': 'Densidad de materia de referencia', 'en': 'Reference matter density', 'de': 'Referenz-Materiedichte'}, f'{Om_ref}'),
    ('xi_shield', r'$\xi$', {'es': 'Apantallamiento de torsion', 'en': 'Torsion shielding', 'de': 'Torsionsabschirmung'}, f'{xi_shield}'),
]


# ============================================================
#  PLANTILLA HTML
# ============================================================
TEMPLATE = Template(r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas Tecnico THU-TBEA v4.1</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]});"></script>
<style>
  :root { --teal: #0f766e; --gold: #b45309; }
  body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 1000px;
         margin: 0 auto; padding: 1.5rem; color: #1f2937; line-height: 1.6; }
  h1 { border-bottom: 3px solid var(--teal); padding-bottom: .4rem; }
  h2 { color: var(--teal); margin-top: 2.5rem; border-left: 5px solid var(--gold);
       padding-left: .6rem; }
  figure { margin: 1.5rem 0; text-align: center; }
  img { max-width: 92%; border: 1px solid #d1d5db; border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,.08); }
  figcaption { margin-top: .5rem; font-style: italic; color: #4b5563; }
  .eq-box { background: #f0fdfa; border: 1px solid #99f6e4; border-radius: 8px;
            padding: .8rem 1rem; margin: 1rem 0; overflow-x: auto; }
  .theory { background: #fffbeb; border-left: 4px solid var(--gold);
            padding: .8rem 1rem; border-radius: 0 8px 8px 0; }
  table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .95rem; }
  th, td { border: 1px solid #d1d5db; padding: .45rem .7rem; text-align: left; }
  th { background: var(--teal); color: #fff; }
  tr:nth-child(even) { background: #f9fafb; }
  .tbl-cap { font-weight: 600; color: var(--teal); margin-bottom: .3rem; }
  .lang-switch { position: sticky; top: 0; background: #fff; padding: .6rem 0;
                 border-bottom: 1px solid #e5e7eb; z-index: 10; }
  .lang-switch button { margin-right: .5rem; padding: .4rem 1rem; border: 2px solid
        var(--teal); background: #fff; color: var(--teal); border-radius: 20px;
        cursor: pointer; font-weight: 600; }
  .lang-switch button.active { background: var(--teal); color: #fff; }
  .author-card { background: #ecfeff; border: 1px solid #67e8f9;
        border-radius: 8px; padding: .8rem 1.2rem; margin: 1rem 0; }
  .lang-en, .lang-de { display: none; }
  .highlight { background: #fef3c7; font-weight: 700; }
  footer { margin-top: 3rem; font-size: .85rem; color: #6b7280;
           border-top: 1px solid #e5e7eb; padding-top: .6rem; }
</style>
</head>
<body>
<div class="lang-switch">
  <button id="btn-es" class="active" onclick="setLang('es')">Espanol</button>
  <button id="btn-en" onclick="setLang('en')">English</button>
  <button id="btn-de" onclick="setLang('de')">Deutsch</button>
</div>

<h1>Atlas Tecnico &mdash; Proyecto THU-TBEA v4.1</h1>

<div class="author-card">
  <strong>
  <span class="lang-es">Investigador Independiente</span><span class="lang-en">Independent Researcher</span><span class="lang-de">Unabhaengiger Forscher</span>:
  Erick Duque</strong><br>
  ORCID: <a href="https://orcid.org/0009-0004-1245-5464</a>
  <em></em><br>
  <span class="lang-es">Correo</span><span class="lang-en">Email</span><span class="lang-de">E-Mail</span>:
  <a href="mailto:international_manager@comllcusa.com">international_manager@comllcusa.com</a><br>
  <span class="lang-es">Licencia</span><span class="lang-en">License</span><span class="lang-de">Lizenz</span>:
  <strong>MIT</strong> &middot; Copyright &copy; 2026 Erick Duque
</div>

<p>
<span class="lang-es">Comprobacion estadistica completa del analisis de torsion
espaciotemporal. Generado el {{ fecha }}. Selecciona el idioma arriba.</span>
<span class="lang-en">Full statistical verification of the spacetime torsion
analysis. Generated on {{ fecha }}. Select the language above.</span>
<span class="lang-de">Vollstaendige statistische Ueberpruefung der
Raumzeit-Torsionsanalyse. Erstellt am {{ fecha }}. Sprache oben waehlen.</span>
</p>

<h2><span class="lang-es">0. Constantes del Modelo</span><span class="lang-en">0. Model Constants</span><span class="lang-de">0. Modellkonstanten</span></h2>
{{ tabla_constantes }}

{% for s in secciones %}
<h2><span class="lang-es">{{ s.titulo.es }}</span><span class="lang-en">{{ s.titulo.en }}</span><span class="lang-de">{{ s.titulo.de }}</span></h2>

{% for fig in s.figuras_html %}
<figure>
  <img src="data:image/png;base64,{{ fig.b64 }}" alt="{{ fig.nombre }}">
  <figcaption>
    <span class="lang-es">{{ fig.desc.es }}</span>
    <span class="lang-en">{{ fig.desc.en }}</span>
    <span class="lang-de">{{ fig.desc.de }}</span>
  </figcaption>
</figure>
<div class="theory">
  <span class="lang-es">{{ s.teoria.es }}</span>
  <span class="lang-en">{{ s.teoria.en }}</span>
  <span class="lang-de">{{ s.teoria.de }}</span>
</div>
{% endfor %}

<div class="eq-box">
{% for eq in s.ecuaciones %} $$ {{ eq }} $$ {% endfor %}
</div>

{% if s.tabla_html %}{{ s.tabla_html }}{% endif %}
{% endfor %}

<footer>
<span class="lang-es">Documento consolidado para el Proyecto THU-TBEA v4.1.
Todas las estadisticas fueron generadas automaticamente por el pipeline
(run_all.py) a partir de los datos y cadenas MCMC.
&copy; 2026 Erick Duque, Investigador Independiente &mdash; Licencia MIT.</span>
<span class="lang-en">Consolidated document for the THU-TBEA v4.1 Project.
All statistics were automatically generated by the pipeline (run_all.py)
from the data and MCMC chains.
&copy; 2026 Erick Duque, Independent Researcher &mdash; MIT License.</span>
<span class="lang-de">Konsolidiertes Dokument fuer das THU-TBEA-Projekt v4.1.
Alle Statistiken wurden automatisch von der Pipeline (run_all.py) aus den
Daten und MCMC-Ketten erzeugt.
&copy; 2026 Erick Duque, Unabhaengiger Forscher &mdash; MIT-Lizenz.</span>
</footer>

<script>
function setLang(l) {
  for (const lang of ['es','en','de']) {
    document.querySelectorAll('.lang-'+lang).forEach(
      e => e.style.display = (lang === l) ? 'inline' : 'none');
    document.getElementById('btn-'+lang).classList.toggle('active', lang === l);
  }
}
</script>
</body>
</html>""")


# ============================================================
#  CONSTRUCCION DE TABLAS Y FIGURAS
# ============================================================
def tri(label_dict):
    """Envuelve una etiqueta en los tres idiomas."""
    return (f'<span class="lang-es">{label_dict["es"]}</span>'
            f'<span class="lang-en">{label_dict["en"]}</span>'
            f'<span class="lang-de">{label_dict["de"]}</span>')


def fig_b64(nombre):
    p = FIG_DIR / nombre
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode('ascii')


FIG_CAPTIONS = {
    'pantheon_scatter_plot.png': {
        'es': 'Fig. 1 - Diagrama de Hubble Pantheon+ con el modelo ajustado.',
        'en': 'Fig. 1 - Pantheon+ Hubble diagram with the fitted model.',
        'de': 'Abb. 1 - Pantheon+ Hubble-Diagramm mit angepasstem Modell.'},
    'pantheon_residuals_hist.png': {
        'es': 'Fig. 2 - Histograma de residuos con gaussiana ajustada.',
        'en': 'Fig. 2 - Residual histogram with fitted Gaussian.',
        'de': 'Abb. 2 - Residuenhistogramm mit angepasster Gausskurve.'},
    'pantheon_residuals_qq.png': {
        'es': 'Fig. 3 - QQ-plot de normalidad de los residuos.',
        'en': 'Fig. 3 - Normality QQ-plot of the residuals.',
        'de': 'Abb. 3 - Normalitaets-QQ-Plot der Residuen.'},
    'mcmc_corner_plot.png': {
        'es': 'Fig. 4 - Posterior marginal y correlaciones (corner plot).',
        'en': 'Fig. 4 - Marginal posteriors and correlations (corner plot).',
        'de': 'Abb. 4 - Marginale Posteriors und Korrelationen (Corner-Plot).'},
    'mcmc_traces.png': {
        'es': 'Fig. 5 - Trazas de la cadena MCMC (diagnostico de mezcla).',
        'en': 'Fig. 5 - MCMC chain traces (mixing diagnostic).',
        'de': 'Abb. 5 - MCMC-Kettentraces (Mischungsdiagnose).'},
    'fig_01_golden_helix.png': {
        'es': 'Fig. 6 - Helice aurea 3D con paso angular theta_phi.',
        'en': 'Fig. 6 - 3D golden helix with angular step theta_phi.',
        'de': 'Abb. 6 - 3D-Goldene Helix mit Winkelschritt theta_phi.'},
    'fig_07_rg_attractor.png': {
        'es': 'Fig. 7 - Flujo RG convergiendo al punto fijo beta0.',
        'en': 'Fig. 7 - RG flow converging to the fixed point beta0.',
        'de': 'Abb. 7 - RG-Fluss konvergiert zum Fixpunkt beta0.'},
}


def build_constants_table():
    rows = ''.join(
        f'<tr><td>{sym}</td><td><code>{val}</code></td><td>{tri(desc)}</td></tr>'
        for _, sym, desc, val in CONSTANT_ROWS)
    return (f'<p class="tbl-cap">{tri(LBL["tabla1"])}</p>'
            f'<table><thead><tr><th>{tri(LBL["simbolo"])}</th>'
            f'<th>{tri(LBL["valor"])}</th><th>{tri(LBL["descripcion"])}</th></tr>'
            f'</thead><tbody>{rows}</tbody></table>')


def build_residual_table():
    path = RESULTS / 'stats_residuals.json'
    if not path.exists():
        return '<p><em>stats_residuals.json no encontrado; ejecuta el pipeline.</em></p>'
    st = json.loads(path.read_text(encoding='utf-8'))
    rows = ''
    for key, sym, desc, fmt in RESIDUAL_ROWS:
        val = fmt.format(st[key]) if key != 'n' else fmt.format(st[key])
        rows += f'<tr><td><code>{sym}</code></td><td>{val}</td><td>{tri(desc)}</td></tr>'
    return (f'<p class="tbl-cap">{tri(LBL["tabla2"])}</p>'
            f'<table><thead><tr><th>{tri(LBL["estadistico"])}</th>'
            f'<th>{tri(LBL["valor"])}</th><th>{tri(LBL["descripcion"])}</th></tr>'
            f'</thead><tbody>{rows}</tbody></table>')


def build_mcmc_table():
    path = RESULTS / 'stats_mcmc.json'
    if not path.exists():
        return '<p><em>stats_mcmc.json no encontrado; ejecuta el pipeline.</em></p>'
    st = json.loads(path.read_text(encoding='utf-8'))
    head = (f'<tr><th>{tri(LBL["parametro"])}</th><th>{tri(LBL["media_std"])}</th>'
            f'<th>{tri(LBL["ic68"])}</th><th>{tri(LBL["ic95"])}</th>'
            f'<th>{tri(LBL["inyectado"])}</th></tr>')
    rows = ''
    for name, d in st['parametros'].items():
        rows += (f'<tr><td><code>{name}</code></td>'
                 f'<td>{d["media"]:.4f} &plusmn; {d["desv_est"]:.4f}</td>'
                 f'<td>[{d["ic68_inf"]:.4f}, {d["ic68_sup"]:.4f}]</td>'
                 f'<td>[{d["ic95_inf"]:.4f}, {d["ic95_sup"]:.4f}]</td>'
                 f'<td>{d["valor_inyectado"]:.4f}</td></tr>')
    sig = st['significancia_xi_sigma']
    rows += (f'<tr class="highlight"><td>{tri(LBL["significancia"])}</td>'
             f'<td colspan="4">{sig:.2f} &sigma;</td></tr>')
    return (f'<p class="tbl-cap">{tri(LBL["tabla3"])} '
            f'(N = {st["n_muestras"]})</p>'
            f'<table><thead>{head}</thead><tbody>{rows}</tbody></table>')


def generate():
    secciones = []
    for s in SECTIONS:
        sec = dict(s)
        sec['figuras_html'] = []
        for fname in s['figuras']:
            b64 = fig_b64(fname)
            if b64:
                sec['figuras_html'].append({
                    'nombre': fname, 'b64': b64,
                    'desc': FIG_CAPTIONS.get(fname, {'es': fname, 'en': fname, 'de': fname})})
        if s['id'] == 'residuos':
            sec['tabla_html'] = build_residual_table()
        elif s['id'] == 'mcmc':
            sec['tabla_html'] = build_mcmc_table()
        else:
            sec['tabla_html'] = ''
        secciones.append(sec)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    html = TEMPLATE.render(
        fecha=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        tabla_constantes=build_constants_table(),
        secciones=secciones,
    )
    OUT_PATH.write_text(html, encoding='utf-8')
    n_fig = sum(len(s['figuras_html']) for s in secciones)
    print(f'Atlas Tecnico trilingue generado -> {OUT_PATH} ({n_fig} figuras)')


if __name__ == '__main__':
    generate()
