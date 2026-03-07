import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle
import mysql.connector
from mysql.connector import Error

# -----------------------------
# Datos de entrenamiento estáticos definidos en el código:[tiempo_pagina, productos_vistos, compra]
# -----------------------------
datos_entrenamiento = [
    [1, 0, 0], [1, 2, 0], [1, 4, 0], [2, 1, 0], [2, 3, 0],
    [2, 5, 0], [3, 0, 0], [3, 2, 0], [3, 4, 1], [4, 1, 0],
    [4, 3, 1], [4, 5, 1], [5, 2, 0], [5, 4, 1], [5, 6, 1],
    [6, 1, 0], [6, 3, 1], [6, 5, 1], [7, 2, 1], [7, 4, 1],
    [7, 6, 1], [8, 3, 1], [8, 5, 1], [8, 7, 1], [9, 4, 1],
    [9, 6, 1], [9, 8, 1], [10, 5, 1], [10, 7, 1], [10, 9, 1],
    [11, 4, 1], [11, 6, 1], [11, 8, 1], [12, 5, 1], [12, 7, 1],
    [12, 9, 1], [13, 6, 1], [13, 8, 1], [13, 10, 1], [14, 7, 1],
    [14, 9, 1], [14, 10, 1], [15, 8, 1], [15, 10, 1], [16, 7, 1],
    [16, 9, 1], [17, 8, 1], [18, 9, 1], [19, 10, 1], [20, 10, 1]
]

df_estatico = pd.DataFrame(
    datos_entrenamiento,
    columns=["tiempo_pagina", "productos_vistos", "compra"]
)

# -----------------------------
# Función para obtener datos desde MySQL
# -----------------------------
def obtener_datos_mysql():
    try:
        conexion = mysql.connector.connect(
            host="db",
            port=3306,
            user="appuser",
            password="apppass",
            database="predictive_purchase"
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
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()
            print("Conexión a MySQL cerrada")

# -----------------------------
# Obtener los datos
# -----------------------------
df = obtener_datos_mysql()

# Si la base de datos no tiene datos, usar los datos estáticos
if df is None or df.empty:
    print("Usando datos estáticos definidos en el código")
    df = df_estatico

# -----------------------------
# Entrenar el modelo
# -----------------------------
X = df[["tiempo_pagina", "productos_vistos"]]
y = df["compra"]

modelo = Pipeline([
    ("scaler", StandardScaler()),
    ("logistic", LogisticRegression())
])

modelo.fit(X, y)

# -----------------------------
# Guardar modelo entrenado
# -----------------------------
with open("modelo.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("Modelo entrenado y guardado correctamente")