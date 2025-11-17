from typing import Callable

from src.models import User
from src.repositories import UserRepository
from src.security import PasswordManager
from src.validators import email_validator, password_validator


class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_manager: PasswordManager,
        email_validator: Callable[[str], tuple[bool, str]],
        password_validator: Callable[[str], tuple[bool, str]],
    ):
        self._user_repository = user_repository
        self._password_manager = password_manager
        self._email_validator = email_validator
        self._password_validator = password_validator

    def execute(
        self, email: str, password: str
    ) -> tuple[User | None, Exception | None]:

        if self._user_repository.exists(email):
            return None, ValueError('Usuário já existe')

        valid, msg = self._email_validator(email)
        if not valid:
            return None, ValueError(msg)

        valid, msg = self._password_validator(password)
        if not valid:
            return None, ValueError(msg)

        hash_password, salt = self._password_manager.hash_password(password)
        user = User(email=email, password=hash_password, salt=salt)
        self._user_repository.save(user)
        return user, None

    @staticmethod
    def factory():
        return RegisterUserUseCase(
            UserRepository(),
            PasswordManager(),
            email_validator,
            password_validator,
        )
