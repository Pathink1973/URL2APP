FROM python:3.10-slim

# Instalar dependências básicas
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential unzip git

# Instalar Node.js (v18) + atualizar NPM
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Instalar Nativefier e Electron separadamente (para evitar erro do idealTree)
RUN npm install -g nativefier
RUN npm install electron@25.9.0

# Criar diretório da app
WORKDIR /app
COPY . /app

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Garantir pasta builds
RUN mkdir -p /app/builds

# Expor a porta usada pelo Streamlit
EXPOSE 8501

# Rodar o app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
