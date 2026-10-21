from ui.main_window_games import _clasificar_resultado_busqueda


def test_all_sources_failed_is_reported_as_offline():
    assert _clasificar_resultado_busqueda(7, 0, False) == "offline"


def test_successful_empty_search_is_distinct_from_outage():
    assert _clasificar_resultado_busqueda(7, 7, False) == "empty"


def test_some_sources_failed_is_reported_as_partial():
    assert _clasificar_resultado_busqueda(7, 4, False) == "partial"


def test_any_offer_means_results_are_available():
    assert _clasificar_resultado_busqueda(7, 0, True) == "offers"
