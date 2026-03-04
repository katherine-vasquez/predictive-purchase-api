FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Solo instalar lo que es necesario
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        liblapack-dev \
        default-libmysqlclient-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_USER=appuser
ENV DB_PASSWORD=apppassword
ENV DB_NAME=predictive_purchase

CMD sh -c "\
    echo 'Ejecutando pruebas...' && \
    pytest -v test/test_main.py && \
    echo 'Levantando FastAPI...' && \
    uvicorn main:app --host 0.0.0.0 --port 8000 \
"