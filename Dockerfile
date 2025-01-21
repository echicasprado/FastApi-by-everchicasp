# Stage 1: Build Stage
FROM python:3.11-slim AS builder

WORKDIR /info-projects

COPY requirements.txt .

# Instalar las dependencias necesarias incluyendo el controlador ODBC
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Production Stage
FROM python:3.11-slim

WORKDIR /info-projects

# Instalar solo el ODBC Driver 17 y UnixODBC en la imagen final
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    unixodbc && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar solo los archivos necesarios desde la etapa de construcción
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=builder /info-projects /info-projects

# Exponer el puerto en el que se ejecutará FastAPI
EXPOSE 4000

# Establecer el directorio de trabajo para la aplicación
WORKDIR /info-projects/app

# Comando para ejecutar la aplicación
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000" ]
