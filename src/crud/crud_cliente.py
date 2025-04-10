import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db_connection

def buscar_cliente(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nome FROM cliente WHERE id_cliente = ?", (id_cliente,))
    row = cursor.fetchone()
    conn.close()
    return {'id_cliente': row[0], 'nome': row[1]} if row else None

def inserir_cliente(id_cliente, nome):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cliente (id_cliente, nome) VALUES (?, ?)", (id_cliente, nome))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erro ao inserir cliente: {e}")
    finally:
        conn.close()