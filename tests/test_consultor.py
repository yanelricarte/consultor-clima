"""Tests unitarios de la clase ConsultorClima."""
from unittest.mock import patch

import pytest
import requests

from app import ConsultorClima, ClimaError
from tests.conftest import fake_response, WEATHER_OK


def test_validar_ciudad():
    c = ConsultorClima("k")
    assert c._validar_ciudad("Madrid")
    assert not c._validar_ciudad("a")          # demasiado corto
    assert not c._validar_ciudad("x" * 51)     # demasiado largo
    assert not c._validar_ciudad("")


def test_obtener_clima_actual_ok():
    c = ConsultorClima("k")
    with patch("app.requests.get", return_value=fake_response(200, WEATHER_OK)):
        resultado = c.obtener_clima_actual("Mar del Plata")
    assert "MAR DEL PLATA" in resultado
    assert "18.5" in resultado


def test_obtener_clima_404_lanza_error():
    c = ConsultorClima("k")
    with patch("app.requests.get", return_value=fake_response(404, {"message": "city not found"})):
        with pytest.raises(ClimaError, match="no encontrada"):
            c.obtener_clima_actual("Ciudadinexistentexyz")


def test_obtener_clima_401_lanza_error():
    c = ConsultorClima("k")
    with patch("app.requests.get", return_value=fake_response(401, {"message": "invalid key"})):
        with pytest.raises(ClimaError, match="autenticación"):
            c.obtener_clima_actual("Madrid")


def test_obtener_clima_timeout_lanza_error():
    c = ConsultorClima("k")
    with patch("app.requests.get", side_effect=requests.exceptions.Timeout):
        with pytest.raises(ClimaError, match="demasiado tiempo"):
            c.obtener_clima_actual("Madrid")


def test_obtener_clima_connection_error():
    c = ConsultorClima("k")
    with patch("app.requests.get", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(ClimaError, match="conexión"):
            c.obtener_clima_actual("Madrid")


def test_datos_incompletos_lanza_error():
    c = ConsultorClima("k")
    # Respuesta 200 pero sin las claves que espera el formateo.
    with patch("app.requests.get", return_value=fake_response(200, {"name": "X"})):
        with pytest.raises(ClimaError, match="incompletos"):
            c.obtener_clima_actual("Madrid")
