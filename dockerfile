# Usar Ubuntu 24.04 como base
FROM ubuntu:24.04
# Evitar interacciones durante la instalación (como configuraciones de zona horaria)
ENV DEBIAN_FRONTEND=noninteractive
# Actualizar paquetes e instalar herramientas básicas
RUN apt-get update && apt-get install -y curl build-essential




# Instalar git
RUN apt-get install -y git
# Clonar el repositorio
RUN git clone https://github.com/0865marc/idealista_scrapper.git
# Establecer directorio de trabajo
WORKDIR /idealista_scrapper

# Instalar uv (usando curl para obtener la última versión) y añadir comandos de depuración
RUN curl -LsSf https://astral.sh/uv/install.sh | sh 
# Configurar PATH para incluir uv
ENV PATH="/root/.local/bin:${PATH}"
# Instalar dependencias python
RUN uv sync




EXPOSE 8000
# Ejecutar el script principal
CMD ["uv", "run", "main.py"]







