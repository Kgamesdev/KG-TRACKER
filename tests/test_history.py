import pytest
from unittest.mock import MagicMock

def test_parsear_valor_juego():
    from ui.main_window_history import _parsear_valor_juego
    
    mock_self = MagicMock()
    
    assert _parsear_valor_juego(mock_self, ".99") == 19.99
    assert _parsear_valor_juego(mock_self, "14,99 €") == 14.99
    assert _parsear_valor_juego(mock_self, "Free") == 0.0
    assert _parsear_valor_juego(mock_self, None) == 0.0
    assert _parsear_valor_juego(mock_self, "N/A") == 0.0
    assert _parsear_valor_juego(mock_self, 50) == 50.0