# =============================================================
#  Instalar_THU-TBEA.ps1
#  Configura y ejecuta el proyecto THU-TBEA v4.1 en Windows
#  Uso (PowerShell, dentro de la carpeta THU-TBEA_v4.1):
#     powershell -ExecutionPolicy Bypass -File .\Instalar_THU-TBEA.ps1
# =============================================================
#Requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

Write-Host '==================================================' -ForegroundColor Cyan
Write-Host '  Proyecto THU-TBEA v4.1 - Instalacion local' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan

# --- 1. Verificar Python -------------------------------------------------
Write-Host "`n[1/4] Verificando Python..." -ForegroundColor Yellow
$python = $null
foreach ($cmd in @('python', 'py')) {
    try {
        $ver = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) { $python = $cmd; break }
    } catch { }
}
if (-not $python) {
    Write-Host 'ERROR: Python no encontrado.' -ForegroundColor Red
    Write-Host 'Descargalo de https://www.python.org/downloads/ y marca "Add Python to PATH".' -ForegroundColor Red
    exit 1
}
Write-Host "  Encontrado: $ver" -ForegroundColor Green

# --- 2. Crear entorno virtual -------------------------------------------
Write-Host "`n[2/4] Creando entorno virtual (.venv)..." -ForegroundColor Yellow
if (-not (Test-Path '.venv')) {
    & $python -m venv .venv
}
$py = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $py -m pip install --upgrade pip | Out-Null

# --- 3. Instalar dependencias -------------------------------------------
Write-Host "`n[3/4] Instalando dependencias (requirements.txt)..." -ForegroundColor Yellow
& $py -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host 'ERROR instalando dependencias.' -ForegroundColor Red
    exit 1
}

# --- 4. Ejecutar pipeline completo ---------------------------------------
Write-Host "`n[4/4] Ejecutando pipeline del LabBook..." -ForegroundColor Yellow
& $py run_all.py
if ($LASTEXITCODE -ne 0) {
    Write-Host 'ERROR durante la ejecucion del pipeline.' -ForegroundColor Red
    exit 1
}

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host '  LISTO. Resultados generados:' -ForegroundColor Green
Write-Host '   - data/raw/PantheonPlus.dat'
Write-Host '   - figures/pantheon_residuals_hist.png'
Write-Host '   - results/mcmc_torsion_samples.dat'
Write-Host '   - labbook/Atlas_Tecnico_THU-TBEA.html'
Write-Host '==================================================' -ForegroundColor Cyan

# Abrir el Atlas en el navegador predeterminado
$atlas = Join-Path $PSScriptRoot 'labbook\Atlas_Tecnico_THU-TBEA.html'
if (Test-Path $atlas) { Start-Process $atlas }
