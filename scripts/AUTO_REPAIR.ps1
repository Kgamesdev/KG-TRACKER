# AUTO_REPAIR_KG_TRACKER.ps1 (Versión Corregida)
$ROOT = Get-Location
Write-Host "🤖 Finalizando REPARACIÓN AUTOMÁTICA..." -ForegroundColor Cyan

# 1. Reparar core\tray.py
$trayPath = "core\tray.py"
if (Test-Path $trayPath) {
    $content = Get-Content $trayPath -Raw
    $old = 'startupinfo = subprocess\.STARTUPINFO\(\)[\s\S]*?creationflags=subprocess\.CREATE_NO_WINDOW if sys\.platform == "win32" else 0,'
    $new = '        if hasattr(self, "tray_icon"): self.tray_icon.showMessage("KG Tracker", "Actualización", QSystemTrayIcon.Information, 3000)'
    Set-Content $trayPath ($content -replace $old, $new) -Encoding UTF8
}

# 2. Optimizar .spec
$specPath = "KGameTracker.spec"
if (Test-Path $specPath) {
    $content = Get-Content $specPath -Raw
    $ex = "excludes=['PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets', 'PySide6.QtDesigner', 'PySide6.QtHelp'],"
    if ($content -match "excludes=\[\]") {
        Set-Content $specPath ($content -replace "excludes=\[\]", $ex) -Encoding UTF8
    }
}

# 3. Limpieza de caché (CORREGIDO)
$loaderPath = "core\image_loader.py"
if (Test-Path $loaderPath) {
    $currentContent = Get-Content $loaderPath -Raw
    if ($currentContent -notmatch "def limpiar_cache_antigua") {
        $clean = "`ndef limpiar_cache_antigua(dias=30):`n    import time, os`n    from .paths import CACHE_DIR`n    if not os.path.exists(CACHE_DIR): return`n    ahora = time.time()`n    for f in os.listdir(CACHE_DIR):`n        r = os.path.join(CACHE_DIR, f)`n        if (os.path.isfile(r) and (os.stat(r).st_mtime < ahora - (dias*86400))):`n            try: os.remove(r)`n            except: pass"
        Add-Content $loaderPath $clean -Encoding UTF8
        Write-Host "✅ Limpiador de caché añadido a core\image_loader.py" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ El limpiador de caché ya estaba presente." -ForegroundColor Yellow
    }
}

Write-Host "🚀 ¡Todo reparado y optimizado correctamente!" -ForegroundColor Cyan
