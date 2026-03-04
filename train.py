import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle
import mysql.connector
from mysql.connector import Error

# Función para obtener datos desde MySQL
def obtener_datos_mysql():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",       # localhost si es Windows, "db" si es docker
            port=3306,
            user="usuario",         # definido en docker-compose.yml
            password="password",    # definido en docker-compose.yml
            database="predictivedb"
        )
        if conexion.is_connected():
            print("Conexión a MySQL exitosa desde train.py")
            query = "SELECT tiempo_pagina, productos_vistos, compra FROM registros_compra;"
            df = pd.read_sql(query, conexion)
            return df
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión a MySQL cerrada")

# Obtener los datos
df = obtener_datos_mysql()

if df is not None and not df.empty:
    X = df[["tiempo_pagina", "productos_vistos"]]
    y = df["compra"]

    # Pipeline con escalado + modelo
    modelo = Pipeline([
        ("scaler", StandardScaler()),
        ("logistic", LogisticRegression())
    ])

    modelo.fit(X, y)

    # Guardar modelo
    with open("modelo.pkl", "wb") as f:
        pickle.dump(modelo, f)

    print("Modelo entrenado y guardado correctamente")
else:
    print("No se pudieron obtener datos de MySQL. Modelo no entrenado.")