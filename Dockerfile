FROM python:3.12-slim

WORKDIR /app

# Instalar dependências de build se necessário (psycopg2-binary dispensa build, mas deixamos otimizado)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY . .

# Expor a porta 8000 para uso local ou padrão
EXPOSE 8000

# Iniciar o servidor usando a porta injetada pela nuvem ($PORT) ou 8000 como fallback
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
