$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$AuditFolder = Join-Path $PSScriptRoot "Auditoria"

New-Item -ItemType Directory -Path $AuditFolder -Force | Out-Null

$OutputFile = Join-Path $AuditFolder "Studio_completo.txt"

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
            [PSCustomObject]@{
                FullPath = $_.FullName
                Relative = $_.FullName.Substring($ProjectRoot.Length).TrimStart('\')
                Length = $_.Length
            }
        } |
        Sort-Object Relative
}

$branch = Invoke-GitSafe @("rev-parse","--abbrev-ref","HEAD")
$status = Invoke-GitSafe @("status","--short")

$commits = Invoke-GitSafe @(
    "-c","i18n.logOutputEncoding=UTF-8",
    "log","-12","--oneline","--decorate"
)

$version = Invoke-GitSafe @(
    "-c","i18n.logOutputEncoding=UTF-8",
    "describe","--tags","--always","--dirty"
)

$allFiles = Get-SafeFiles

$allowedExtensions = @(
    ".py",".md",".txt",".json",".toml",".ini",".cfg",
    ".yml",".yaml",".ps1",".bat",".cmd"
)

$priorityRoots = @("core","ui","tests","scripts")

$priorityRootFiles = @(
    "main.py","config.py","logger.py","requirements.txt",
    "README.md","CHANGELOG.md","LICENSE","CONTEXTO_PROYECTO.md"
)

$candidates = $allFiles | Where-Object {
    $ext = [IO.Path]::GetExtension($_.Relative).ToLowerInvariant()
    $firstPart = ($_.Relative -split '[\\/]')[0]

    ($allowedExtensions -contains $ext) -and (
        ($priorityRoots -contains $firstPart) -or
        ($priorityRootFiles -contains $_.Relative)
    )
}

$maxTotalBytes = 2MB
$maxFileBytes = 160KB
$maxFiles = 70

$selected = New-Object System.Collections.Generic.List[object]
$totalBytes = 0

$ordered = $candidates | Sort-Object `
    @{Expression={
        $first = ($_.Relative -split '[\\/]')[0]
        if ($priorityRoots -contains $first) { 0 }
        elseif ($priorityRootFiles -contains $_.Relative) { 1 }
        else { 2 }
    }}, Relative

foreach ($file in $ordered) {

    if ($selected.Count -ge $maxFiles) {
        break
    }

    if ($file.Length -gt $maxFileBytes) {
        continue
    }

    if (($totalBytes + $file.Length) -gt $maxTotalBytes) {
        break
    }

    $selected.Add($file)
    $totalBytes += $file.Length
}

$selectedPaths = @($selected | ForEach-Object { $_.Relative })

$skipped = @(
    $candidates | Where-Object {
        $selectedPaths -notcontains $_.Relative
    }
)

$builder = New-Object System.Text.StringBuilder

[void]$builder.AppendLine("KG TRACKER - CONTEXTO STUDIO COMPLETO")
[void]$builder.AppendLine("=====================================")
[void]$builder.AppendLine()
[void]$builder.AppendLine("Generado: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$builder.AppendLine()

[void]$builder.AppendLine("OBJETIVO")
[void]$builder.AppendLine("KG Tracker es una aplicacion nativa Windows para agregar, filtrar y notificar ofertas de juegos gratuitos para PC.")
[void]$builder.AppendLine()

[void]$builder.AppendLine("STACK")
[void]$builder.AppendLine("- Python 3.14+")
[void]$builder.AppendLine("- PySide6 / Qt 6")
[void]$builder.AppendLine("- Windows")
[void]$builder.AppendLine("- VS Code + PowerShell")
[void]$builder.AppendLine("- Git/GitHub")
[void]$builder.AppendLine()

[void]$builder.AppendLine("REGLAS PARA GEMINI")
[void]$builder.AppendLine("- No modificar ni borrar archivos sin autorizacion explicita.")
[void]$builder.AppendLine("- No ejecutar acciones destructivas.")
[void]$builder.AppendLine("- Antes de modificar codigo: explicar causa, impacto, riesgo y validacion.")
[void]$builder.AppendLine("- Verificar las auditorias anteriores contra el codigo actual.")
[void]$builder.AppendLine("- No asumir que una dependencia o funcion es innecesaria sin comprobar referencias.")
[void]$builder.AppendLine()

[void]$builder.AppendLine("ESTADO GIT")
[void]$builder.AppendLine("Rama: $branch")
[void]$builder.AppendLine("Version/tag: $version")
[void]$builder.AppendLine()
[void]$builder.AppendLine("Cambios sin commit:")
[void]$builder.AppendLine($status)
[void]$builder.AppendLine()
[void]$builder.AppendLine("ULTIMOS COMMITS")
[void]$builder.AppendLine($commits)
[void]$builder.AppendLine()

[void]$builder.AppendLine("ARCHIVOS INCLUIDOS")

foreach ($file in $selected) {
    [void]$builder.AppendLine(
        "- $($file.Relative) [$($file.Length) bytes]"
    )
}

[void]$builder.AppendLine()
[void]$builder.AppendLine("ARCHIVOS OMITIDOS POR LOS LIMITES")

foreach ($file in ($skipped | Select-Object -First 120)) {
    [void]$builder.AppendLine(
        "- $($file.Relative) [$($file.Length) bytes]"
    )
}

[void]$builder.AppendLine()
[void]$builder.AppendLine("AUDITORIA ANTERIOR - HIPOTESIS A VERIFICAR")
[void]$builder.AppendLine("- cache/thread-safety")
[void]$builder.AppendLine("- construccion de comandos en audio")
[void]$builder.AppendLine("- escritura no atomica de reclamados.json")
[void]$builder.AppendLine("- duplicacion de metodos de idioma")
[void]$builder.AppendLine("- monkey-patching instalar_metodos(cls)")
[void]$builder.AppendLine("- requests.Session compartida")
[void]$builder.AppendLine("- parsing HTML de Itch.io")
[void]$builder.AppendLine("- recreacion de GameCard")
[void]$builder.AppendLine("- animacion de RoundedButton")
[void]$builder.AppendLine("- print frente a logger")
[void]$builder.AppendLine("- discrepancia README/LICENSE")
[void]$builder.AppendLine("- cobertura de tests baja")
[void]$builder.AppendLine("- posibles dependencias residuales")
[void]$builder.AppendLine("Ningun punto anterior es un bug confirmado sin verificar el codigo actual.")
[void]$builder.AppendLine()

foreach ($file in $selected) {

    [void]$builder.AppendLine(("=" * 90))
    [void]$builder.AppendLine("FILE: $($file.Relative)")
    [void]$builder.AppendLine(("=" * 90))

    try {
        $text = [IO.File]::ReadAllText(
            $file.FullPath,
            [Text.Encoding]::UTF8
        )

        [void]$builder.AppendLine($text)
    }
    catch {
        [void]$builder.AppendLine(
            "[No se pudo leer este archivo]"
        )
    }

    [void]$builder.AppendLine()
}

$content = $builder.ToString()
$bytes = [Text.Encoding]::UTF8.GetBytes($content)

if ($bytes.Length -gt $maxTotalBytes) {
    throw "SEGURIDAD: Studio Completo supera el limite de 2 MB."
}

$utf8 = New-Object System.Text.UTF8Encoding($false)

[IO.File]::WriteAllText(
    $OutputFile,
    $content,
    $utf8
)

Write-Host "OK - Studio Completo generado."
Write-Host "Archivo: $OutputFile"
Write-Host ("Tamano: {0:N0} bytes" -f (Get-Item $OutputFile).Length)
Write-Host ("Archivos incluidos: {0}" -f $selected.Count)
Write-Host ("Archivos omitidos: {0}" -f $skipped.Count)