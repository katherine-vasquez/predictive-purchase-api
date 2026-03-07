from fastapi import FastAPI, HTTPException
import pickle
import numpy as np
import os
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
import time  # <--- agregado para el retry loop

app = FastAPI(
    title="Predictive Purchase API",
    version="0.1.0"
)

# ------------------------
# Modelos Pydantic
# ------------------------
class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int

class PrediccionInput(BaseModel):
    tiempo_pagina: int
    productos_vistos: int

# ------------------------
# Función para conectarse a MySQL con retry
# ------------------------
def obtener_conexion():
    intentos = 5  # número de reintentos
    while intentos > 0:
        try:
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                port=3306,
                user=os.getenv("DB_USER", "appuser"),
                password=os.getenv("DB_PASSWORD", "apppass"),
                database=os.getenv("DB_NAME", "predictive_purchase")
            )
            return conexion
        except Error as e:
            print(f"Error al conectar a MySQL, reintentando en 5s: {e}")
            intentos -= 1
            time.sleep(5)  # espera 5 segundos antes de reintentar
    return None

# ------------------------
# Endpoint de prueba
# ------------------------
@app.get("/")
def inicio():
    return "Inicio"

@app.get("/test-mysql")
def test_mysql():
    conexion = obtener_conexion()
    if conexion:
        conexion.close()
        return {"mensaje": "Conexión a MySQL exitosa"}
    return {"mensaje": "Error al conectar a MySQL"}

# ------------------------
# Endpoints CRUD Productos
# ------------------------
@app.get("/productos")
def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos

@app.post("/productos")
def crear_producto(producto: Producto):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
        cursor.execute(sql, (producto.nombre, producto.precio, producto.stock))
        conexion.commit()
        producto_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        return {
            "id": producto_id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {e}")

@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id=%s"
        cursor.execute(sql, (producto.nombre, producto.precio, producto.stock, producto_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {
            "id": producto_id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {e}")

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id=%s", (producto_id,))
        producto = cursor.fetchone()
        if not producto:
            cursor.close()
            conexion.close()
            return {"mensaje": "Producto no encontrado"}
        cursor.execute("DELETE FROM productos WHERE id=%s", (producto_id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return producto
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {e}")

# ------------------------
# Endpoint de predicción
# ------------------------
@app.post("/predict")
def predecir(input: PrediccionInput):
    if not os.path.exists("modelo.pkl"):
        return {"mensaje": "Modelo no encontrado"}
    with open("modelo.pkl", "rb") as f:
        modelo = pickle.load(f)
    X = np.array([[input.tiempo_pagina, input.productos_vistos]])
    resultado = modelo.predict(X)[0]
    prob = modelo.predict_proba(X)[0]
    return {
        "resultado": "Compra" if resultado == 1 else "No Compra",
        "probabilidad_compra": f"{prob[1]*100:.2f}%",
        "probabilidad_no_compra": f"{prob[0]*100:.2f}%"
    }