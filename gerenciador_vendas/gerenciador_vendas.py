import sqlite3

from gerenciador_vendas import structures  # ,error_codes


def was_table_created(nome: str) -> bool:
    """ Checa se a tabela com o nome passado foi criada no banco de dados.

    Args:
        name (str): Nome da tabela a ser checada.
    """
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome}'")
    result = cursor.fetchone()
    connection.close()
    return result is not None


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


if __name__ == '__main__':
    database_name = 'database.db'
    # Cria a tabela de usuarios
    if not was_table_created('usuarios'):
        print('Criando tabela de usuarios...')
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, senha TEXT)')
        connection.commit()
        connection.close()
