import psycopg2
import os
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

# Lê as variáveis de ambiente
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

print("🔍 Testando conexão com o banco PostgreSQL...")
print(f"→ Host: {DB_HOST}, Banco: {DB_NAME}, Usuário: {DB_USER}")

try:
    # Tenta se conectar ao banco
    connection = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    print("✅ Conexão bem-sucedida!")
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("🧠 Versão do PostgreSQL:", record)

except Exception as e:
    print("❌ Erro ao conectar ao banco de dados:")
    print(e)

finally:
    if 'connection' in locals() and connection:
        connection.close()
        print("🔒 Conexão encerrada.")
