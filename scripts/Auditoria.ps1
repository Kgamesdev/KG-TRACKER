# KG TRACKER — AUDITORÍA
# Este script realiza una auditoría estática y de solo lectura.
# NO modifica el código, NO instala dependencias, NO ejecuta la aplicación,
# NO hace commits, NO hace push y NO borra archivos.

$ErrorActionPreference = "Stop"

$Root = "F:\KURIGAMESDEV\KG TRACKER"
$Scripts = Join-Path $Root "scripts"
$Output = Join-Path $Scripts "Auditoria.txt"
$Prompt = Join-Path $Scripts "PromptMaestro.txt"

Set-Location $Root
New-Item -ItemType Directory -Path $Scripts -Force | Out-Null

function Add-Section {
    param(
        [string]$Title,
        [string]$Content
    )

    Add-Content -Path $Output -Value ""
    Add-Content -Path $Output -Value ("=" * 90)
    Add-Content -Path $Output -Value $Title
    Add-Content -Path $Output -Value ("=" * 90)
    Add-Content -Path $Output -Value $Content
}

@"
KG TRACKER — AUDITORÍA
Fecha: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Ruta: $Root

AUDITORÍA ESTÁTICA — SOLO LECTURA

Este informe recopila evidencias del estado actual del proyecto.
Las coincidencias encontradas no son automáticamente bugs.
Deben verificarse antes de clasificarlas o modificar código.

"@ | Set-Content -Path $Output -Encoding UTF8

Add-Section "ENTORNO" @"
PowerShell:
$($PSVersionTable | Out-String)

Python:
$(try { python --version 2>&1 | Out-String } catch { "No disponible" })

Node:
$(try { node --version 2>&1 | Out-String } catch { "No disponible" })

Gemini:
$(try { gemini --version 2>&1 | Out-String } catch { "No disponible" })
"@

Add-Section "GIT" @"
ESTADO:
$(git status --short --branch 2>&1 | Out-String)

VERSIÓN:
$(git describe --tags --always --dirty 2>&1 | Out-String)

HISTORIAL:
$(git log -15 --oneline --decorate 2>&1 | Out-String)
"@

Add-Section "ESTRUCTURA DEL PROYECTO" @"
$(Get-ChildItem -Recurse -File |
    Where-Object {
        $_.FullName -notmatch '\\(\.git|\.venv|venv|__pycache__|node_modules)\\'
    } |
    ForEach-Object {
        $_.FullName.Substring($Root.Length).TrimStart('\')
    } |
    Sort-Object | Out-String)
"@

$pyFiles = @(Get-ChildItem -Path $Root -Recurse -File -Filter "*.py" |
    Where-Object {
        $_.FullName -notmatch '\\(\.git|\.venv|venv|__pycache__|node_modules)\\'
    })

$totalLines = 0
foreach ($f in $pyFiles) {
    $totalLines += @(Get-Content $f.FullName -ErrorAction SilentlyContinue).Count
}

Add-Section "PYTHON — INVENTARIO" @"
Archivos Python: $($pyFiles.Count)
Líneas aproximadas: $totalLines
"@

$importLines = foreach ($f in $pyFiles) {
    $matches = Select-String -Path $f.FullName -Pattern '^\s*(from|import)\s+' -ErrorAction SilentlyContinue
    foreach ($m in $matches) {
        $rel = $f.FullName.Substring($Root.Length).TrimStart('\')
        "{0}:{1}: {2}" -f $rel, $m.LineNumber, $m.Line.Trim()
    }
}

Add-Section "IMPORTS" (($importLines | Out-String))

$patterns = [ordered]@{
    "CONCURRENCIA" = 'thread|Thread|QThread|QRunnable|QThreadPool|ThreadPoolExecutor|asyncio|async def|Lock|RLock|Semaphore|Queue|concurrent\.futures'
    "RED / HTTP" = 'requests|httpx|urllib|aiohttp|Session\(|timeout\s*=|retry|backoff'
    "ALMACENAMIENTO" = 'open\(|json\.dump|json\.load|write_text|write_bytes|os\.replace|fsync|\.tmp|\.bak'
    "SUBPROCESS / SHELL" = 'subprocess|Popen|shell\s*=\s*True|powershell|pwsh|os\.system'
    "UI / QT" = 'QTimer|QVariantAnimation|QPropertyAnimation|QParallelAnimationGroup|QSequentialAnimationGroup|paintEvent|eventFilter|setStyleSheet|Signal|Slot'
    "ERRORES / LOGGING" = 'except\s*:|except\s+Exception|print\(|logger\.|logging\.|traceback'
    "SEGURIDAD" = 'eval\(|exec\(|pickle|shell\s*=\s*True|password|passwd|token|api[_-]?key|secret'
    "PENDIENTES / DEUDA" = 'TODO|FIXME|HACK|XXX|monkey|global\s+'
}

foreach ($item in $patterns.GetEnumerator()) {
    $found = foreach ($f in $pyFiles) {
        $matches = Select-String -Path $f.FullName -Pattern $item.Value -AllMatches -ErrorAction SilentlyContinue
        foreach ($m in $matches) {
            $rel = $f.FullName.Substring($Root.Length).TrimStart('\')
            "{0}:{1}: {2}" -f $rel, $m.LineNumber, $m.Line.Trim()
        }
    }

    Add-Section $item.Key (($found | Out-String))
}

$requirements = if (Test-Path "$Root\requirements.txt") {
    Get-Content "$Root\requirements.txt" -Raw
} else {
    "No existe requirements.txt"
}

$package = if (Test-Path "$Root\package.json") {
    Get-Content "$Root\package.json" -Raw
} else {
    "No existe package.json"
}

$config = if (Test-Path "$Root\config.py") {
    Get-Content "$Root\config.py" -Raw
} else {
    "No existe config.py"
}

Add-Section "DEPENDENCIAS Y CONFIGURACIÓN" @"
--- requirements.txt ---
$requirements

--- package.json ---
$package

--- config.py ---
$config
"@

$tests = @(Get-ChildItem -Path "$Root\tests" -Recurse -File -ErrorAction SilentlyContinue)

$testContent = foreach ($t in $tests) {
    "--- $($t.FullName.Substring($Root.Length).TrimStart('\')) ---"
    Get-Content $t.FullName -ErrorAction SilentlyContinue
}

Add-Section "TESTS" @"
Archivos de test: $($tests.Count)

$($testContent | Out-String)
"@

$readme = if (Test-Path "$Root\README.md") {
    Get-Content "$Root\README.md" -Raw
} else { "No existe README.md" }

$license = if (Test-Path "$Root\LICENSE") {
    Get-Content "$Root\LICENSE" -Raw
} else { "No existe LICENSE" }

$changelog = if (Test-Path "$Root\CHANGELOG.md") {
    Get-Content "$Root\CHANGELOG.md" -TotalCount 500 | Out-String
} else { "No existe CHANGELOG.md" }

Add-Section "DOCUMENTACIÓN" @"
--- README.md ---
$readme

--- LICENSE ---
$license

--- CHANGELOG.md ---
$changelog
"@

Add-Section "RESUMEN" @"
Archivos Python: $($pyFiles.Count)
Líneas Python aproximadas: $totalLines
Archivos de tests: $($tests.Count)

IMPORTANTE:
Esta es una auditoría estática.
Las coincidencias deben revisarse en contexto.
No se ha ejecutado KG Tracker.
No se ha modificado el código.
No se ha hecho commit.
No se ha hecho push.
"@

if (Test-Path $Prompt) {
    Add-Section "PROMPT MAESTRO" (Get-Content $Prompt -Raw -Encoding UTF8)
}
else {
    Add-Section "PROMPT MAESTRO" "AVISO: No existe scripts\PromptMaestro.txt"
}

$info = Get-Item $Output

Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host " AUDITORÍA TERMINADA" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host "Archivo: $($info.FullName)"
Write-Host ("Tamaño: {0:N0} bytes" -f $info.Length)
Write-Host ""
Write-Host "No se ha modificado el código de KG Tracker." -ForegroundColor Green
Write-Host "No se ha hecho commit ni push." -ForegroundColor Green
