class Role:
    ADMIN = 'ADMIN'
    USER = 'USER'


class User:
    def __init__(self, email: str, password: str, salt: str):
        self._email = email
        self._password = password
        self._salt = salt
        self._role = Role.USER

    def __str__(self):
        return f'Usuário: {self._email} {self._role}'

    def __repr__(self):
        return self.__str__()

    @property
    def email(self):
        return self._email

    # @email.setter
    # def email(self, value):
    #     self._email = value

    @property
    def password(self):
        return self._password

    # @password.setter
    # def password(self, value):
    #     self._password = value

    @property
    def salt(self):
        return self._salt

    # @salt.setter
    # def salt(self, value):
    #     self._salt = value

    # @property
    # def username(self):
    #     return self._username

    # @username.setter
    # def username(self, value):
    #     self._username = value

    # @property
    # def role(self):
    #     return self._role

    # @role.setter
    # def role(self, value):
    #     self._role = value
