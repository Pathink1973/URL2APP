FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y curl gnupg build-essential unzip git && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g nativefier && \
    npm install electron@25.9.0

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/builds

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
