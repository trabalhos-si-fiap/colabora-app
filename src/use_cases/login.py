
from src.exceptions import UserNotFoundException
from src.repositories import UserRepository
from src.security import PasswordManager


class LoginUseCase:
    def __init__(self, user_repository, password_manager):
        self.user_repository = user_repository
        self.password_manager = password_manager

    def execute(self):
        print("=== Login ===")
        username = input("Digite seu nome de usuário: ")
        password = input("Digite sua senha: ")

        try:
            user = self.user_repository.find_user(username)
            if self.password_manager.check_password(password, user):
                print(f"Bem-vindo, {user.username}!")
                return user
            else:
                print("Login falhou. Senha incorreta.")
                return None
        except UserNotFoundException:
            print("Login falhou. Usuário não encontrado.")
            return None

    @staticmethod
    def factory():
        return LoginUseCase(UserRepository(), PasswordManager())
