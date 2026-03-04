import sys
import os
from fastapi.testclient import TestClient

# Agrega la ruta del proyecto para poder importar main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

# ------------------------
# Endpoint de prueba
# ------------------------
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Inicio"

def test_test_mysql():
    response = client.get("/test-mysql")
    assert response.status_code == 200
    assert "mensaje" in response.json()

# ------------------------
# Endpoint de predicción
# ------------------------
def test_predict():
    response = client.post(
        "/predict",
        json={
            "tiempo_pagina": 10,
            "productos_vistos": 5
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "resultado" in json_data
    assert "probabilidad_compra" in json_data
    assert "probabilidad_no_compra" in json_data

# ------------------------
# Endpoints CRUD Productos
# ------------------------
def test_list_productos():
    response = client.get("/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_producto():
    nuevo_producto = {
        "nombre": "Producto Test",
        "precio": 99.99,
        "stock": 10
    }
    response = client.post("/productos", json=nuevo_producto)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Producto Test"
    assert data["precio"] == 99.99
    assert data["stock"] == 10
    return data["id"]  # Retornamos el ID para otros tests

def test_update_producto():
    producto_id = test_create_producto()  # Creamos un producto para actualizar
    actualizado = {
        "nombre": "Producto Actualizado",
        "precio": 149.99,
        "stock": 5
    }
    response = client.put(f"/productos/{producto_id}", json=actualizado)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Producto Actualizado"
    assert data["precio"] == 149.99
    assert data["stock"] == 5

def test_delete_producto():
    producto_id = test_create_producto()  # Creamos un producto para eliminar
    response = client.delete(f"/productos/{producto_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == producto_id
    # Comprobamos que ya no existe
    response_check = client.get("/productos")
    ids = [p["id"] for p in response_check.json()]
    assert producto_id not in ids