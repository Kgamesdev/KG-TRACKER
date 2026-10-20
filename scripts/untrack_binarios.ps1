# Deja de versionar los binarios compilados (siguen en tu disco; ya están en .gitignore).
# Ejecutar UNA vez desde la raíz del repo, después de aplicar el parche:
#   powershell -ExecutionPolicy Bypass -File scripts\untrack_binarios.ps1
git rm -r --cached --ignore-unmatch dist build KG-TRACKER-Portable.zip
git commit -m "chore: dejar de versionar binarios (dist, build, zip); se publican en Releases"
Write-Host "Hecho. Sube el KG-TRACKER-Portable.zip como asset de la próxima Release."
Write-Host "Opcional: para borrar el peso del historial antiguo usa 'git filter-repo --path dist --path build --invert-paths'."
