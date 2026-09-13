$outputFile = "..\project-context.txt"
$rootPath = "F:\KURIGAMESDEV\KG TRACKER"

$allowedExtensions = @(".ts", ".tsx", ".js", ".jsx", ".json", ".env.example", ".md", ".ps1")
$excludedDirs = @("node_modules", ".git", "dist", "build", ".next", "coverage")

Write-Host "🔍 Analizando el proyecto en: $rootPath" -ForegroundColor Cyan

"=== ESTRUCTURA DEL PROYECTO ===" | Out-File -FilePath $outputFile -Encoding utf8
Get-ChildItem -Path $rootPath -Recurse | Where-Object {
    $item = $_
    $skip = $false
    foreach ($dir in $excludedDirs) {
        if ($item.FullName -like "*\$dir\*") { $skip = $true }
    }
    -not $skip
} | ForEach-Object {
    $indent = "  " * ($_.FullName.Replace($rootPath, "").Split("\").Count - 1)
    "$indent$($_.Name)"
} | Out-File -FilePath $outputFile -Append -Encoding utf8

"`n`n=== CONTENIDO DE ARCHIVOS ===" | Out-File -FilePath $outputFile -Append -Encoding utf8

Get-ChildItem -Path $rootPath -Recurse -File | Where-Object {
    $file = $_
    $skip = $false
    foreach ($dir in $excludedDirs) {
        if ($file.FullName -like "*\$dir\*") { $skip = $true }
    }
    if ($allowedExtensions -contains $file.Extension -and -not $skip) {
        $true
    } else {
        $false
    }
} | ForEach-Object {
    $relativePath = $_.FullName.Replace($rootPath, "")
    "`n--- ARCHIVO: $relativePath ---`n" | Out-File -FilePath $outputFile -Append -Encoding utf8
    Get-Content -Path $_.FullName -Raw | Out-File -FilePath $outputFile -Append -Encoding utf8
}

Write-Host "✅ Contexto generado correctamente en: $outputFile" -ForegroundColor Green
