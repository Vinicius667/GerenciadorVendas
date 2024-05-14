import sqlite3
from typing import Dict

from gerenciador_vendas import globals, structures  # ,error_codes


def was_table_created(nome: str, cursor) -> bool:
    """ Checa se a tabela com o nome passado foi criada no banco de dados.

    Args:
        name (str): Nome da tabela a ser checada.
    """
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome}'")
    result = cursor.fetchone()
    return result is not None


def create_tables(dict_tables_names_columns_names_types: Dict) -> bool:
    """ Cria as tabelas no banco de dados.

    Args:
        dict_tables_names_columns_names_types (Dict): Dicionario com o nome das tabelas e suas colunas.
    """
    connection = sqlite3.connect(globals.DATABASE_NAME)
    cursor = connection.cursor()
    for table_name, columns_names_types in dict_tables_names_columns_names_types.items():
        if not was_table_created(table_name, cursor):
            col_names_types = ', '.join([f'{column_name} {column_type}' for column_name, column_type in columns_names_types.items()])
            sql_query = f'CREATE TABLE {table_name} ({col_names_types})'
            print(sql_query)
            cursor.execute(sql_query)
    connection.commit()
    connection.close()
    return True


create_tables(globals.DICT_TABLES_NAMES_COLUMNS_NAMES_TYPES)


def add_new_user(nome: str, cpf: str, telefone: str,
                 email: str = '') -> str:
    """ Adiciona um novo usuario ao banco de dados. Checa se o usuario ja existe, caso exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.

    Args:
        nome (str): Nome do usuario.
        cpf (str): CPF do usuario.
        telefone (str): Telefone do usuario.
        email (str): Email do usuario.
    """

    return ''


def check_user_info(cpf: str) -> structures.UserInfo:
    """ Retorna um dicionario com as informacoes do usuario com o CPF passado.

    Args:
        cpf (str): CPF do usuario.
    """

    return structures.UserInfo(False)


def update_user_info(cpf: str, **kwargs) -> str:
    """ Atualiza as informacoes do usuario com o CPF passado. Checa se o usuario existe, caso nao exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.

    Args:
        cpf (str): CPF do usuario.
    """

    return '000'


def delete_user(cpf: str) -> str:
    """ Deleta um usuario do banco de dados. Checa se o usuario existe, caso nao exista retorna um codigo de erro. Caso exista, retorna um codigo de sucesso.

    Args:
        cpf (str): CPF do usuario.
    """

    return '000'
