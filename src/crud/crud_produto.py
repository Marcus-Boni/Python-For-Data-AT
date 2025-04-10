import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db_connection

def buscar_produto(id_produto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_produto, nome, quantidade, preco FROM produto WHERE id_produto = ?", (id_produto,))
    row = cursor.fetchone()
    conn.close()
    return {
        'id_produto': row[0],
        'nome': row[1],
        'quantidade': row[2],
        'preco': row[3]
    } if row else None

def atualizar_estoque(id_produto, nova_quantidade):
    conn = get_db_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute("UPDATE produto SET quantidade = ? WHERE id_produto = ?", (nova_quantidade, id_produto))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erro ao atualizar estoque: {e}")
    finally:
        conn.close()