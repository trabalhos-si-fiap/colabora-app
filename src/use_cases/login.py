from typing import Optional

from src.models.users import User
from src.repositories import UserRepository
from src.security import PasswordManager


class LoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_manager: PasswordManager,
    ):
        self.user_repository = user_repository
        self.password_manager = password_manager

    def execute(
        self, email: str, password: str
    ) -> tuple[Optional[User], Optional[str]]:
        user = self.user_repository.get_by_email(email)

        msg = 'Credenciais inválidas.'

        if user is None:
            return None, msg

        if self.password_manager.check_password(password, user):
            return user, None
        else:
            return None, msg

    @staticmethod
    def factory():
        return LoginUseCase(UserRepository(), PasswordManager())
