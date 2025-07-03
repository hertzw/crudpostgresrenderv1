import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

class repositorio():
    mydb = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT", 5432)
    )  # Conexão com dados do banco de dados e PostgreSQL
    cursor = mydb.cursor()

