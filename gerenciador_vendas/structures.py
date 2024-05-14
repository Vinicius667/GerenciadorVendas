class UserInfo:
    def __init__(self, was_found, **kwargs):
        self.was_found = was_found
        if was_found:
            self.cpf = kwargs['cpf']
            self.email = kwargs['email']
            self.telefone = kwargs['telefone']
            self.nome = kwargs['nome']
