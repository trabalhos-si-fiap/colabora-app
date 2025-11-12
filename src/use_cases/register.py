from src.models import User
from src.repositories import UserRepository
from src.security import PasswordManager


class RegisterUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self):
        print("=== Bem vindo ao app xpto === ")
        print("=== Registro de novo usuário === ")
        
        username = input("Digite o seu nome de usuário: ")
        password = input("Digite a sua senha: ")
        
        
        hash_password, salt = PasswordManager().hash_password(password)

        new_user = User(username, hash_password, salt)
        
        self.user_repository.save(new_user)
    

    @staticmethod
    def factory():
        return RegisterUseCase(UserRepository())