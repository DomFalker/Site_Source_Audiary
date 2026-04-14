from sqlalchemy import create_engine
import sys
import os

# Adicionando o diretório atual ao path para importar db.conex
sys.path.append(os.getcwd())

try:
    from db.conex import engine
    with engine.connect() as conn:
        print("Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    sys.exit(1)
