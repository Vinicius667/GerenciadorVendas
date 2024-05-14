DATABASE_NAME = 'gerenciador_vendas.db'

USER_TABLE_NAME = 'usuarios'
USER_TABLE_COLUMNS_NAMES_TYPES = {'user_id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 'cpf': 'TEXT NOT NULL', 'nome': 'TEXT NOT NULL', 'telefone': 'TEXT NOT NULL', 'email': 'TEXT'}

PRODUCT_TABLE_NAME = 'produtos'
PRODUCT_TABLE_COLUMNS_NAMES_TYPES = {'produto_id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 'nome': 'TEXT NOT NULL', 'preco': 'REAL NOT NULL', 'quant_estoque': 'INTEGER NOT NULL', 'descricao': 'TEXT'}

SALES_TABLE_NAME = 'vendas'
SALES_TABLE_COLUMNS_NAMES_TYPES = {'venda_id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 'user_id': 'INTEGER NOT NULL', 'produto_id': 'INTEGER NOT NULL', 'data_venda': 'TEXT NOT NULL', 'quantidade': 'INTEGER NOT NULL'}

DICT_TABLES_NAMES_COLUMNS_NAMES_TYPES = {USER_TABLE_NAME: USER_TABLE_COLUMNS_NAMES_TYPES, 
                                         PRODUCT_TABLE_NAME: PRODUCT_TABLE_COLUMNS_NAMES_TYPES, 
                                         SALES_TABLE_NAME: SALES_TABLE_COLUMNS_NAMES_TYPES}


for name, columns_names_types in DICT_TABLES_NAMES_COLUMNS_NAMES_TYPES.items():
    print("Tabela:", name)
    print("Colunas:")
    for column_name, column_type in columns_names_types.items():
        print(column_name, column_type)
        print('---------------------------------')
    print('----------------------------------------------------------------')
