# POLÍTICA DE PRIVACIDAD — KG TRACKER

**Última actualización:** Versión v0.2.35

KG Tracker es una aplicación de escritorio diseñada bajo el principio de **Privacidad por Diseño (Privacy by Design)**.

## 1. Recolección de Datos
* **0% Credenciales:** KG Tracker **NUNCA** solicita, almacena ni gestiona contraseñas, tokens de inicio de sesión ni datos bancarios de Steam, Epic Games, GOG ni de ninguna otra tienda.
* **0% Telemetría:** No recopilamos analíticas de uso, seguimiento de clicks ni identificadores únicos de usuario.

## 2. Almacenamiento Local
Todos tus datos personales de uso se guardan **exclusivamente en tu dispositivo local** en la siguiente ruta:
`%LOCALAPPDATA%\KGTracker\`

Archivos locales:
* `settings.json`: Preferencias de interfaz e idioma.
* `reclamados.json`: Lista de títulos que has marcado como reclamados.
* `cache/`: Miniaturas e historial de ofertas públicas cacheados para acelerar la interfaz.

## 3. Conexiones de Red Externas
KG Tracker realiza consultas exclusivas de lectura en protocolo **HTTPS** a las siguientes APIs públicas de promociones:
* Steam API (`store.steampowered.com`)
* Epic Games Store API (`store.epicgames.com`)
* GamerPower API (`gamerpower.com`)
* Servicio de Traducción Pública Google Translate / MyMemory

## 4. Control del Usuario
Puedes borrar en cualquier momento todo el historial de la aplicación eliminando la carpeta `%LOCALAPPDATA%\KGTracker\`.
