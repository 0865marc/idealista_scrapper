# Usar Ubuntu 24.04 como base
FROM ubuntu:24.04
# Evitar interacciones durante la instalación (como configuraciones de zona horaria)
ENV DEBIAN_FRONTEND=noninteractive
# Actualizar paquetes e instalar herramientas básicas
RUN apt-get update && apt-get install -y curl build-essential
# Instalar git
RUN apt-get install -y git


# Copiar archivos locales 
WORKDIR /idealista_scrapper
COPY . .


# Instalar uv (usando curl para obtener la última versión) y añadir comandos de depuración
RUN curl -LsSf https://astral.sh/uv/install.sh | sh 
# Configurar PATH para incluir uv
ENV PATH="/root/.local/bin:${PATH}"
# Instalar dependencias python
RUN uv sync


EXPOSE 8000
# Ejecutar el script principal
CMD ["uv", "run", "main.py"]







