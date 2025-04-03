FROM python:3.10-slim

# Instalar ferramentas básicas + Node.js
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential unzip git && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g nativefier electron@25.9.0

# Diretório da app
WORKDIR /app
COPY . .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar pasta de builds
RUN mkdir -p /app/builds

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
