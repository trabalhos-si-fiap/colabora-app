class User:
    def __init__(self, username: str, password: str, salt: str):
        self.username = username
        self.password = password
        self.salt = salt

    def __str__(self):
        return f'Usuário: {self.username}'

    def __repr__(self):
        return self.__str__()


class Admin(User):
    def __init__(self, username, password, is_admin=True):
        super().__init__(username, password)
        self.is_admin = is_admin
