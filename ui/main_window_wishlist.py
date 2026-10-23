"""Wishlist de precios de CheapShark, aislada de la búsqueda de juegos gratis."""

import time

from PySide6.QtCore import QThread, Qt, Signal, QUrl, QTimer
from PySide6.QtGui import QDesktopServices, QDoubleValidator
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout,
    QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QSizePolicy,
)

import config
from core.cheapshark import search_games, get_game_deals, get_stores, get_regional_prices, deal_url
from core.paths import SETTINGS_FILE, WISHLIST_FILE
from core.storage import cargar_json_seguro, guardar_json_atomico
from core.i18n import t
from logger import log_error, log_info, log_warning

CHECK_INTERVAL_SECONDS = 6 * 60 * 60
_DETACHED_WISHLIST_WORKERS = set()


class _WishlistWorker(QThread):
    completed = Signal(str, object)
    failed = Signal(str, str)

    def __init__(self, operation, payload=None, parent=None):
        super().__init__(parent)
        self.operation = operation
        self.payload = payload or {}

    def run(self):
        try:
            if self.operation == "search":
                result = search_games(self.payload.get("query", ""))
            else:
                stores = get_stores()
                result = {}
                if self.isInterruptionRequested():
                    return
                games = self.payload.get("games", {})
                for game_id in self.payload.get("game_ids", []):
                    if self.isInterruptionRequested():
                        break
                    try:
                        game_data = get_game_deals(game_id)
                        if self.isInterruptionRequested():
                            break
                        game_data["deals"] = [
                            deal for deal in game_data.get("deals", [])
                            if str(deal.get("storeID", "")) in stores
                        ]
                        saved = games.get(str(game_id), {})
                        store_names = {
                            stores[str(deal.get("storeID", ""))]
                            for deal in game_data["deals"]
                            if str(deal.get("storeID", "")) in stores
                        }
                        game_data["_regional_prices"] = get_regional_prices(
                            game_data.get("info", {}).get("title") or saved.get("title", ""),
                            game_data.get("info", {}).get("steamAppID") or saved.get("steam_app_id"),
                            # CheapShark puede tener solo ofertas activas; consultar
                            # Steam y GOG también permite mostrar su banner cuando
                            # el juego está disponible a precio normal.
                            store_names | {"Steam", "GOG"},
                            should_cancel=self.isInterruptionRequested,
                        )
                        if self.isInterruptionRequested():
                            break
                        result[str(game_id)] = game_data
                    except Exception as exc:
                        log_warning(f"No se pudieron actualizar ofertas para {game_id}: {exc}")
                result["_meta"] = {"stores": stores}
            self.completed.emit(self.operation, result)
        except Exception as exc:
            self.failed.emit(self.operation, str(exc))


def _load_wishlist(self):
    raw = cargar_json_seguro(str(WISHLIST_FILE), default={})
    if not isinstance(raw, dict) or not isinstance(raw.get("games", {}), dict):
        return {"games": {}, "last_check": 0}
    return {"games": raw.get("games", {}), "last_check": float(raw.get("last_check", 0) or 0)}


def _save_wishlist(self):
    return guardar_json_atomico(str(WISHLIST_FILE), self.wishlist_data)


def _initialize_wishlist(self):
    self.wishlist_data = _load_wishlist(self)
    self._wishlist_worker = None
    self._wishlist_is_active = False
    self._wishlist_stores = {}
    self._wishlist_timer = QTimer(self)
    self._wishlist_timer.setInterval(CHECK_INTERVAL_SECONDS * 1000)
    self._wishlist_timer.timeout.connect(lambda: _check_wishlist(self))
    self._wishlist_timer.start()
    _update_wishlist_badge(self)
    if self.wishlist_data["games"]:
        last_check = self.wishlist_data.get("last_check", 0)
        elapsed = time.time() - last_check if last_check else CHECK_INTERVAL_SECONDS
        delay = max(5000, int((CHECK_INTERVAL_SECONDS - elapsed) * 1000))
        QTimer.singleShot(delay, lambda: _check_wishlist(self))


def alternar_wishlist(self):
    entrando = not getattr(self, "_wishlist_is_active", False)
    if entrando:
        self._wishlist_previous_view = {
            "filters": dict(self.active_filters),
            "all": bool(self.todas_activado),
            "store": self.tienda_seleccionada,
            "claimed": bool(self.mostrando_reclamados),
        }
    self._wishlist_is_active = not self._wishlist_is_active
    if self._wishlist_is_active:
        self.mostrando_reclamados = False
        self.mostrando_wishlist = True
        self.active_filters = {store: False for store in self.active_filters}
        self.todas_activado = False
        self.tienda_seleccionada = None
        self.btn_actualizar.hide()
        self.wishlist_search_panel.show()
        self.btn_wishlist.setText("♥ WISHLIST")
        self._set_button_role(self.btn_wishlist, "wishlist_active")
        self.btn_reclamados.setText(t("claimed.btn"))
        self.btn_reclamados.setProperty("role", "secondary")
        self._actualizar_visibilidad_atras()
        self._ajustar_ventana_por_estado(True)
        _render_wishlist(self)
        _update_wishlist_badge(self)
        # Refresca al entrar para que los banners y resaltados reflejen el
        # estado actual. El worker evita duplicar una consulta ya en curso.
        if self.wishlist_data.get("games"):
            _check_wishlist(self)
    else:
        self.mostrando_wishlist = False
        self.btn_actualizar.show()
        self.wishlist_search_panel.hide()
        self.btn_wishlist.setText("♡ WISHLIST")
        self._set_button_role(self.btn_wishlist, "wishlist")
        previous = getattr(self, "_wishlist_previous_view", None) or {}
        saved_filters = previous.get("filters", {})
        self.active_filters = {
            store: bool(saved_filters.get(store, False))
            for store in self.active_filters
        }
        self.todas_activado = bool(previous.get("all", False))
        self.tienda_seleccionada = previous.get("store")
        self.mostrando_reclamados = bool(previous.get("claimed", False))
        self.btn_side_todas.setIcon(
            self._crear_icono_seleccion(not self.todas_activado)
        )
        self.btn_side_todas.setToolTip(
            t("sidebar.deselect_all") if self.todas_activado else t("sidebar.select_all")
        )
        self.btn_reclamados.setText(
            t("claimed.btn_active") if self.mostrando_reclamados else t("claimed.btn")
        )
        self.btn_reclamados.setProperty(
            "role", "accent" if self.mostrando_reclamados else "secondary"
        )
        self.btn_reclamados.style().unpolish(self.btn_reclamados)
        self.btn_reclamados.style().polish(self.btn_reclamados)
        self._sync_store_states()
        self._actualizar_visibilidad_atras()
        self._actualizar_vista_juegos()
        _update_wishlist_badge(self)


def _buscar_juegos_wishlist(self):
    query = self.wishlist_query.text().strip()
    if len(query) < 2:
        return
    if self._wishlist_worker and self._wishlist_worker.isRunning():
        return
    self.wishlist_search_button.setEnabled(False)
    self.wishlist_search_button.setText("BUSCANDO…")
    _start_wishlist_worker(self, "search", {"query": query})


def _anadir_juego_wishlist(self):
    candidate = self.wishlist_results.currentData()
    if not isinstance(candidate, dict):
        return
    game_id = str(candidate.get("gameID", ""))
    if not game_id:
        return
    games = self.wishlist_data["games"]
    if game_id in games:
        self._set_status("Ese juego ya está en la Wishlist", "warning")
        return
    games[game_id] = {
        "game_id": game_id,
        "title": candidate.get("external") or "Juego sin título",
        "steam_app_id": candidate.get("steamAppID"),
        "thumb": candidate.get("thumb", ""),
        "target_eur": None,
        "deals": [],
        "best_eur": None,
        "last_notified_eur": None,
    }
    if not self._save_wishlist():
        games.pop(game_id, None)
        self._set_status("No se pudo guardar la Wishlist", "error")
        return
    self.wishlist_results.clear()
    self.wishlist_results.setCurrentIndex(-1)
    self.wishlist_results.hide()
    self.wishlist_add_button.hide()
    self.wishlist_query.clear()
    _render_wishlist(self)
    _check_wishlist(self)


def _start_wishlist_worker(self, operation, payload):
    worker = _WishlistWorker(operation, payload, self)
    worker.completed.connect(self._wishlist_operation_completed)
    worker.failed.connect(self._wishlist_operation_failed)
    worker.finished.connect(worker.deleteLater)
    self._wishlist_worker = worker
    worker.start()


def _wishlist_worker_finished(self, worker):
    if self._wishlist_worker is worker:
        self._wishlist_worker = None
    worker.deleteLater()


def _wishlist_offer_is_active(deal):
    """Indica si una tienda ofrece un descuento, sin confundir precio normal con oferta."""
    try:
        if deal.get("price_exact"):
            current = deal.get("price_eur")
            retail = deal.get("retail_eur")
            return current is not None and retail is not None and float(current) < float(retail)
        current = float(deal.get("price_usd") or 0)
        retail = float(deal.get("retail_usd") or 0)
        savings = float(deal.get("savings") or 0)
        return savings > 0 or (current > 0 and retail > current)
    except (TypeError, ValueError):
        return False


def _wishlist_offer_map(deals):
    offers = {}
    for deal in deals if isinstance(deals, list) else []:
        if not isinstance(deal, dict) or not _wishlist_offer_is_active(deal):
            continue
        store = str(deal.get("store") or deal.get("store_id") or "Tienda digital").strip()
        key = store.casefold()
        current = offers.get(key)
        if current is None:
            offers[key] = deal
            continue
        price, currency = _wishlist_comparable_price(deal)
        old_price, old_currency = _wishlist_comparable_price(current)
        if price is not None and (old_price is None or (currency == old_currency and price < old_price)):
            offers[key] = deal
    return offers


def _wishlist_comparable_price(deal):
    try:
        if deal.get("price_eur") is not None:
            return float(deal["price_eur"]), "EUR"
        if not deal.get("price_exact") and float(deal.get("price_usd") or 0) > 0:
            return float(deal["price_usd"]), "USD"
    except (TypeError, ValueError):
        pass
    return None, None


def _wishlist_format_price(amount, currency):
    if amount is None:
        return "precio disponible"
    if currency == "EUR":
        return f"{amount:.2f}".replace(".", ",") + " €"
    return f"${amount:.2f} USD"


def _wishlist_offer_alerts(title, old_deals, new_deals, has_baseline):
    """Devuelve novedades y bajadas comparando cada tienda con su revisión anterior."""
    if not has_baseline:
        return []
    previous = _wishlist_offer_map(old_deals)
    current = _wishlist_offer_map(new_deals)
    alerts = []
    for key, deal in current.items():
        store = str(deal.get("store") or "Tienda digital")
        price, currency = _wishlist_comparable_price(deal)
        old_deal = previous.get(key)
        if old_deal is None:
            price_text = _wishlist_format_price(price, currency)
            alerts.append(f"Nueva oferta: {title} · {store} · {price_text}")
            continue

        old_price, old_currency = _wishlist_comparable_price(old_deal)
        if price is None or old_price is None or currency != old_currency or price >= old_price - 0.005:
            continue
        old_text = _wishlist_format_price(old_price, old_currency)
        new_text = _wishlist_format_price(price, currency)
        alerts.append(f"Bajó: {title} · {store} · {old_text} → {new_text}")
    return alerts


def _wishlist_operation_completed(self, operation, payload):
    self._wishlist_worker = None
    if operation == "search":
        self.wishlist_search_button.setEnabled(True)
        self.wishlist_search_button.setText("BUSCAR JUEGO")
        self.wishlist_results.clear()
        candidates = payload if isinstance(payload, list) else []
        for game in candidates:
            title = str(game.get("external") or "Juego sin título")
            # El precio de este endpoint es el más bajo entre todas las tiendas
            # de CheapShark, incluidas tiendas ajenas a KG Tracker. Se muestra
            # solo tras filtrar las tiendas admitidas en la consulta de ofertas.
            self.wishlist_results.addItem(title, game)
        self.wishlist_results.setVisible(bool(candidates))
        self.wishlist_add_button.setVisible(bool(candidates))
        self.wishlist_results.setCurrentIndex(-1)
        if candidates:
            self.wishlist_results.showPopup()
        if not candidates:
            self._set_status("No se encontraron juegos", "warning")
        return

    meta = payload.pop("_meta", {}) if isinstance(payload, dict) else {}
    self._wishlist_stores = meta.get("stores", {})
    changed = False
    notifications = []
    for game_id, response in payload.items():
        entry = self.wishlist_data["games"].get(str(game_id))
        if not entry or not isinstance(response, dict):
            continue
        regional_prices = response.get("_regional_prices", {})
        deals = []
        for deal in response.get("deals", []):
            try:
                usd = float(deal.get("price", 0))
            except (TypeError, ValueError):
                continue
            try:
                retail_usd = float(deal.get("retailPrice", 0) or 0)
            except (TypeError, ValueError):
                retail_usd = 0.0
            try:
                savings = float(deal.get("savings", 0) or 0)
            except (TypeError, ValueError):
                savings = 0.0
            store_id = str(deal.get("storeID", ""))
            store_name = self._wishlist_stores.get(store_id, "Tienda digital")
            regional = regional_prices.get(store_name)
            deals.append({
                "store": store_name,
                "store_id": store_id,
                "price_usd": usd,
                "retail_usd": retail_usd,
                "price_eur": regional.get("price_eur") if regional else None,
                "retail_eur": regional.get("retail_eur") if regional else None,
                "price_exact": bool(regional),
                "price_source": regional.get("source") if regional else None,
                "deal_id": deal.get("dealID", ""),
                # El precio regional de la tienda es la fuente de verdad cuando
                # está disponible; CheapShark puede tener el dato horario viejo.
                "savings": float(regional.get("savings", 0) or 0) if regional else savings,
            })
        present_stores = {deal["store"] for deal in deals}
        for store_name, regional in regional_prices.items():
            if store_name in present_stores:
                continue
            steam_app_id = str(entry.get("steam_app_id") or "").strip()
            store_url = regional.get("url", "")
            if store_name == "Steam" and steam_app_id.isdigit():
                store_url = f"https://store.steampowered.com/app/{steam_app_id}/?cc=es&l=spanish"
            deals.append({
                "store": store_name,
                "store_id": f"regional:{store_name.casefold()}",
                "price_usd": 0.0,
                "retail_usd": 0.0,
                "price_eur": regional.get("price_eur"),
                "retail_eur": regional.get("retail_eur"),
                "price_exact": True,
                "price_source": regional.get("source"),
                "deal_id": "",
                "store_url": store_url,
                "savings": float(regional.get("savings", 0) or 0),
            })
        deals.sort(key=lambda deal: (deal["price_eur"] is None, deal["price_eur"] or float("inf"), deal["price_usd"]))
        verified_deals = [deal for deal in deals if deal["price_eur"] is not None]
        best_deal = min(verified_deals, key=lambda deal: deal["price_eur"]) if verified_deals else None
        best_eur = best_deal["price_eur"] if best_deal else None
        # Los best_eur guardados por versiones antiguas procedían de convertir
        # USD; no sirven como referencia para detectar bajadas reales.
        previous = entry.get("best_eur") if entry.get("best_price_source") else None
        target = entry.get("target_eur")
        try:
            target_value = float(target) if target is not None else None
        except (TypeError, ValueError):
            target_value = None
        try:
            previous_value = float(previous) if previous is not None else None
        except (TypeError, ValueError):
            previous_value = None
        target_reached = (
            best_eur is not None
            and target_value is not None
            and best_eur <= target_value
            and (previous_value is None or previous_value > target_value)
        )
        title = str(entry.get("title") or game_id)
        if target_reached:
            store = str(best_deal.get("store") or "Tienda")
            notifications.append(
                f"Objetivo alcanzado: {title} · {store} · "
                f"{_wishlist_format_price(best_eur, 'EUR')} (límite "
                f"{_wishlist_format_price(target_value, 'EUR')})"
            )

        old_deals = entry.get("deals", [])
        has_baseline = bool(entry.get("updated_at") or old_deals)
        store_alerts = _wishlist_offer_alerts(title, old_deals, deals, has_baseline)
        if target_reached:
            best_store_key = str(best_deal.get("store") or "Tienda").casefold()
            target_alert_prefixes = (
                f"nueva oferta: {title} · {best_store_key} ·".casefold(),
                f"bajó: {title} · {best_store_key} ·".casefold(),
            )
            store_alerts = [
                alert for alert in store_alerts
                if not alert.casefold().startswith(target_alert_prefixes)
            ]
        notifications.extend(store_alerts)
        entry["deals"] = deals
        entry["best_eur"] = best_eur
        entry["best_price_source"] = best_deal.get("price_source") if best_deal else None
        entry["updated_at"] = int(time.time())
        changed = True
        log_info(
            f"[Wishlist] {entry.get('title', game_id)}: "
            f"tiendas={', '.join(deal.get('store', 'Tienda') for deal in deals) or 'ninguna'}; "
            f"oferta={best_deal.get('store', 'ninguna') if best_deal else 'ninguna'}"
        )
    self.wishlist_data["last_check"] = time.time()
    guardado = self._save_wishlist()
    _render_wishlist(self)
    _update_wishlist_badge(self)
    self._set_status(
        t("wishlist.updated") if guardado else "No se pudo guardar la Wishlist; los cambios podrían perderse al cerrar",
        "success" if guardado else "error",
    )
    for message in notifications if guardado else []:
        tray = getattr(self, "_tray", None)
        ajustes = cargar_json_seguro(str(SETTINGS_FILE), default={})
        if tray and ajustes.get("notificaciones_activas", True):
            restantes = len(notifications) - 1
            if restantes:
                message = f"{message} · +{restantes} más"
            titulo = "Alerta de Wishlist" if len(notifications) == 1 else f"Wishlist · {len(notifications)} alertas"
            tray.mostrar_notificacion_push(
                titulo, message
            )
            break
    log_info(f"Wishlist actualizada; {len(notifications)} bajadas relevantes.")


def _wishlist_operation_failed(self, operation, message):
    self._wishlist_worker = None
    if operation == "search":
        self.wishlist_search_button.setEnabled(True)
        self.wishlist_search_button.setText("BUSCAR JUEGO")
    log_warning(f"Fallo de la Wishlist ({operation}): {message}")
    self._set_status("Wishlist temporalmente no disponible", "warning")


def _check_wishlist(self):
    if not self.wishlist_data.get("games"):
        return
    worker = getattr(self, "_wishlist_worker", None)
    if worker and worker.isRunning():
        return
    _start_wishlist_worker(
        self, "check", {
            "game_ids": list(self.wishlist_data["games"].keys()),
            "games": self.wishlist_data["games"],
        }
    )


def _wait_wishlist_worker(self, timeout_ms=20000):
    worker = getattr(self, "_wishlist_worker", None)
    if worker is None:
        return True
    try:
        if worker.isRunning():
            worker.requestInterruption()
            terminado = worker.wait(timeout_ms)
            if not terminado:
                log_error("La consulta de Wishlist superó el plazo de cierre; se desacopla para no bloquear la salida.")
                worker.setParent(None)
                _DETACHED_WISHLIST_WORKERS.add(worker)
                worker.finished.connect(
                    lambda worker=worker: _DETACHED_WISHLIST_WORKERS.discard(worker)
                )
        self._wishlist_worker = None
        return True
    except RuntimeError:
        self._wishlist_worker = None
        return True


def _remove_wishlist_game(self, game_id):
    game_id = str(game_id)
    removed = self.wishlist_data["games"].pop(game_id, None)
    if not self._save_wishlist():
        if removed is not None:
            self.wishlist_data["games"][game_id] = removed
        self._set_status("No se pudo guardar la Wishlist", "error")
        return
    _render_wishlist(self)
    _update_wishlist_badge(self)


def _save_wishlist_target(self, game_id, text):
    entry = self.wishlist_data.get("games", {}).get(str(game_id))
    if not entry:
        return
    previous_target = entry.get("target_eur")
    normalized = str(text or "").strip().replace(",", ".")
    try:
        target = float(normalized) if normalized else None
    except ValueError:
        target = None
    entry["target_eur"] = target
    if not self._save_wishlist():
        entry["target_eur"] = previous_target
        self._set_status("No se pudo guardar el objetivo de precio", "error")
    _render_wishlist(self)


def _game_has_active_offer(entry):
    for deal in entry.get("deals", []):
        try:
            if deal.get("price_exact"):
                retail = deal.get("retail_eur")
                current = deal.get("price_eur")
                if retail is not None and current is not None:
                    if float(current) < float(retail):
                        return True
                    continue
            if float(deal.get("savings", 0) or 0) > 0:
                return True
            retail = deal.get("retail_eur")
            current = deal.get("price_eur")
            if retail is not None and current is not None and float(current) < float(retail):
                return True
        except (TypeError, ValueError):
            continue
    return False


def _update_wishlist_badge(self):
    badge = getattr(self, "wishlist_notification_badge", None)
    if badge is None:
        return
    count = sum(
        _game_has_active_offer(entry)
        for entry in self.wishlist_data.get("games", {}).values()
    )
    badge.setText("99+" if count > 99 else str(count))
    width = 27 if count > 99 else (22 if count > 9 else 18)
    badge.setFixedSize(width, 18)
    parent = badge.parentWidget()
    if parent:
        badge.move(parent.width() - width - 2, 0)
        badge.raise_()
    badge.setVisible(count > 0 and not getattr(self, "mostrando_wishlist", False))


def _render_wishlist(self):
    if not getattr(self, "mostrando_wishlist", False):
        return
    log_info(f"[Wishlist UI] Renderizando tarjetas: {len(self.wishlist_data.get('games', {}))}")
    self.container.setVisible(True)
    self.container.setMaximumHeight(16777215)
    self.frame_lista_layout.setEnabled(False)
    while self.frame_lista_layout.count():
        item = self.frame_lista_layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
    self.game_widgets_map.clear()
    games = self.wishlist_data["games"]
    if not games:
        label = QLabel("Tu Wishlist está vacía. Busca un juego arriba para empezar a seguir su precio.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setMinimumHeight(110)
        self.frame_lista_layout.addWidget(label)
    for game_id, entry in sorted(games.items(), key=lambda pair: str(pair[1].get("title", "")).casefold()):
        card = QFrame(self.frame_lista)
        card.setObjectName("wishlistCard")
        card.setStyleSheet(
            f"QFrame#wishlistCard {{ background: {config.THEMES[config.CURRENT_THEME]['COLOR_BG_CARD']}; "
            f"border: 1px solid {config.THEMES[config.CURRENT_THEME]['COLOR_BORDER']}; border-radius: 12px; }}"
        )
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(10, 9, 12, 9)
        card_layout.setSpacing(12)
        cover = QLabel("🎮")
        cover.setObjectName("wishlistCover")
        cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cover.setFixedSize(112, 64)
        thumb_url = str(entry.get("thumb") or "")
        if thumb_url:
            cover.setProperty("imageUrl", thumb_url)
            from core.image_loader import ImageLoader
            ImageLoader.get_instance().cargar(
                thumb_url,
                lambda url, pixmap, target=cover: _wishlist_cover_loaded(target, url, pixmap),
                target_size=(224, 128),
                context=f"Wishlist: {entry.get('title', 'juego')}",
            )
        card_layout.addWidget(cover, 0, Qt.AlignmentFlag.AlignVCenter)
        details = QWidget(card)
        details_layout = QVBoxLayout(details)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(6)
        heading = QHBoxLayout()
        heading.setSpacing(10)
        title = QLabel(str(entry.get("title", "Juego")))
        title.setObjectName("wishlistTitle")
        heading.addWidget(title, 1)
        best = entry.get("best_eur")
        best_label = QLabel(f"Desde {float(best):.2f} €" if best is not None else ("Precio en España sin verificar" if entry.get("deals") else "Buscando precio…"))
        best_label.setObjectName("wishlistPrice")
        heading.addWidget(best_label)
        remove = QPushButton("×")
        remove.setObjectName("wishlistRemoveButton")
        remove.setToolTip("Quitar de la Wishlist")
        remove.setFixedSize(28, 28)
        remove.clicked.connect(lambda _checked=False, gid=game_id: _remove_wishlist_game(self, gid))
        heading.addWidget(remove)
        details_layout.addLayout(heading)
        deals = entry.get("deals", [])
        log_info(
            f"[Wishlist UI] {entry.get('title', game_id)}: "
            f"tipo_deals={type(deals).__name__}, tiendas={len(deals) if isinstance(deals, list) else 'inválido'}"
        )
        store_row = QHBoxLayout()
        store_row.setContentsMargins(0, 0, 0, 0)
        store_row.setSpacing(8)
        theme = config.THEMES[config.CURRENT_THEME]
        if deals:
            store_groups = {}
            for deal in deals:
                key = str(deal.get("store_id") or deal.get("store") or "store")
                store_name = str(deal.get("store") or "").strip()
                if not store_name:
                    store_name = self._wishlist_stores.get(str(deal.get("store_id", "")), "Tienda digital")
                group = store_groups.setdefault(key, {"store": store_name, "deals": []})
                group["deals"].append(deal)
            for group in store_groups.values():
                group_deals = sorted(group["deals"], key=lambda item: (item.get("price_eur") is None, item.get("price_eur") or float("inf"), item.get("price_usd") or float("inf")))
                offer_deals = [
                    candidate for candidate in group_deals
                    if _game_has_active_offer({"deals": [candidate]})
                ]
                # Si hay varias entradas para la misma tienda, resalta y
                # muestra los precios de la entrada rebajada, no los de otra.
                deal = (offer_deals or group_deals)[0]
                store_name = group["store"] or "Tienda digital"
                is_on_sale = bool(offer_deals)
                price = deal.get("price_eur") if deal.get("price_exact") else None
                retail = deal.get("retail_eur") if deal.get("price_exact") else None
                if price is not None and is_on_sale and retail is not None:
                    tooltip = (
                        f"{store_name} · Antes: {float(retail):.2f} € · "
                        f"Oferta: {float(price):.2f} € · {deal.get('price_source', 'precio regional')}"
                    )
                elif price is not None:
                    tooltip = f"{store_name} · Precio: {float(price):.2f} € · {deal.get('price_source', 'precio regional')}"
                elif is_on_sale:
                    tooltip = (
                        f"{store_name} · Antes: ${float(deal.get('retail_usd') or 0):.2f} USD · "
                        f"Oferta: ${float(deal.get('price_usd') or 0):.2f} USD · Precio de España sin verificar"
                    )
                else:
                    tooltip = (
                        f"{store_name} · ${float(deal.get('price_usd') or 0):.2f} USD · "
                        "Precio de España sin verificar"
                    )
                percent = float(deal.get("savings", 0) or 0)
                if is_on_sale and percent > 0:
                    tooltip += f" · Descuento: {percent:.0f}%"
                chip = QFrame()
                chip.setObjectName("wishlistStoreChip")
                chip.setProperty("onSale", is_on_sale)
                theme = config.THEMES[config.CURRENT_THEME]
                chip.setStyleSheet("QFrame#wishlistStoreChip { background: transparent; border: none; }")
                chip.setToolTip(tooltip)
                chip_layout = QHBoxLayout(chip)
                chip_layout.setContentsMargins(0, 1, 0, 1)
                chip_layout.setSpacing(6)
                store_button = QPushButton(store_name.upper())
                store_button.setObjectName("wishlistStoreButton")
                if config.CURRENT_THEME == "dark":
                    if is_on_sale:
                        store_button.setStyleSheet("""
                            QPushButton#wishlistStoreButton {
                        background-color: #8A6512;
                        color: #FFF4C2;
                        border: 2px solid #FFD54A;
                                border-radius: 6px;
                        padding: 2px 10px;
                                font: bold 8pt "Segoe UI";
                            }
                            QPushButton#wishlistStoreButton:hover {
                        background-color: #A77A16;
                            }
                        """)
                    else:
                        store_button.setStyleSheet("""
                            QPushButton#wishlistStoreButton {
                                background-color: rgba(99, 102, 241, 0.18);
                                color: #A5B4FC;
                                border: 1px solid #818CF8;
                                border-radius: 6px;
                                padding: 2px 8px;
                                font: bold 8pt "Segoe UI";
                            }
                            QPushButton#wishlistStoreButton:hover {
                                background-color: rgba(99, 102, 241, 0.32);
                            }
                        """)
                else:
                    if is_on_sale:
                        store_button.setStyleSheet("""
                            QPushButton#wishlistStoreButton {
                                background: #F8E9B6;
                                color: #70510B;
                                border: 2px solid #C89617;
                                border-radius: 6px;
                                padding: 2px 10px;
                                font: bold 8pt "Segoe UI";
                            }
                            QPushButton#wishlistStoreButton:hover { background: #F2D98A; }
                        """)
                    else:
                        store_button.setStyleSheet("""
                            QPushButton#wishlistStoreButton {
                                background: #E3E8EF;
                                color: #536B9D;
                                border: 1px solid #AEBFD7;
                                border-radius: 6px;
                                padding: 2px 8px;
                                font: bold 8pt "Segoe UI";
                            }
                            QPushButton#wishlistStoreButton:hover { background: #D7E0EC; }
                        """)
                store_button.setToolTip(tooltip)
                store_button.setCursor(Qt.CursorShape.PointingHandCursor)
                store_button.setMinimumHeight(25)
                store_button.setMinimumWidth(max(58, store_button.fontMetrics().horizontalAdvance(store_name.upper()) + 22))
                deal_id = deal.get("deal_id", "")
                store_button.clicked.connect(
                    lambda _checked=False, did=deal_id, url=deal.get("store_url", ""):
                    QDesktopServices.openUrl(QUrl(url or deal_url(did))) if (url or did) else None
                )
                chip_layout.addWidget(store_button)
                # El chip debe conservar el ancho de su nombre y no colapsar
                # cuando la fila también contiene el objetivo de precio.
                chip.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
                chip.setMinimumWidth(chip.sizeHint().width())
                # El nombre de la tienda siempre permanece visible. Los dos
                # precios aparecen juntos al pasar el cursor por el banner.
                store_row.addWidget(chip)
        else:
            no_deals = QLabel("No hay tiendas disponibles para este juego en el comparador")
            no_deals.setObjectName("wishlistEmpty")
            store_row.addWidget(no_deals)
        store_row.addStretch(1)

        # El objetivo comparte una sola línea con las tiendas y usa tonos neutros
        # del tema; el verde queda reservado para indicar que ya se alcanzó.
        target_control = QFrame()
        target_control.setObjectName("wishlistTargetControl")
        target_control.setStyleSheet(
            f"QFrame#wishlistTargetControl {{ background: {theme['COLOR_BG_DESC']}; "
            f"border: 1px solid {theme['COLOR_BORDER']}; border-radius: 7px; }}"
        )
        target_layout = QHBoxLayout(target_control)
        target_layout.setContentsMargins(7, 3, 7, 3)
        target_layout.setSpacing(5)
        target_caption = QLabel("OBJETIVO")
        target_caption.setStyleSheet(
            f"color: {theme['COLOR_TEXT_MUTED']}; font: bold 7pt 'Segoe UI'; background: transparent; border: none;"
        )
        target_layout.addWidget(target_caption)
        target_input = QLineEdit()
        target_input.setObjectName("wishlistTargetInput")
        target_input.setPlaceholderText("00,00")
        target_input.setFixedWidth(66)
        target_input.setMaximumHeight(25)
        target_input.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        target_input.setStyleSheet(
            f"QLineEdit#wishlistTargetInput {{ background: {theme['COLOR_BG_CARD']}; "
            f"color: {theme['COLOR_TEXT_PRIMARY']}; border: 1px solid {theme['COLOR_BORDER']}; "
            f"border-radius: 5px; padding: 3px 5px; font: 8pt 'Segoe UI'; }} "
            f"QLineEdit#wishlistTargetInput:focus {{ border-color: {theme['COLOR_ACCENT_LIGHT']}; }}"
        )
        target_input.setValidator(QDoubleValidator(0.0, 9999.0, 2, target_input))
        target_value = entry.get("target_eur")
        if target_value is not None:
            target_input.setText(f"{float(target_value):.2f}")
        target_input.setToolTip("Objetivo de precio en euros. Se guarda al salir del campo.")
        target_input.editingFinished.connect(
            lambda gid=game_id, field=target_input: _save_wishlist_target(self, gid, field.text())
        )
        target_layout.addWidget(target_input)
        target_currency = QLabel("€")
        target_currency.setStyleSheet(
            f"color: {theme['COLOR_TEXT_MUTED']}; font: 8pt 'Segoe UI'; background: transparent; border: none;"
        )
        target_layout.addWidget(target_currency)
        store_row.addWidget(target_control)

        target = entry.get("target_eur")
        best_value = entry.get("best_eur")
        if target is not None and best_value is not None and float(best_value) <= float(target):
            reached = QLabel("OBJETIVO ALCANZADO")
            reached.setObjectName("wishlistTargetReached")
            reached.setStyleSheet(
                f"QLabel#wishlistTargetReached {{ background: {theme['COLOR_SUCCESS']}; "
                "color: #FFFFFF; border-radius: 6px; padding: 4px 7px; font: bold 7pt 'Segoe UI'; }"
            )
            store_row.addWidget(reached)
        details_layout.addLayout(store_row)
        card_layout.addWidget(details, 1)
        self.frame_lista_layout.addWidget(card)
    self.frame_lista_layout.addStretch(1)
    self.frame_lista_layout.setEnabled(True)
    self.frame_lista_layout.activate()
    _update_wishlist_badge(self)


def _wishlist_cover_loaded(label, url, pixmap):
    if label.property("imageUrl") != url or pixmap is None or pixmap.isNull():
        return
    from PySide6.QtCore import QRect
    from PySide6.QtGui import QPainter, QPainterPath
    size = label.size()
    scaled = pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                           Qt.TransformationMode.SmoothTransformation)
    x = max(0, (scaled.width() - size.width()) // 2)
    y = max(0, (scaled.height() - size.height()) // 2)
    cropped = scaled.copy(QRect(x, y, size.width(), size.height()))
    rounded = cropped.copy()
    rounded.fill(Qt.GlobalColor.transparent)
    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(0, 0, size.width(), size.height(), 8, 8)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, cropped)
    painter.end()
    label.setText("")
    label.setPixmap(rounded)


def _wishlist_intercept_view(self):
    if getattr(self, "mostrando_wishlist", False):
        _render_wishlist(self)
        return True
    return False


def instalar_metodos(cls):
    cls._initialize_wishlist = _initialize_wishlist
    cls._save_wishlist = _save_wishlist
    cls.alternar_wishlist = alternar_wishlist
    cls._buscar_juegos_wishlist = _buscar_juegos_wishlist
    cls._anadir_juego_wishlist = _anadir_juego_wishlist
    cls._wishlist_operation_completed = _wishlist_operation_completed
    cls._wishlist_operation_failed = _wishlist_operation_failed
    cls._check_wishlist = _check_wishlist
    cls._wait_wishlist_worker = _wait_wishlist_worker
    cls._remove_wishlist_game = _remove_wishlist_game
    cls._render_wishlist = _render_wishlist
    cls._wishlist_intercept_view = _wishlist_intercept_view
    cls._update_wishlist_badge = _update_wishlist_badge
