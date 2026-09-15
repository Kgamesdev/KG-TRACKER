# KG TRACKER - COMPLETE TECHNICAL AUDIT
# ASCII-only PowerShell script.
# Safe audit: does not modify project source code.
# Run from project root or from this scripts folder.

$ErrorActionPreference = "Continue"

function Find-ProjectRoot {
    param([string]$StartPath)

    $current = (Resolve-Path $StartPath).Path

    while ($true) {
        if (Test-Path (Join-Path $current "main.py")) {
            return $current
        }

        $parent = Split-Path $current -Parent
        if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $current) {
            return $null
        }

        $current = $parent
    }
}

$ProjectRoot = Find-ProjectRoot (Get-Location)

if (-not $ProjectRoot) {
    Write-Host "ERROR: Could not find project root (main.py)." -ForegroundColor Red
    Write-Host "Run this script from the KG TRACKER project or its scripts folder."
    exit 1
}

$AuditDir = Join-Path $ProjectRoot "_audit"
New-Item -ItemType Directory -Path $AuditDir -Force | Out-Null

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ReportPath = Join-Path $AuditDir "AUDITORIA_KG_TRACKER_$Stamp.md"

function Add-Section {
    param([string]$Title)
    Add-Content -Path $ReportPath -Value ""
    Add-Content -Path $ReportPath -Value "## $Title"
    Add-Content -Path $ReportPath -Value ""
}

function Add-CommandResult {
    param(
        [string]$Title,
        [string]$Command
    )

    Add-Content -Path $ReportPath -Value "### $Title"
    Add-Content -Path $ReportPath -Value ""
    Add-Content -Path $ReportPath -Value '```text'

    try {
        $result = Invoke-Expression $Command 2>&1 | Out-String
        if ([string]::IsNullOrWhiteSpace($result)) {
            $result = "[No output]"
        }
        Add-Content -Path $ReportPath -Value $result.TrimEnd()
    }
    catch {
        Add-Content -Path $ReportPath -Value ("ERROR: " + $_.Exception.Message)
    }

    Add-Content -Path $ReportPath -Value '```'
    Add-Content -Path $ReportPath -Value ""
}

"# KG TRACKER - COMPLETE TECHNICAL AUDIT" | Set-Content $ReportPath -Encoding UTF8
Add-Content $ReportPath "Technical snapshot generated automatically. This is not a release verdict."
Add-Content $ReportPath "This script does not modify project source code."
Add-Content $ReportPath ""
Add-Content $ReportPath ("Project root: " + $ProjectRoot)
Add-Content $ReportPath ("Audit date: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Add-Content $ReportPath ""

Add-Section "1. Git status and history"

Add-CommandResult "Git status" "git -C `"$ProjectRoot`" status --short --branch"
Add-CommandResult "Recent commits" "git -C `"$ProjectRoot`" log --oneline --decorate -12"
Add-CommandResult "Tags" "git -C `"$ProjectRoot`" tag --sort=-creatordate | Select-Object -First 20"
Add-CommandResult "Recent diff statistics" "git -C `"$ProjectRoot`" diff --stat"

Add-Section "2. Project structure"

Add-CommandResult "Top-level files and folders" "Get-ChildItem -LiteralPath `"$ProjectRoot`" -Force | Select-Object Mode,Length,LastWriteTime,Name | Format-Table -AutoSize"
Add-CommandResult "Python files" "Get-ChildItem -LiteralPath `"$ProjectRoot`" -Recurse -File -Filter *.py | Where-Object { `$_.FullName -notmatch '\\node_modules\\|\\\.git\\|\\_audit\\' } | ForEach-Object { `$_.FullName.Substring(`"$ProjectRoot`".Length + 1) } | Sort-Object"

Add-Section "3. File inventory"

Add-CommandResult "Extension counts" "Get-ChildItem -LiteralPath `"$ProjectRoot`" -Recurse -File | Where-Object { `$_.FullName -notmatch '\\\.git\\|\\node_modules\\|\\_audit\\' } | Group-Object Extension | Sort-Object Count -Descending | Select-Object Count,Name | Format-Table -AutoSize"

Add-CommandResult "Largest project files" "Get-ChildItem -LiteralPath `"$ProjectRoot`" -Recurse -File | Where-Object { `$_.FullName -notmatch '\\\.git\\|\\node_modules\\|\\_audit\\' } | Sort-Object Length -Descending | Select-Object -First 40 @{N='MB';E={[math]::Round(`$_.Length / 1MB,2)}},FullName | Format-Table -AutoSize"

Add-Section "4. Python metrics"

$PythonFiles = Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File -Filter *.py |
    Where-Object { $_.FullName -notmatch '\\node_modules\\|\\.git\\|\\_audit\\' }

$TotalPythonLines = 0
$PythonMetrics = @()

foreach ($file in $PythonFiles) {
    try {
        $lines = (Get-Content -LiteralPath $file.FullName -ErrorAction Stop).Count
        $TotalPythonLines += $lines
        $PythonMetrics += [PSCustomObject]@{
            Lines = $lines
            File  = $file.FullName.Substring($ProjectRoot.Length + 1)
        }
    }
    catch {
        $PythonMetrics += [PSCustomObject]@{
            Lines = -1
            File  = $file.FullName.Substring($ProjectRoot.Length + 1)
        }
    }
}

Add-Content $ReportPath ("Python files: " + $PythonFiles.Count)
Add-Content $ReportPath ("Python lines: " + $TotalPythonLines)
Add-Content $ReportPath ""
Add-Content $ReportPath '```text'
Add-Content $ReportPath ($PythonMetrics | Sort-Object Lines -Descending | Format-Table -AutoSize | Out-String)
Add-Content $ReportPath '```'

Add-Section "5. Tests and syntax"

Add-CommandResult "Python version" "python --version"
Add-CommandResult "Unittest discovery" "python -m unittest discover -v"
Add-CommandResult "Compileall" "python -m compileall -q ."

if (Test-Path (Join-Path $ProjectRoot "pytest.ini")) {
    Add-CommandResult "Pytest" "python -m pytest -q"
}
elseif (Test-Path (Join-Path $ProjectRoot "pyproject.toml")) {
    Add-CommandResult "Pytest if installed" "python -m pytest -q"
}
else {
    Add-Content $ReportPath "Pytest: no pytest.ini or pyproject.toml detected."
}

Add-Section "6. Dependencies"

foreach ($depFile in @("requirements.txt","pyproject.toml","package.json","package-lock.json")) {
    $path = Join-Path $ProjectRoot $depFile
    if (Test-Path $path) {
        Add-CommandResult $depFile "Get-Content -LiteralPath `"$path`" -Raw"
    }
}

Add-CommandResult "Installed Python packages" "python -m pip freeze"

Add-Section "7. Static security scan"

$SecurityPatterns = @(
    "verify\s*=\s*False",
    "shell\s*=\s*True",
    "subprocess\.",
    "os\.system\s*\(",
    "eval\s*\(",
    "exec\s*\(",
    "pickle\.",
    "yaml\.load\s*\(",
    "powershell\.exe",
    "Invoke-Expression",
    "Start-Process",
    "requests\.(get|post|put|patch|delete)\s*\(",
    "webbrowser\.open",
    "open\s*\([^)]*['""]w['""]",
    "json\.dump\s*\("
)

foreach ($pattern in $SecurityPatterns) {
    Add-Content $ReportPath ("### Pattern: " + $pattern)
    Add-Content $ReportPath ""
    Add-Content $ReportPath '```text'

    $matches = Select-String -Path ($PythonFiles.FullName) -Pattern $pattern -AllMatches -ErrorAction SilentlyContinue

    if ($matches) {
        foreach ($match in $matches) {
            $relative = $match.Path.Substring($ProjectRoot.Length + 1)
            Add-Content $ReportPath ("{0}:{1}: {2}" -f $relative,$match.LineNumber,$match.Line.Trim())
        }
    }
    else {
        Add-Content $ReportPath "[No matches]"
    }

    Add-Content $ReportPath '```'
    Add-Content $ReportPath ""
}

Add-Section "8. Sensitive-looking files and directories"

Add-CommandResult "Potential runtime or sensitive files" "Get-ChildItem -LiteralPath `"$ProjectRoot`" -Recurse -Force -File | Where-Object { `$_.Name -match '(^|\.)(env|key|pem|p12|pfx|secret|secrets|token|credentials?)$|password|credential|reclamados|settings|cache' -and `$_.FullName -notmatch '\\\.git\\|\\node_modules\\|\\_audit\\' } | Select-Object FullName,Length | Format-Table -AutoSize"

Add-Section "9. Network and external services"

$NetworkPatterns = @(
    "https?://",
    "requests\.",
    "Session\s*\(",
    "webbrowser\.",
    "socket\.",
    "urllib\."
)

foreach ($pattern in $NetworkPatterns) {
    Add-Content $ReportPath ("### Network pattern: " + $pattern)
    Add-Content $ReportPath ""
    Add-Content $ReportPath '```text'

    $matches = Select-String -Path ($PythonFiles.FullName) -Pattern $pattern -AllMatches -ErrorAction SilentlyContinue

    if ($matches) {
        foreach ($match in $matches) {
            $relative = $match.Path.Substring($ProjectRoot.Length + 1)
            Add-Content $ReportPath ("{0}:{1}: {2}" -f $relative,$match.LineNumber,$match.Line.Trim())
        }
    }
    else {
        Add-Content $ReportPath "[No matches]"
    }

    Add-Content $ReportPath '```'
    Add-Content $ReportPath ""
}

Add-Section "10. Persistence and data writes"

$PersistencePatterns = @(
    "os\.replace",
    "fsync",
    "tempfile",
    "json\.dump",
    "open\s*\(",
    "QSettings",
    "winreg",
    "RegSetValue",
    "Path\."
)

foreach ($pattern in $PersistencePatterns) {
    Add-Content $ReportPath ("### Persistence pattern: " + $pattern)
    Add-Content $ReportPath ""
    Add-Content $ReportPath '```text'

    $matches = Select-String -Path ($PythonFiles.FullName) -Pattern $pattern -AllMatches -ErrorAction SilentlyContinue

    if ($matches) {
        foreach ($match in $matches) {
            $relative = $match.Path.Substring($ProjectRoot.Length + 1)
            Add-Content $ReportPath ("{0}:{1}: {2}" -f $relative,$match.LineNumber,$match.Line.Trim())
        }
    }
    else {
        Add-Content $ReportPath "[No matches]"
    }

    Add-Content $ReportPath '```'
    Add-Content $ReportPath ""
}

Add-Section "11. Packaging and distribution"

$PackagingFiles = @(
    "*.spec",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "pyside6-deploy.spec",
    "*.iss",
    "*.wxs",
    "*.msix",
    "*.appx"
)

$foundPackaging = Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File -Include $PackagingFiles -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\node_modules\\|\\.git\\|\\_audit\\' }

if ($foundPackaging) {
    Add-Content $ReportPath '```text'
    Add-Content $ReportPath ($foundPackaging | Select-Object FullName,Length | Format-Table -AutoSize | Out-String)
    Add-Content $ReportPath '```'
}
else {
    Add-Content $ReportPath "No common packaging configuration files detected."
}

Add-Section "12. Assets"

$AssetsDir = Join-Path $ProjectRoot "assets"

if (Test-Path $AssetsDir) {
    Add-CommandResult "Asset inventory" "Get-ChildItem -LiteralPath `"$AssetsDir`" -Recurse -File | Sort-Object Length -Descending | Select-Object @{N='MB';E={[math]::Round(`$_.Length / 1MB,2)}},Length,FullName | Format-Table -AutoSize"
}
else {
    Add-Content $ReportPath "assets directory not found."
}

Add-Section "13. Documentation"

foreach ($doc in @("README.md","CHANGELOG.md","LICENSE","CONTEXTO_PROYECTO.md")) {
    $path = Join-Path $ProjectRoot $doc
    if (Test-Path $path) {
        Add-Content $ReportPath ("### " + $doc)
        Add-Content $ReportPath ""
        Add-Content $ReportPath '```text'
        try {
            $text = Get-Content -LiteralPath $path -Raw -ErrorAction Stop
            Add-Content $ReportPath $text
        }
        catch {
            Add-Content $ReportPath ("ERROR: " + $_.Exception.Message)
        }
        Add-Content $ReportPath '```'
        Add-Content $ReportPath ""
    }
}

Add-Section "14. Git ignored files"

Add-CommandResult "Git ignored files" "git -C `"$ProjectRoot`" status --ignored --short"

Add-Section "15. Optional source snapshot"

Add-Content $ReportPath "The following section lists source files and their sizes. Full source is not duplicated here by default."
Add-Content $ReportPath ""

foreach ($file in $PythonMetrics | Sort-Object File) {
    Add-Content $ReportPath ("- " + $file.File + " (" + $file.Lines + " lines)")
}

Add-Section "16. Audit instructions for AI review"

Add-Content $ReportPath @"
AI REVIEW INSTRUCTIONS

Review this audit as a senior software architect, Python/PySide6 engineer,
Windows desktop security reviewer, QA engineer, and release engineer.

Rules:
1. Do not modify project files.
2. Do not assume an old audit finding is still valid.
3. Verify every important finding against the current source.
4. Separate confirmed issues from hypotheses.
5. Assign severity using P0, P1, P2, P3, P4.
6. Pay special attention to:
   - security
   - thread safety
   - data integrity
   - network handling
   - external URLs
   - PowerShell or subprocess execution
   - image downloading
   - persistence
   - UI responsiveness
   - animations
   - accessibility
   - DPI and resizing
   - resource paths
   - packaging
   - dependency hygiene
   - tests and coverage
   - privacy and network disclosure
   - license consistency
   - release hygiene

For every confirmed issue provide:
- severity
- exact file
- exact relevant function/class
- why it is a problem
- realistic impact
- recommended fix
- regression test required

Do not recommend a release merely because tests pass.
Do not perform or request destructive actions.
"@

Add-Content $ReportPath ""
Add-Content $ReportPath "---"
Add-Content $ReportPath ("Audit finished: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Add-Content $ReportPath ("Report: " + $ReportPath)

Write-Host ""
Write-Host "AUDIT COMPLETED" -ForegroundColor Green
Write-Host ("Project root: " + $ProjectRoot)
Write-Host ("Report: " + $ReportPath)
Write-Host ""
