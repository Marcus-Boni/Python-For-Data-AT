import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db_connection

def criar_compra(data_compra, id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO compra (data_compra, id_cliente) VALUES (?, ?)", (data_compra, id_cliente))
        id_compra = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erro ao criar compra: {e}")
    finally:
        conn.close()
    return id_compra