import urllib.request
url = "https://githubusercontent.com"
path = r"F:\KURIGAMESDEV\BACKUPS\ACTUAL\ui\main_window.py"
try:
    print("Reparando archivo...")
    urllib.request.urlretrieve(url, path)
    print("¡COMPLETADO CON ÉXITO! Ya puedes cerrar este archivo.")
    print("Prueba ahora a arrancar con: py main.py")
except Exception as e:
    print(f"Error: {e}")
