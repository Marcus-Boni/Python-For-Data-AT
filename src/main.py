from datetime import datetime
from tabulate import tabulate
import csv
import os
from config import DATA_DIR, DB_PATH
from crud.crud_cliente import buscar_cliente, inserir_cliente
from crud.crud_produto import buscar_produto, atualizar_estoque
from crud.crud_compra import criar_compra
from crud.crud_item import criar_item
import sqlite3

CLIENTES_CSV = os.path.join(DATA_DIR, 'clientes.csv')
PRODUTOS_CSV = os.path.join(DATA_DIR, 'produtos.csv')

def initialize_database():
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    
    cursor.executescript("""
    DROP TABLE IF EXISTS cliente;                     
    DROP TABLE IF EXISTS produto;
    DROP TABLE IF EXISTS compra;
    DROP TABLE IF EXISTS item;
    
    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS produto (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS compra (
        id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        data_compra TEXT NOT NULL,
        id_cliente INTEGER NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
    );

    CREATE TABLE IF NOT EXISTS item (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT,
        quantidade INTEGER NOT NULL,
        id_compra INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        FOREIGN KEY (id_compra) REFERENCES compra(id_compra),
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
    );
    """)
    
    cursor.execute("DELETE FROM item WHERE 1=1")
    cursor.execute("DELETE FROM compra WHERE 1=1")
    cursor.execute("DELETE FROM produto WHERE 1=1")
    cursor.execute("DELETE FROM cliente WHERE 1=1")
    
    with open(CLIENTES_CSV, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cursor.execute("INSERT INTO cliente (id_cliente, nome) VALUES (?, ?)", 
                          (int(row[0]), row[1]))
    
    with open(PRODUTOS_CSV, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cursor.execute("""INSERT INTO produto 
                          (id_produto, nome, quantidade, preco) 
                          VALUES (?, ?, ?, ?)""",
                          (int(row[0]), row[1], int(row[2]), float(row[3])))
    
    conn.commit()
    conn.close()

def processar_cliente():
    while True:
        id_cliente = input("ID do cliente: ")
        if not id_cliente.isdigit():
            print("Erro: valor inválido")
            continue
        id_cliente = int(id_cliente)
        break
    
    cliente = buscar_cliente(id_cliente)
    if not cliente:
        nome = input("Nome do cliente: ")
        inserir_cliente(id_cliente, nome)
    
    data_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_compra = criar_compra(data_compra, id_cliente)
    
    itens = []
    while True:
        id_produto = input("ID do produto (ou 'fim' para finalizar): ")
        if id_produto.lower() == 'fim':
            if not itens:
                print("Erro: Adicione pelo menos um item.")
                continue
            break
        if not id_produto.isdigit() or int(id_produto) <= 0:
            print("Erro: ID inválido")
            continue
        id_produto = int(id_produto)
        produto = buscar_produto(id_produto)
        if not produto:
            print("Erro: produto não cadastrado")
            continue
        
        while True:
            quantidade = input("Quantidade (ou digite 'voltar' para escolher outro produto): ")
            if quantidade.lower() == 'voltar':
                break
            
            if not quantidade.isdigit() or int(quantidade) <= 0:
                print("Erro: quantidade inválida")
                continue
            quantidade = int(quantidade)
            if quantidade > produto['quantidade']:
                print(f"Erro: quantidade fora do estoque. Disponível: {produto['quantidade']}")
                print("Digite uma quantidade menor ou 'voltar' para escolher outro produto.")
                continue
            
            nova_quantidade = produto['quantidade'] - quantidade
            atualizar_estoque(id_produto, nova_quantidade)
            criar_item(quantidade, id_compra, id_produto)
            itens.append({
                'Produto': produto['nome'],
                'Quantidade': quantidade,
                'Preço Unitário': produto['preco'],
                'Total': quantidade * produto['preco']
            })
            break  
        
        continue

    print("\n" + "=" * 40)
    print("Nota Fiscal")
    print(f"Data: {data_compra}")
    print(f"Cliente ID: {id_cliente}")
    print(tabulate(itens, headers="keys", tablefmt="grid"))
    total = sum(item['Total'] for item in itens)
    print(f"\nTotal da Compra: R$ {total:.2f}")
    print("=" * 40 + "\n")

def gerar_extrato():
    conn = sqlite3.connect(DB_PATH)   
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.id_cliente, cli.nome, SUM(i.quantidade * p.preco) as total
        FROM compra c
        JOIN cliente cli ON c.id_cliente = cli.id_cliente
        JOIN item i ON c.id_compra = i.id_compra
        JOIN produto p ON i.id_produto = p.id_produto
        GROUP BY c.id_cliente
    """)
    clientes_vendas = cursor.fetchall()
    
    total_vendas = sum(row[2] for row in clientes_vendas) if clientes_vendas else 0
    
    cursor.execute("SELECT id_produto, nome FROM produto WHERE quantidade = 0")
    produtos_sem_estoque = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 40)
    print("Extrato do Caixa")
    print("=" * 40)
    
    print("\nClientes Atendidos:")
    if clientes_vendas:
        print(tabulate(clientes_vendas, headers=["ID Cliente", "Nome", "Total Gasto"], tablefmt="grid"))
    else:
        print("Nenhum cliente atendido.")
    
    print(f"\nTotal de Vendas: R$ {total_vendas:.2f}")
    
    print("\nProdutos Sem Estoque:")
    if produtos_sem_estoque:
        print(tabulate(produtos_sem_estoque, headers=["ID Produto", "Nome"], tablefmt="grid"))
    else:
        print("Nenhum produto sem estoque.")
    print("=" * 40 + "\n")

def main():
    initialize_database()
    
    while True:
        print("\nOpções:")
        print("1. Iniciar Atendimento")
        print("2. Fechar Caixa")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            processar_cliente()
        elif opcao == '2':
            gerar_extrato()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()