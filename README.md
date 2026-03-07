Predictive Purchase API / API de Predicción de Compras
Descripción / Description

Español:
Este proyecto implementa una API para predecir la probabilidad de compra de un usuario usando FastAPI, MySQL y Docker. Permite gestionar productos (operaciones CRUD) y realizar predicciones basadas en el comportamiento del usuario en la página.

English:
This project implements an API to predict a user's purchase probability using FastAPI, MySQL, and Docker. It allows product management (CRUD operations) and predictions based on user behavior on the site.

Funcionalidades / Features

CRUD de productos / Product CRUD endpoints:

GET /productos – Listar productos / List products

POST /productos – Crear un producto / Create a new product

PUT /productos/{id} – Actualizar un producto / Update a product

DELETE /productos/{id} – Eliminar un producto / Delete a product

Predicción / Prediction endpoint:

POST /predict – Predecir la probabilidad de compra basado en el tiempo en página y productos vistos / Predict purchase probability based on page time and viewed products

Pruebas automatizadas / Automated tests:

Pruebas implementadas con pytest para asegurar el correcto funcionamiento

Dockerizado / Dockerized:

Contenedores para fácil despliegue y replicación del proyecto

Persistencia con MySQL / MySQL for data persistence

Requisitos / Requirements

Python 3.11

MySQL 8.0

Docker y Docker Compose

Paquetes Python (listados en requirements.txt)

Instalación y Ejecución / Installation & Running

Clonar el repositorio / Clone the repository:

git clone https://github.com/katherine-vasquez/predictive-purchase-api.git
cd predictive-purchase-api

Construir y levantar los contenedores / Build and run Docker containers:

docker-compose up --build -d

Entrenar el modelo (opcional) / Train the model (optional):

docker-compose exec app python train.py

Probar la API / Test the API:

curl http://localhost:8000/productos
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"tiempo_pagina": 5, "productos_vistos": 2}'
Estructura del Proyecto / Project Structure
Predictive-Purchase-API/
│
├─ app/ (código fuente de la API)
├─ tests/ (pruebas automatizadas)
├─ Dockerfile
├─ docker-compose.yml
├─ init.sql (datos iniciales para MySQL)
├─ train.py (entrenamiento del modelo)
├─ modelo.pkl (modelo entrenado)
├─ requirements.txt
└─ README.md
Uso / Usage

Levantar los contenedores Docker.

Entrenar el modelo con train.py para generar modelo.pkl.

Consultar los endpoints de la API para listar productos o predecir compras.
