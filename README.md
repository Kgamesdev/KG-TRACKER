# K GAME TRACKER (KG Tracker)

<p align="center">
  <img src="assets/LogoKG_transparente.png" alt="KG Tracker Logo" width="150"/>
</p>

<p align="center"><strong>Find and claim time-limited free PC games from one Windows app.</strong></p>

<p align="center">
  <a href="#key-features">Features</a> · <a href="#quick-start">Quick start</a> · <a href="#credits-and-data-sources">Credits</a> · <a href="https://github.com/Kgamesdev/KG-TRACKER/issues">Ideas & bug reports</a>
</p>

<p align="center"><a href="README_ES.md"><strong>🇪🇸 Leer en español</strong></a></p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.3.4-blue?style=for-the-badge" alt="Version 0.3.4"/>
  <img src="https://img.shields.io/badge/Python-3.12%20tested-yellow?style=for-the-badge" alt="Python 3.12 tested"/>
  <img src="https://img.shields.io/badge/framework-PySide6%20%2B%20Qt%206-41CD52?style=for-the-badge" alt="PySide6 and Qt 6"/>
  <img src="https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D6?style=for-the-badge" alt="Windows 10 and 11"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Non--Commercial-orange?style=for-the-badge" alt="Non-commercial license"/></a>
</p>

<p align="center">
  <a href="https://github.com/Kgamesdev/KG-TRACKER/stargazers"><img src="https://img.shields.io/github/stars/Kgamesdev/KG-TRACKER?style=social" alt="Star KG Tracker"/></a>
  <a href="https://github.com/Kgamesdev/KG-TRACKER/issues"><img src="https://img.shields.io/github/issues/Kgamesdev/KG-TRACKER" alt="Open issues"/></a>
</p>

---

## 🎮 Project Description

**KG Tracker** is a native Windows desktop app built with **Python** and **PySide6 (Qt 6)**. It helps you find time-limited free PC game offers from multiple stores in one place. It also enriches offers with Steam community reviews and translates descriptions in the background.

## ✨ Key Features

- **Centralized multi-store tracking:** combines GamerPower listings with direct searches of Epic Games, Steam, GOG and itch.io.
- **Smart filtering and deduplication:** filters many demos and add-ons, and merges duplicate offers even when titles differ by language.
- **Useful game details:** shows Steam review information when available and translates descriptions in the background.
- **Notifications and background checks:** scan on demand or periodically, with Windows notifications from the system tray.
- **Claim history and savings:** saves claimed games locally and tracks their accumulated value.
- **Personal settings:** English and Spanish interface, light and dark themes, persistent music and volume settings, and optional start with Windows.
- **Responsive interface:** loads game artwork asynchronously and uses caching to keep browsing smooth.

## 🚀 Quick Start

**Requirements:** Windows 10 or 11 and Python 3.12.

```powershell
git clone https://github.com/Kgamesdev/KG-TRACKER.git
cd KG-TRACKER
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## 👋 About the Author

> This personal project was created by me, a nurse who never had much time to study programming, but always had an overwhelming desire to learn. I developed this project guided by research and AI. I hope you enjoy the hours and care I have put into it.

## 🧰 Architecture & Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.12 (tested) |
| **GUI Framework** | PySide6 (Qt 6.x) with QSS stylesheets |
| **Image Processing** | Pillow (`PIL`) |
| **Networking** | `requests` and concurrent session pooling |
| **Audio Engine** | `pygame-ce` |
| **Persistence** | Local JSON with atomic writes |

## 🔌 Credits and Data Sources

KG Tracker uses the following services and public endpoints. Availability and offer data are controlled by their providers.

- **[GamerPower API](https://www.gamerpower.com/api/)** — giveaway listings and offer details.
- **[Epic Games Store](https://store-site-backend-static.ak.epicgames.com/)** — free game promotions catalog.
- **[Steam Store](https://store.steampowered.com/)** — featured free/discounted games, app search and community reviews; artwork is served from the Steam CDN.
- **[itch.io](https://itch.io/games/on-sale?format=json)** — games-on-sale listing.
- **[GOG Catalog](https://catalog.gog.com/)** — discounted game catalog.
- **[Google Translate](https://translate.googleapis.com/)** — primary description translation source.
- **[MyMemory Translation API](https://mymemory.translated.net/)** — translation fallback.
- **[GitHub Releases API](https://docs.github.com/en/rest/releases/releases)** — latest release check inside the app.

## ☕ Support the Project

If KG Tracker is useful to you and you would like to support its development, you can [buy me a coffee on Ko-fi](https://ko-fi.com/kurigamedeveloper).

## 📋 Recent Highlights (v0.3.4)

- Broader free-game coverage by combining giveaway listings with direct store searches.
- Improved duplicate detection for the same game listed in different languages.
- Persistent music preferences and working playback controls.
- Single-instance protection, with clearer close and minimize-to-tray behavior.

## 🤝 Help Improve the Project

Found a bug or have an idea? [Open an issue](https://github.com/Kgamesdev/KG-TRACKER/issues). Contributions are welcome; please read the [non-commercial license](LICENSE) before reusing the code.

## License

This project is licensed under a **Non-Commercial License**. See [LICENSE](LICENSE) for details.
