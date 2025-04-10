# Sistema de Gerenciamento de Mercado

Este projeto implementa um sistema de gerenciamento de mercado com funcionalidades de cadastro de clientes, controle de estoque, processamento de compras e geração de relatórios, utilizando SQLite como banco de dados.

## Estrutura do Projeto

```
Python_Dados_AT/
│
├── src/
│   ├── main.py                # Arquivo principal da aplicação
│   │
│   └── crud/                  # Módulos de operações CRUD
│       ├── crud_cliente.py    # Operações de cliente
│       ├── crud_produto.py    # Operações de produto
│       ├── crud_compra.py     # Operações de compra
│       └── crud_item.py       # Operações de item de compra
│
├── data/
│   ├── clientes.csv           # Dados iniciais de clientes
│   └── produtos.csv           # Dados iniciais de produtos
│
├── README.md                  # Documentação do projeto
└── requirements.txt           # Dependências do projeto
```

## Funcionalidades

- **Gestão de Clientes**: Cadastro e consulta de clientes
- **Gestão de Produtos**: Consulta e atualização de estoque
- **Processamento de Compras**: Registro de compras com múltiplos itens
- **Emissão de Notas Fiscais**: Geração de nota fiscal detalhada após cada compra
- **Relatórios**: Extrato de caixa com informações sobre vendas e produtos sem estoque

## Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- **cliente**: Armazena informações dos clientes
- **produto**: Armazena informações dos produtos, incluindo estoque e preço
- **compra**: Registra as compras realizadas
- **item**: Registra os itens de cada compra

## Requisitos

- Python 3.x
- Pacotes Python (listados em requirements.txt):
  - sqlite3
  - tabulate

## Instalação

1. Clone o repositório ou baixe os arquivos do projeto

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

1. Execute o programa principal:
```bash
python src/main.py
```

2. No menu principal, você terá as seguintes opções:
   - **1. Iniciar Atendimento**: Iniciar um processo de compra
   - **2. Fechar Caixa**: Gerar relatório de vendas e encerrar o programa

### Fluxo de Compra

1. Informe o ID do cliente
2. Se o cliente não existir, você será solicitado a cadastrar um novo
3. Adicione produtos informando ID e quantidade
4. Digite 'fim' quando terminar de adicionar produtos
5. Uma nota fiscal será gerada com o detalhe da compra

### Relatório de Caixa

Ao selecionar a opção de fechar o caixa, o sistema gera um extrato com:
- Clientes atendidos e total gasto por cada um
- Valor total de vendas
- Produtos sem estoque

## Dados Iniciais

O sistema é inicializado com dados de:
- 3 clientes (do arquivo clientes.csv)
- 5 produtos (do arquivo produtos.csv)

## Desenvolvimento

Este projeto foi desenvolvido como atividade acadêmica para demonstrar o uso de:
- Python para desenvolvimento de aplicações
- Banco de dados SQLite
- Operações CRUD (Create, Read, Update, Delete)
- Processamento de arquivos CSV
- Formatação de saídas para console
