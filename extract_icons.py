import os
from PIL import Image

# Ruta del atlas (ahora en assets)
atlas_path = r"D:\K GAME TRACKER\assets\atlas_neon.jpg"

# Carpeta de salida
output_dir = r"D:\K GAME TRACKER\assets\icons\stores"

# Crear carpeta si no existe
os.makedirs(output_dir, exist_ok=True)

# Abrir el atlas
img = Image.open(atlas_path)

# Dimensiones del atlas
w, h = img.size
print(f"Tamaño del atlas: {w}x{h}")

# Asumimos grid 3x3 (9 iconos)
cols = 3
rows = 3

# Calcular tamaño de cada icono (con margen)
icon_w = w // cols
icon_h = h // rows

print(f"Tamaño estimado por icono: {icon_w}x{icon_h}")

# Nombres de los iconos (orden según el atlas)
icon_names = [
    "epic", "steam", "gog",
    "amazon_prime", "itch_io", "humble_store",
    "fanatical", "indiegala", "other"
]

# Extraer cada icono
for i, name in enumerate(icon_names):
    row = i // cols
    col = i % cols
    
    x = col * icon_w
    y = row * icon_h
    
    # Recortar el icono (con un pequeño margen para eliminar bordes)
    crop_x = x + 10
    crop_y = y + 10
    crop_w = icon_w - 20
    crop_h = icon_h - 20
    
    icon = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
    
    # Guardar como PNG
    output_path = os.path.join(output_dir, f"{name}.png")
    icon.save(output_path, "PNG")
    print(f"✅ Icono guardado: {name}.png")

print("")
print("✅ Todos los iconos extraídos correctamente.")
