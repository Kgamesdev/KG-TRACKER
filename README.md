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
  <img src="https://img.shields.io/badge/version-v0.5.0-blue?style=for-the-badge" alt="Version 0.5.0"/>
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

- **Broad free-game search:** combines GamerPower with direct searches of Epic Games, Steam, GOG, itch.io, Amazon Prime Gaming and Fanatical. Some additional stores can appear through GamerPower listings; direct coverage depends on each store's public data.
- **Automatic checks:** searches when the app starts and can repeat at the interval selected in Settings. Results load in the app; store pages open only when you choose an offer.
- **Smart filtering and deduplication:** filters demos and add-ons and merges duplicate offers across sources, regional links and translated titles.
- **Useful game details:** shows Steam review information when available and translates descriptions in the background.
- **Notifications and background checks:** scan on demand or periodically, with Windows notifications from the system tray while the app is minimized.
- **Claim history and savings:** saves claimed games locally and tracks their accumulated value.
- **Personal settings:** English and Spanish interface, softened light and dark themes, saved music preference, mute and volume controls, search interval, notifications, and optional start with Windows.
- **Window behavior:** single-instance protection, minimize to the system tray, and a setting to minimize or exit when closing the window.
- **Responsive interface:** loads game artwork asynchronously and uses caching to keep browsing smooth.

## 🚀 Quick Start

**Requirements:** Windows 10 or 11 and Python 3.12.

**Windows downloads:** see the [published releases](https://github.com/Kgamesdev/KG-TRACKER/releases). The [v0.5.0 source code](https://github.com/Kgamesdev/KG-TRACKER/tree/v0.5.0) is also available.

### Windows SmartScreen and SHA-256 verification

Windows SmartScreen may warn when downloading or starting KG Tracker because the executable is not signed with a publicly trusted code-signing certificate. This is a publisher/file reputation warning; by itself it does not prove the program is malicious or guarantee that it is safe.

When an EXE is published, download it only from [official GitHub releases](https://github.com/Kgamesdev/KG-TRACKER/releases) and compare its fingerprint with the attached `.sha256` file. In PowerShell, calculate it with `Get-FileHash .\KG-TRACKER.exe -Algorithm SHA256`.

SHA-256 only verifies that a file matches the bytes covered by that fingerprint. It does not certify who created the file, prove it is malware-free, or remove the SmartScreen warning.

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
| **Networking** | `requests` and concurrent session pooling |
| **Audio Engine** | `pygame-ce` |
| **Persistence** | Local JSON with atomic writes |

## 🔌 Credits and Data Sources

KG Tracker uses the following services, public endpoints and store pages. Some sources are public web pages rather than formal APIs. Availability and offer data are controlled by their providers.

- **[GamerPower API](https://www.gamerpower.com/api/)** — giveaway listings and offer details.
- **[Epic Games Store](https://store-site-backend-static.ak.epicgames.com/)** — free game promotions catalog.
- **[Steam Store](https://store.steampowered.com/)** — featured free/discounted games, app search and community reviews; artwork is served from the Steam CDN.
- **[itch.io](https://itch.io/games/on-sale?format=json)** — games-on-sale listing.
- **[GOG Catalog](https://catalog.gog.com/)** — discounted game catalog.
- **[Amazon Games / Luna](https://www.amazongamestudios.com/en-us/news)** — Prime Gaming offer announcements and public claim pages.
- **[Fanatical Promotions](https://support.fanatical.com/hc/en-us/articles/360018002197-Promotions-Summary-Terms-and-Conditions)** — promotion details used to identify current giveaways.
- **[Google Translate](https://translate.googleapis.com/)** — primary description translation source.
- **[MyMemory Translation API](https://mymemory.translated.net/)** — translation fallback.
- **[GitHub Releases API](https://docs.github.com/en/rest/releases/releases)** — latest release check inside the app.

## ☕ Support the Project

If KG Tracker is useful to you and you would like to support its development, you can [buy me a coffee on Ko-fi](https://ko-fi.com/kurigamedeveloper).

## 📋 Recent Highlights (v0.5.0)

- Persistent wishlist for tracking games and checking store availability, deals and prices.
- Store indicators remain visible on each tracked game; active deals are highlighted and expose the before and current prices on hover.
- Typo-tolerant game search and periodic price checks.
- Wishlist access from the main window, with a badge counting games currently on sale.
- Consistent typography and polished styling for windows, controls and menus.
- Wishlist price lookups now shut down cleanly when the app exits.

### v0.4.1 highlights

- Prevented missing and mismatched game artwork with store-specific image extraction, verified Steam title matching, and clearer diagnostics when an image cannot be loaded.
- Added regression tests for nested Itch.io cards, Amazon Prime artwork matching, and Steam fallback title verification.
- Preserved the v0.4.0 improvements: additional store sources, cross-language duplicate detection, automatic startup search, persistent audio settings, light theme refinements, and more reliable Windows single-instance startup.
- Added direct free-game sources for Amazon Prime Gaming and Fanatical alongside the existing store search and GamerPower fallback.
- Improved duplicate detection for equivalent titles across languages, sources and regional store URLs.
- Added automatic search on startup, persistent audio settings, and clearer minimize-to-tray versus exit behavior.
- Updated the light theme and settings interaction, and kept store tabs closed until the user opens an offer.
- Made artwork loading more resilient to temporary failures and added alternative images where available.
- Reorganized visual components internally for easier maintenance while preserving interface behavior.
- Hardened Windows single-instance startup by clearing stale system error state before acquiring the process mutex.

## 🤝 Help Improve the Project

Found a bug or have an idea? [Open an issue](https://github.com/Kgamesdev/KG-TRACKER/issues). Contributions are welcome; please read the [non-commercial license](LICENSE) before reusing the code.

## License

This project is licensed under a **Non-Commercial License**. See [LICENSE](LICENSE) for details.
