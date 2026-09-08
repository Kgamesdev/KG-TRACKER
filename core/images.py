import os
import requests
import hashlib
from io import BytesIO
from PIL import Image, ImageTk
from config import THUMBNAIL_SIZE

CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

_REFERENCIAS_IMAGENES = {}

def _obtener_nombre_cache(url_img):
    hash_url = hashlib.sha256(url_img.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, f"{hash_url}.png")

def guardar_en_cache(url_img, datos_bytes=None):
    pass

def limpiar_cache_imagenes():
    """Libera las referencias de miniaturas en memoria.

    No elimina los archivos PNG almacenados en disco.
    """
    _REFERENCIAS_IMAGENES.clear()

def obtener_tamaño_cache():
    total_bytes = 0
    if os.path.exists(CACHE_DIR):
        for archivo in os.listdir(CACHE_DIR):
            ruta = os.path.join(CACHE_DIR, archivo)
            if os.path.isfile(ruta):
                total_bytes += os.path.getsize(ruta)
    return round(total_bytes / (1024 * 1024), 2)

def descargar_imagen_thumbnail(url_img):
    if not url_img:
        return None

    if url_img in _REFERENCIAS_IMAGENES:
        return _REFERENCIAS_IMAGENES[url_img]

    nombre_archivo = _obtener_nombre_cache(url_img)

    try:
        if os.path.exists(nombre_archivo):
            img = Image.open(nombre_archivo)
            photo = ImageTk.PhotoImage(img)
            _REFERENCIAS_IMAGENES[url_img] = photo
            return photo

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(url_img, headers=headers, timeout=5)
        if res.status_code == 200:
            img_orig = Image.open(BytesIO(res.content)).convert("RGBA")
            img_orig.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            canvas_img = Image.new("RGBA", THUMBNAIL_SIZE, (0, 0, 0, 0))
            x = (THUMBNAIL_SIZE[0] - img_orig.width) // 2
            y = (THUMBNAIL_SIZE[1] - img_orig.height) // 2
            canvas_img.paste(img_orig, (x, y), img_orig)

            canvas_img.save(nombre_archivo, "PNG")

            photo = ImageTk.PhotoImage(canvas_img)
            _REFERENCIAS_IMAGENES[url_img] = photo
            return photo
    except Exception as e:
        print(f"Error descargando miniatura ({url_img}): {e}")

    return None