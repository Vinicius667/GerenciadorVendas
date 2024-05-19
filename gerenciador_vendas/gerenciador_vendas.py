import os
import sqlite3
from typing import Dict, List

if __name__ == "__main__":
    import globals
    import structures
else:
    from gerenciador_vendas import globals, structures  # ,error_codes


def was_table_created(nome: str, cursor) -> bool:
    """Checa se a tabela com o nome passado foi criada no banco de dados.

    Args:
        name (str): Nome da tabela a ser checada.
    """
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome}'"
    )
    result = cursor.fetchone()
    return result is not None


def create_tables(dict_tables_names_columns_names_types: Dict) -> bool:
    """Cria as tabelas no banco de dados.

    Args:
        dict_tables_names_columns_names_types (Dict): Dicionario com o nome das tabelas e suas colunas.
    """
    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()
    for (
        table_name,
        columns_names_types,
    ) in dict_tables_names_columns_names_types.items():
        if not was_table_created(table_name, cursor):
            col_names_types = ", ".join(
                [
                    f"{column_name} {column_type}"
                    for column_name, column_type in columns_names_types.items()
                ]
            )
            sql_query = f"CREATE TABLE {table_name} ({col_names_types})"
            cursor.execute(sql_query)
    connection.commit()
    connection.close()
    return True


def add_new_user(nome: str, cpf: str, telefone: str, email: str = "") -> str:
    """Adiciona um novo usuario ao banco de dados. Checa se o usuario ja existe, caso exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.

    Args:
        nome (str): Nome do usuario.
        cpf (str): CPF do usuario.
        telefone (str): Telefone do usuario.
        email (str): Email do usuario.
    """
    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {globals.USER_TABLE_NAME} WHERE cpf = '{cpf}'")
    fetch = cursor.fetchone()
    if fetch is not None:
        connection.close()
        return "001"
    cursor.execute(
        f"INSERT INTO {globals.USER_TABLE_NAME} (nome, cpf, telefone, email) VALUES ('{nome}', '{cpf}', '{telefone}', '{email}')"
    )
    connection.commit()
    connection.close()
    return "000"


def get_user_info(cpf: str) -> structures.UserInfo:
    """Retorna um dicionario com as informacoes do usuario com o CPF passado.

    Args:
        cpf (str): CPF do usuario.
    """
    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {globals.USER_TABLE_NAME} WHERE cpf = '{cpf}'")
    fetch = cursor.fetchone()
    column_names = [description[0] for description in cursor.description]
    connection.close()
    if fetch is None:
        return structures.UserInfo(False)
    else:
        dict_result = dict(zip(column_names, fetch))
        return structures.UserInfo(True, **dict_result)


def update_user_info(cpf: str, **kwargs) -> str:
    """Atualiza as informacoes do usuario com o CPF passado. Checa se o usuario existe, caso nao exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.

    Args:
        cpf (str): CPF do usuario.
    """

    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {globals.USER_TABLE_NAME} WHERE cpf = '{cpf}'")
    fetch = cursor.fetchone()
    if fetch is None:
        connection.close()
        return "001"
    set_values = ", ".join([f"{key} = '{value}'" for key, value in kwargs.items()])
    cursor.execute(
        f"UPDATE {globals.USER_TABLE_NAME} SET {set_values} WHERE cpf = '{cpf}'"
    )
    connection.commit()
    connection.close()
    return "000"


def delete_user(cpf: str) -> str:
    """Deleta um usuario do banco de dados. Checa se o usuario existe, caso nao exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.

    Args:
        cpf (str): CPF do usuario.
    """
    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {globals.USER_TABLE_NAME} WHERE cpf = '{cpf}'")
    fetch = cursor.fetchone()
    if fetch is None:
        connection.close()
        return "001"
    cursor.execute(f"DELETE FROM {globals.USER_TABLE_NAME} WHERE cpf = '{cpf}'")
    connection.commit()
    connection.close()
    return "000"


def get_list_users() -> List[structures.UserInfo]:
    """Retorna uma lista com todos os usuarios do banco de dados."""
    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {globals.USER_TABLE_NAME}")
    fetch = cursor.fetchall()
    connection.close()
    list_users = []
    column_names = [description[0] for description in cursor.description]
    for user in fetch:
        list_users.append(structures.UserInfo(True, **dict(zip(column_names, user))))
    return list_users


def add_new_product(nome: str, preco: float, quant_estoque: int, descricao: str) -> str:
    """Adiciona um novo produto ao banco de dados. Checa se o produto ja existe, caso exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.

    Args:
        nome (str): Nome do produto.
        preco (float): Preco do produto.
        quant_estoque (int): Quantidade em estoque do produto.
        descricao (str): Descricao do produto.
    """
    if preco <= 0:
        return "006"

    nome = nome.strip().upper()
    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {globals.PRODUCT_TABLE_NAME} WHERE nome = '{nome}'")
    fetch = cursor.fetchone()
    if fetch is not None:
        connection.close()
        return "008"
    cursor.execute(
        f"INSERT INTO {globals.PRODUCT_TABLE_NAME} (nome, quant_estoque, descricao) VALUES ('{nome}', {quant_estoque}, '{descricao}')"
    )
    cursor.execute(
        f"SELECT produto_id FROM {globals.PRODUCT_TABLE_NAME} WHERE nome = '{nome}'"
    )
    fetch = cursor.fetchone()
    produto_id = fetch[0]
    cursor.execute(
        f"INSERT INTO {globals.PRICES_TABLE_NAME} (produto_id, preco, data_inicio) VALUES ({produto_id}, {preco}, date('now'))"
    )
    connection.commit()
    connection.close()
    return "000"


def get_product_info(*produtos_id) -> structures.ProductsList:
    """Retorna um dicionario com as informacoes do produto com o nome passado.

    Args:
        nome (str): Nome do produto.
    """
    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()

    produtos_id = [str(produto_id) for produto_id in produtos_id]
    # Faz merge das tabelas produtos e precos pelo produto_id pegando o preço mais recente removendo duplicadas de produtos
    cursor.execute(
        f'SELECT * FROM {globals.PRODUCT_TABLE_NAME} JOIN (SELECT * FROM {globals.PRICES_TABLE_NAME} WHERE preco_id IN (SELECT MAX(preco_id) FROM {globals.PRICES_TABLE_NAME} GROUP BY produto_id)) USING (produto_id) WHERE produto_id IN ({", ".join(produtos_id)}) ORDER BY produto_id ASC'
    )

    fetch = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    connection.close()

    list_products = structures.ProductsList()

    for product in fetch:
        dict_result = dict(zip(column_names, product))
        list_products.append(structures.ProductInfo(True, **dict_result))

    return list_products


def _aux_update_price(cursor, produto_id: int, preco: float) -> str:
    """Atualiza o preco do produto com o id passado.

    Args:
        produto_id (int): Id do produto.
        preco (float): Preco do produto.
    """
    if preco <= 0:
        return "006"

    cursor.execute(
        f"SELECT * FROM {globals.PRODUCT_TABLE_NAME} WHERE produto_id = {produto_id}"
    )
    fetch = cursor.fetchone()
    if fetch is None:
        return "004"
    cursor.execute(
        f"INSERT INTO {globals.PRICES_TABLE_NAME} (produto_id, preco, data_inicio) VALUES ({produto_id}, {preco}, date('now'))"
    )
    return "000"


def update_product_info(produto_id: int, **kwargs) -> str:
    """Atualiza as informacoes do produto com o nome passado. Checa se o produto existe, caso nao exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.

    Args:
        nome (str): Nome do produto.
    """

    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()

    if "preco" in kwargs:
        preco = kwargs.pop("preco")
        print(f"preco = {preco}")
        if preco <= 0:
            return "006"
        return_code = _aux_update_price(cursor, produto_id, preco)
        print(f"return_code = {return_code}")

        if return_code != "000":
            connection.close()
            return return_code

    if not kwargs:
        connection.commit()
        connection.close()
        return "000"

    cursor.execute(
        f"SELECT * FROM {globals.PRODUCT_TABLE_NAME} WHERE produto_id = {produto_id}"
    )
    fetch = cursor.fetchone()
    if fetch is None:
        connection.close()
        return "004"
    set_values = ", ".join([f"{key} = '{value}'" for key, value in kwargs.items()])
    cursor.execute(
        f"UPDATE {globals.PRODUCT_TABLE_NAME} SET {set_values} WHERE produto_id = {produto_id}"
    )
    connection.commit()
    connection.close()
    return "000"


def add_product_sales_cart(
    produto_id: int, quantidade: int, sales_info: structures.SaleInfo
) -> str:
    """Adiciona uma nova venda ao carrinho. Checa se o produto existe, caso nao exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.
    Args:
        produto_id (int): Id do produto.
        quantidade (int): Quantidade de produtos vendidos.
        sales_info (structures.SaleInfo): Informacoes da venda.
    """

    if produto_id in sales_info:
        sales_info.add_new_product(produto_id, quantidade)
        return "000"

    else:
        list_products = get_product_info(produto_id)
        if not list_products.products:
            return "004"
        else:
            product = list_products.products[0]
            sales_info.add_new_product(
                produto_id,
                quantidade,
                preco=product.preco,  # type: ignore
                nome=product.nome,  # type: ignore
                preco_id=product.preco_id,  # type: ignore
            )
            return "000"


if __name__ == "__main__":
    os.remove(globals.DATABASE_NAME)

    # what
    print("Criando tabelas...")
    create_tables(globals.DICT_TABLES_NAMES_COLUMNS_NAMES_TYPES)
    print("--------------------")

    print("Adicionando usuarios...")
    fake_users = [
        ["João", "123.456.789-00", "1234-5678", "joao@email.com"],
        ["Maria", "987.654.321-00", "9876-5432", "maria@email.com"],
        ["José", "111.222.333-44", "1111-2222", "jose@email.com"],
    ]
    for user in fake_users:
        print(f"{user} -> ", end="")
        print(add_new_user(*user))
    print("--------------------")

    print("Deletando usuarios...")
    list_cpfs = [fake_users[-1][1]] + ["000.000.000-00"]

    for cpf in list_cpfs:
        print(f"{cpf} -> ", end="")
        print(delete_user(cpf))
    print("--------------------")

    print("Adiciona usuario já cadastrado...")
    print(add_new_user("João", "123.456.789-00", "1234-5678", "joao123@email.com"))
    print("--------------------")

    print(get_list_users())

    print("--------------------")

    products = [
        ["Arroz", 33.0, 66, "Arroz branco"],
        ["Feijão", 8.0, 100, "Feijão carioca"],
        ["Macarrão", 5.0, 100, "Macarrão de trigo"],
    ]

    for product in products:
        print(f"{product[0]} -> ", end="")
        print(add_new_product(*product))

    update_product_info(1, quant_estoque=10, descricao="Arroz integral")

    print("--------------------")
    print(
        get_product_info(1, 2, 3)
        .get_table()
        .to_string(index=False, justify="center", max_colwidth=40)
    )
