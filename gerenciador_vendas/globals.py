MACHINE_ID = 1

DATABASE_NAME = "gerenciador_vendas.db"

USER_TABLE_NAME = "usuarios"
USER_TABLE_COLUMNS_NAMES_TYPES = {
    "user_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "cpf": "TEXT NOT NULL",
    "nome": "TEXT NOT NULL",
    "telefone": "TEXT NOT NULL",
    "email": "TEXT",
}

PRODUCT_TABLE_NAME = "produtos"
PRODUCT_TABLE_COLUMNS_NAMES_TYPES = {
    "produto_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "nome": "TEXT NOT NULL",
    "quant_estoque": "INTEGER NOT NULL",
    "descricao": "TEXT",
}

PRICES_TABLE_NAME = "precos"
PRICES_TABLE_COLUMNS_NAMES_TYPES = {
    "preco_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "produto_id": "INTEGER NOT NULL",
    "preco": "REAL NOT NULL",
    "data_inicio": "TEXT NOT NULL",
}

SALES_TABLE_NAME = "vendas"
SALES_TABLE_COLUMNS_NAMES_TYPES = {
    "venda_id": "INTEGER NOT NULL",
    "user_id": "INTEGER NOT NULL",
    "produto_id": "INTEGER NOT NULL",
    "quantidade": "INTEGER NOT NULL",
    "preco": "REAL NOT NULL",
    "preco_id": "INTEGER NOT NULL",
    "data_venda": "TEXT NOT NULL",
    "valor_total": "REAL NOT NULL",
}

DICT_TABLES_NAMES_COLUMNS_NAMES_TYPES = {
    USER_TABLE_NAME: USER_TABLE_COLUMNS_NAMES_TYPES,
    PRODUCT_TABLE_NAME: PRODUCT_TABLE_COLUMNS_NAMES_TYPES,
    PRICES_TABLE_NAME: PRICES_TABLE_COLUMNS_NAMES_TYPES,
    SALES_TABLE_NAME: SALES_TABLE_COLUMNS_NAMES_TYPES,
}


if __name__ == "__main__":
    for name, columns_names_types in DICT_TABLES_NAMES_COLUMNS_NAMES_TYPES.items():
        print("Tabela:", name)
        print("Colunas:")
        for column_name, column_type in columns_names_types.items():
            print(column_name, column_type)
            print("---------------------------------")
        print("----------------------------------------------------------------")
