"""Configuración compartida de los tests.

La app exige API_KEY al importarse (crear_app() la valida), por eso se
define ANTES de importar app.py.
"""
import os

os.environ.setdefault("API_KEY", "test-key-123")

import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def fake_response(status_code, payload):
    """Respuesta HTTP falsa para mockear requests.get."""
    class _Resp:
        def __init__(self):
            self.status_code = status_code

        def json(self):
            return payload

    return _Resp()


# Payload completo de OpenWeatherMap (todas las claves que usa el formateo).
WEATHER_OK = {
    "name": "Mar del Plata",
    "sys": {"country": "AR"},
    "main": {"temp": 18.5, "feels_like": 17.0, "humidity": 60, "pressure": 1012},
    "weather": [{"description": "cielo claro"}],
    "wind": {"speed": 5.1},
    "dt": 1700000000,
}
