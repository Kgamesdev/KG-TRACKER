# Script para generar un dossier de contexto del proyecto KG Tracker
$outputFile = "CONTEXTO_PROYECTO.md"
$mainEntryPoint = "main.py"
$requirementsFile = "requirements.txt"
$foldersToExclude = @("__pycache__", ".venv", ".git", "node_modules", "cache", "logs", ".vscode")
Write-Host "Generando dossier de contexto actualizado en '$outputFile'..." -ForegroundColor Cyan
Set-Content -Path $outputFile -Value "# CONTEXTO DEL PROYECTO: KG TRACKER (Clean Architecture)"
Add-Content -Path $outputFile -Value "`n## 1. Estructura de Archivos`n"
Add-Content -Path $outputFile -Value "```text"
Get-ChildItem -Recurse -Exclude $foldersToExclude | Where-Object {
    $path = $_.FullName
    -not ($path -match '\\__pycache__\\|\\\.venv\\|\\\.git\\|\\node_modules\\|\\cache\\|\\logs\\')
} | ForEach-Object {
    $depth = $_.FullName.Split('\' ).Count - (Get-Location).Path.Split('\' ).Count
    $indent = "  " * $depth
    $isDir = if ($_.PSIsContainer) { "/" } else { "" }
    "$indent- $($_.Name)$isDir"
} | Add-Content -Path $outputFile
Add-Content -Path $outputFile -Value "```"
if (Test-Path $requirementsFile) {
    Add-Content -Path $outputFile -Value "`n## 2. Dependencias (requirements.txt)`n"
    Add-Content -Path $outputFile -Value "```"
    Get-Content $requirementsFile | Add-Content -Path $outputFile
    Add-Content -Path $outputFile -Value "```"
}
if (Test-Path $mainEntryPoint) {
    Add-Content -Path $outputFile -Value "`n## 3. Punto de Entrada (main.py)`n"
    Add-Content -Path $outputFile -Value "```python"
    Get-Content $mainEntryPoint | Add-Content -Path $outputFile
    Add-Content -Path $outputFile -Value "```"
}
Write-Host "Dossier de contexto actualizado con éxito en la raíz." -ForegroundColor Cyan
