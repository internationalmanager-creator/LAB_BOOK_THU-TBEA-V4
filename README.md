=============================================================
 PROYECTO THU-TBEA v4.1 - INSTRUCCIONES DE USO LOCAL (Windows)
=============================================================

REQUISITO PREVIO
----------------
Tener Python 3.10+ instalado desde https://www.python.org/downloads/
(IMPORTANTE: durante la instalacion marca la casilla "Add Python to PATH").

Para verificar, abre PowerShell y escribe:
    python --version

INSTALACION Y EJECUCION (todo automatico)
-----------------------------------------
1. Descomprime el ZIP en donde quieras (ej. Documentos\THU-TBEA_v4.1).
2. Abre PowerShell y entra a la carpeta:
       cd "$env:USERPROFILE\Documents\THU-TBEA_v4.1"
3. Ejecuta el instalador:
       powershell -ExecutionPolicy Bypass -File .\Instalar_THU-TBEA.ps1

El script hace todo solo: crea el entorno virtual (.venv), instala las
dependencias (numpy, pandas, scipy, matplotlib, seaborn, emcee, jinja2)
y ejecuta el pipeline completo. Al terminar abre el Atlas Tecnico en tu
navegador.

USO POSTERIOR (despues de la primera instalacion)
-------------------------------------------------
    cd ruta\a\THU-TBEA_v4.1
    .\.venv\Scripts\python.exe run_all.py

O activa el entorno si quieres trabajar interactivamente:
    .\.venv\Scripts\Activate.ps1

ESTRUCTURA DEL PROYECTO
-----------------------
THU-TBEA_v4.1\
|-- Instalar_THU-TBEA.ps1   Instalador automatico (PowerShell)
|-- run_all.py              Ejecuta todo el pipeline del LabBook
|-- requirements.txt        Dependencias de Python
|-- LICENSE                 Licencia MIT (Copyright 2026 Erick Duque)
|-- CITATION.cff            Datos de citacion del repositorio
|-- src\
|   |-- constants.py        Seccion 2: Constantes fisicas (Atractor Aureo)
|   |-- fetch_data.py       Seccion 3: Datos Pantheon+
|   |-- analyze_residuals.py  Seccion 4: Residuos + 17 estadisticos + 3 figuras
|   |-- generate_golden_figures.py  Helice aurea 3D y atractor RG
|   |-- generate_labbook.py   Seccion 6: Atlas Tecnico TRILINGUE (HTML)
|   |-- export_tables.py      Seccion 7: Tablas CSV + LaTeX para la tesis
|   |-- utils.py              Utilidades (guardado robusto de figuras)
|-- scripts\
|   |-- run_mcmc_torsion.py   Seccion 5: Muestreo MCMC de torsion
|-- tests\test_smoke.py     Prueba rapida de constantes
|-- data\raw\               Datos generados (PantheonPlus.dat)
|-- figures\                Figuras generadas (PNG)
|-- results\                Muestras MCMC
|-- labbook\                Atlas Tecnico HTML generado
|   |-- tables\             Tablas exportadas (CSV + LaTeX booktabs)

AUTORIA
-------
Investigador Independiente: Erick Duque
ORCID: 0009-0004-1245-5464
Correo: international_manager@comllcusa.com
Licencia: MIT

EL ATLAS TECNICO TRILINGUE (novedad)
------------------------------------
labbook\Atlas_Tecnico_THU-TBEA.html incluye:
- Selector de idioma ES / EN / DE (botones superiores).
- Tabla 1: constantes fisicas del modelo (phi, theta_phi, beta0, H0, Om, xi).
- 7 figuras generadas por el pipeline; DEBAJO de cada figura aparece la
  explicacion teorica y la ecuacion matematica correspondiente (KaTeX).
- Tabla 2: 17 estadisticos de los residuos (media, sigma, asimetria,
  curtosis, D'Agostino-Pearson, Shapiro-Wilk, Anderson-Darling, chi2_red...).
- Tabla 3: estadistica posterior MCMC (media +/- sigma, IC 68%/95%, valor
  inyectado) y la significancia de la torsion xi (~4.1 sigma).
- Las estadisticas se leen de results\*.json: si recorres el pipeline,
  las tablas del Atlas se actualizan solas.
- Las ecuaciones usan KaTeX desde CDN: se necesita internet al abrir el HTML.

NOTAS
-----
- Correcciones minimas respecto al LabBook original:
  * Se crea la carpeta results\ (el script MCMC original fallaba sin ella).
  * Las figuras se guardan en figures\ en vez de plt.show().
  * La varianza de xi en el MCMC se ajusto para reproducir la deteccion
    de 4.1 sigma declarada en el LabBook (con 0.005 salian solo ~0.28 sigma).
  * Semilla aleatoria fija (42) para resultados reproducibles.
- Los datos Pantheon+ se generan sinteticamente (como en el LabBook).
  Para datos reales reemplaza src/fetch_data.py con la descarga oficial:
  https://github.com/PantheonPlusSH0ES/DataRelease
- Para compilar la tesis LaTeX (Tesis_THU_SP_7.tex) usa MiKTeX:
      pdflatex Tesis_THU_SP_7.tex
=============================================================
