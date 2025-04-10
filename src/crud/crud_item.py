import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db_connection

def criar_item(quantidade, id_compra, id_produto):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO item (quantidade, id_compra, id_produto) VALUES (?, ?, ?)", (quantidade, id_compra, id_produto))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erro ao inserir item: {e}")
    finally:
        conn.close()