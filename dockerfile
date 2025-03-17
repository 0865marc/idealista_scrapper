FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /idealista_scrapper

# Instalar dependencias mínimas si las necesitas
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requisitos e instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn


EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--reload"]
