# K GAME TRACKER (KG Tracker)

<p align="center">
  <img src="assets/LogoKG_transparente.png" alt="KG Tracker Logo" width="130"/>
</p>

<p align="center">
  <strong>Desktop control center to track, centralize, and claim time-limited free PC video games.</strong>
</p>

<p align="center">
  <a href="README_ES.md"><strong>Español / Spanish Version</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.2.35-blue?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/python-3.14+-yellow?style=for-the-badge" alt="Python Version"/>
  <img src="https://img.shields.io/badge/framework-PySide6%20(Qt%206)-41CD52?style=for-the-badge" alt="PySide6"/>
  <img src="https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D6?style=for-the-badge" alt="Platform"/>
  <img src="https://img.shields.io/badge/license-Non--Commercial-orange?style=for-the-badge" alt="License"/>
</p>

---

## Project Description

**KG Tracker** is a native Windows desktop application built with **Python** and **PySide6 (Qt 6)**. Its primary purpose is to keep gamers informed about all 100% free, time-limited game offers across major PC digital distribution stores, automatically filtering out DLCs, demos, season passes, and soundtracks.

It features a real-time data enrichment engine that cross-references each giveaway with **Steam community reviews** and dynamically translates store descriptions in the background.

---

## Key Features

- **Centralized Multi-Store Tracking:** Monitors giveaways from Epic Games, Steam, GOG, Amazon Prime Gaming, Itch.io, Humble Store, Fanatical, and IndieGala via the GamerPower API.
- **Smart Filtering:** Automatically excludes expansions, skins, demos, betas, and secondary content, displaying exclusively full video games.
- **Live Steam API Integration:** Displays community scores and positive review percentages (e.g., `Steam: 95% (Very Positive)`) even for giveaways hosted on Epic Games, GOG, or Prime Gaming.
- **Dynamic Description Translator:** Asynchronous engine with multi-channel fallback (Google Mobile Web + MyMemory) that translates descriptions in the background without freezing the UI.
- **Full Internationalization (i18n):** On-the-fly bilingual support (Spanish / English) for buttons, status badges, modals, context menus, and push notifications.
- **High-Performance Architecture (60 FPS):** Asynchronous thumbnail loading and rendering (`QThreadPool` + `QRunnable`) with multi-level RAM and disk caching for fluid scrolling.
- **Windows System Tray Integration:** Minimizes to the tray area next to the clock with native bilingual push notifications and a configurable sweep timer (2h, 4h, 8h, 24h).
- **Claim History & Savings Tracker:** Safely stores claimed games locally using atomic I/O and calculates total accumulated savings in USD (`$ SAVED`).
- **Configurable Background Audio:** Background music player with smooth audio transitions (*Fade Out* on minimize, *Fade In* on restore).

---

## About the Author

> This personal project was created by me, a nurse who never had much time to study programming, but always had an overwhelming desire to learn. I developed this project guided solely by research and AI. I hope you enjoy the hours and care I have put into it.

---

## Architecture & Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.14 |
| **GUI Framework** | PySide6 (Qt 6.x) with dynamic QSS stylesheets |
| **Image Processing** | Pillow (`PIL`) |
| **Networking & APIs** | `requests` with concurrent session pooling |
| **Audio Engine** | `pygame-ce` |
| **Persistence** | Transactional JSON with atomic writing (`fsync` + safe replace) |

---

## License

This project is licensed under a **Non-Commercial License**. See the [**LICENSE**](LICENSE) file for more information.
