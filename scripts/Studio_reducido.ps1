$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$AuditFolder = Join-Path $PSScriptRoot "Auditoria"

New-Item -ItemType Directory -Path $AuditFolder -Force | Out-Null

$OutputFile = Join-Path $AuditFolder "Studio_reducido.txt"

if (-not (Test-Path (Join-Path $ProjectRoot "main.py"))) {
    throw "No se ha encontrado main.py: $ProjectRoot"
}

if (-not (Test-Path (Join-Path $ProjectRoot ".git"))) {
    throw "No se ha encontrado .git: $ProjectRoot"
}

function Invoke-GitSafe {
    param([string[]]$Arguments)

    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "git.exe"
        $psi.WorkingDirectory = $ProjectRoot
        $psi.UseShellExecute = $false
        $psi.CreateNoWindow = $true
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
        $psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8
        $psi.Arguments = ($Arguments | ForEach-Object {
            '"' + ($_ -replace '"','\"') + '"'
        }) -join " "

        $p = New-Object System.Diagnostics.Process
        $p.StartInfo = $psi
        [void]$p.Start()

        $stdout = $p.StandardOutput.ReadToEnd()
        $stderr = $p.StandardError.ReadToEnd()

        $p.WaitForExit()

        if ($p.ExitCode -ne 0) {
            return "[Dato Git no disponible]"
        }

        return $stdout.Trim()
    }
    catch {
        return "[Dato Git no disponible]"
    }
}

function Get-SafeFiles {
    $excluded = @(
        ".git",".venv","venv","env","node_modules",
        "__pycache__",".pytest_cache",".mypy_cache",".ruff_cache",
        "build","dist","coverage",".coverage","logs","cache",
        ".idea",".vscode"
    )

    Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File -Force |
        Where-Object {
            $relative = $_.FullName.Substring($ProjectRoot.Length).TrimStart('\')
            $parts = $relative -split '[\\/]'
            -not ($parts | Where-Object { $excluded -contains $_ })
        } |
        ForEach-Object {
            $_.FullName.Substring($ProjectRoot.Length).TrimStart('\')
        } |
        Sort-Object
}

$branch = Invoke-GitSafe @("rev-parse","--abbrev-ref","HEAD")
$status = Invoke-GitSafe @("status","--short")

$commits = Invoke-GitSafe @(
    "-c","i18n.logOutputEncoding=UTF-8",
    "log","-8","--oneline","--decorate"
)

$version = Invoke-GitSafe @(
    "-c","i18n.logOutputEncoding=UTF-8",
    "describe","--tags","--always","--dirty"
)

$files = Get-SafeFiles
$structure = ($files | Select-Object -First 300) -join "`r`n"

if ($files.Count -gt 300) {
    $structure += "`r`n... [estructura limitada a 300 archivos]"
}

$content = @"
KG TRACKER - CONTEXTO STUDIO REDUCIDO
=====================================

Generado:
$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

OBJETIVO
--------
KG Tracker es una aplicacion nativa Windows para agregar, filtrar y notificar ofertas de juegos gratuitos para PC.

STACK
-----
- Python 3.14+
- PySide6 / Qt 6
- Windows
- VS Code + PowerShell
- Git/GitHub

REGLAS DE TRABAJO PARA GEMINI
-----------------------------
- No modificar ni borrar archivos sin autorizacion explicita.
- No ejecutar acciones destructivas.
- Antes de modificar codigo: analizar causa, impacto, riesgos y validacion.
- Las auditorias anteriores son hipotesis hasta verificarlas.
- Priorizar seguridad, estabilidad, rendimiento y mantenibilidad.
- No inventar resultados.
- Separar diagnostico, propuesta, cambio y validacion.

ESTADO GIT
----------
Rama:
$branch

Version/tag:
$version

Cambios sin commit:
$status

ULTIMOS COMMITS
---------------
$commits

ESTRUCTURA DEL PROYECTO
-----------------------
$structure

CONTEXTO DE TRABAJO
-------------------
Se utilizan dos contextos para Google AI Studio:
Studio Reducido: Contexto habitual sintetizado.
Studio Completo: Contexto tecnico con codigo fuente para auditorias.

DIRECTRICES OBLIGATORIAS DE ENTREGA (REGLA MAESTRA)
----------------------------------------------------
1. CONVENCION DE COMMITS GIT:
   - Todo commit DEBE seguir estrictamente el formato de versiones de la app:
     "v0.1.XX: <descripcion clara y profesional en espanol>"
     Ejemplo: "v0.1.38: microinteraccion de ahorro flotante al reclamar y feedback instantaneo"

2. ENTORNO DE TERMINAL Y COMANDOS:
   - TODO comando, bloque de instalacion, ejecucion de scripts o pruebas unitarias DEBE entregarse SIEMPRE y de forma exclusiva en sintaxis nativa de Windows PowerShell.

FIN DEL CONTEXTO
================
"@

$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)

if ($bytes.Length -gt 120KB) {
    throw "SEGURIDAD: Studio Reducido supera 120 KB."
}

$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($OutputFile,$content,$utf8)

Write-Host "OK - Studio Reducido generado." -ForegroundColor Green
Write-Host "Archivo: $OutputFile"
Write-Host ("Tamano: {0:N0} bytes" -f (Get-Item $OutputFile).Length)