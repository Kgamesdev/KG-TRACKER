# K GAME TRACKER

<p align="center">
  <img src="assets/LogoKG_transparente.png" alt="KG Tracker" width="132"/>
</p>

<p align="center"><strong>Find free PC game offers across stores, all from one Windows app.</strong></p>

<p align="center">
  <a href="#quick-start">Get started</a> ·
  <a href="#features">Explore features</a> ·
  <a href="https://github.com/Kgamesdev/KG-TRACKER/issues">Share an idea or report a bug</a> ·
  <a href="https://github.com/Kgamesdev/KG-TRACKER">Star the project</a>
</p>

<p align="center">
  <a href="README_ES.md"><strong>Leer en español</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.3.4-blue?style=for-the-badge" alt="Version 0.3.4"/>
  <img src="https://img.shields.io/badge/Python-3.12%20tested-yellow?style=for-the-badge" alt="Python 3.12 tested"/>
  <img src="https://img.shields.io/badge/GUI-PySide6%20%2B%20Qt%206-41CD52?style=for-the-badge" alt="PySide6 and Qt 6"/>
  <img src="https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D6?style=for-the-badge" alt="Windows 10 and 11"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Non--Commercial-orange?style=for-the-badge" alt="Non-commercial license"/></a>
</p>

<p align="center">
  <a href="https://github.com/Kgamesdev/KG-TRACKER/stargazers"><img src="https://img.shields.io/github/stars/Kgamesdev/KG-TRACKER?style=social" alt="Star KG Tracker on GitHub"/></a>
  <a href="https://github.com/Kgamesdev/KG-TRACKER/issues"><img src="https://img.shields.io/github/issues/Kgamesdev/KG-TRACKER" alt="Open issues"/></a>
</p>

---

KG Tracker helps you catch limited-time PC game giveaways without checking every store by hand. It combines **GamerPower** listings with checks of supported store pages, then brings the offers together in one desktop app.

## Features

- **More places to find games:** combines giveaway listings and supported store sources to improve coverage.
- **Cleaner results:** filters out many demos and add-ons, and reduces duplicate offers when stores use different titles or languages.
- **Useful game details:** shows Steam review information when available and translates descriptions in the background.
- **Stay in the loop:** check offers manually or let the app scan periodically and send Windows notifications from the system tray.
- **Keep track of claims:** stores claimed games locally and shows your accumulated savings.
- **Make it yours:** Spanish and English interface, light and dark themes, persistent music and volume settings, and optional start with Windows.

KG Tracker is built for Windows 10 and 11 with Python and PySide6. Offers can expire or vary by region, account, and store.

## Quick start

### Requirements

- Windows 10 or 11
- Python 3.12 (tested)

### Run from source

```powershell
git clone https://github.com/Kgamesdev/KG-TRACKER.git
cd KG-TRACKER
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Help shape the project

Found a bug, missing a store, or have an idea? [Open an issue](https://github.com/Kgamesdev/KG-TRACKER/issues) and include what you expected and what happened. If KG Tracker is useful to you, [give the repository a star](https://github.com/Kgamesdev/KG-TRACKER/stargazers)—it helps other players discover it.

Contributions are welcome: fork the repository, make a focused change, and open a pull request. Please read the [license](LICENSE) before reusing the code; this project is **non-commercial**.

## Support

KG Tracker is a personal learning project. If you would like to support its development, you can [buy me a coffee on Ko-fi](https://ko-fi.com/kurigamedeveloper).

## Credits

Giveaway data is provided by [GamerPower](https://www.gamerpower.com/). The app also uses Steam community review information where available.
