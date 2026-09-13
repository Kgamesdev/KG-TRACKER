import os

# Obtener la ruta absoluta de la raíz del proyecto (donde está este script, subiendo un nivel)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_file = os.path.join(BASE_DIR, "CONTEXTO_PROYECTO.md")
main_entry = os.path.join(BASE_DIR, "main.py")
reqs_file = os.path.join(BASE_DIR, "requirements.txt")
exclude_dirs = {"__pycache__", ".venv", ".git", "node_modules", "cache", "logs", ".vscode", ".idea"}

print(f"Generando dossier en ruta absoluta: {output_file}")

def leer_seguro(ruta):
    for enc in ["utf-8", "utf-16", "latin-1"]:
        try:
            with open(ruta, "r", encoding=enc) as f:
                return f.read()
        except Exception:
            continue
    return ""

try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# CONTEXTO DEL PROYECTO: KG TRACKER (Clean Architecture)\n\n")
        f.write("## 1. Estructura de Archivos\n\n```text\n")
        
        root_depth = len(BASE_DIR.split(os.sep))
        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            path_parts = root.split(os.sep)
            depth = len(path_parts) - root_depth
            if depth < 0:
                depth = 0
            indent = "  " * depth
            if root != BASE_DIR:
                f.write(f"{indent}- {os.path.basename(root)}/\n")
            for file in files:
                if file == "CONTEXTO_PROYECTO.md":
                    continue
                f.write(f"{indent}  - {file}\n")
                
        f.write("```\n\n")
        
        if os.path.exists(reqs_file):
            f.write("## 2. Dependencias (requirements.txt)\n\n```\n")
            f.write(leer_seguro(reqs_file))
            f.write("\n```\n\n")
            
        if os.path.exists(main_entry):
            f.write("## 3. Punto de Entrada (main.py)\n\n```python\n")
            f.write(leer_seguro(main_entry))
            f.write("\n```\n")

    if os.path.exists(output_file):
        print(f"¡ÉXITO! Archivo confirmado físicamente en: {output_file}")
    else:
        print("❌ ERROR: El script terminó pero el archivo no se encuentra.")

except Exception as e:
    print(f"❌ Error crítico escribiendo el dossier: {e}")
