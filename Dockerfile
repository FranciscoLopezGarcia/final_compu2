# Dockerfile

# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos del proyecto al contenedor
COPY . .

# Comando por defecto (puede sobreescribirse con docker-compose)
CMD ["python", "server.py"]
