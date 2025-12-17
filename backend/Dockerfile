# Dockerfile para Railway - Estoque Engenho
# Use Python 3.11 para compatibilidade
FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    pkg-config \
    default-libmysqlclient-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache)
COPY requirements.txt .

# Atualizar pip e instalar dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para arquivos estáticos
RUN mkdir -p static

# Expor porta (Railway define automaticamente)
EXPOSE 8000

# Comando para iniciar - Railway usa $PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
