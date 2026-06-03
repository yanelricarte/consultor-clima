"""Tests de los endpoints HTTP de la app."""
from unittest.mock import patch

from tests.conftest import fake_response, WEATHER_OK


def test_health_responde_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"


def test_clima_actual_sin_ciudad_devuelve_400(client):
    r = client.get("/clima_actual")
    assert r.status_code == 400
    assert "ciudad" in r.get_json()["error"].lower()


def test_clima_actual_con_ciudad_valida(client):
    with patch("app.requests.get", return_value=fake_response(200, WEATHER_OK)):
        r = client.get("/clima_actual?ciudad=Mar del Plata")
    assert r.status_code == 200
    resultado = r.get_json()["resultado"]
    assert "MAR DEL PLATA" in resultado
    assert "18.5" in resultado


def test_clima_actual_ciudad_inexistente_devuelve_400(client):
    payload = {"message": "city not found"}
    with patch("app.requests.get", return_value=fake_response(404, payload)):
        r = client.get("/clima_actual?ciudad=Ciudadinexistentexyz")
    assert r.status_code == 400
    assert "no encontrada" in r.get_json()["error"].lower()


def test_endpoint_desconocido_devuelve_404(client):
    r = client.get("/no-existe")
    assert r.status_code == 404
    assert "error" in r.get_json()
