from typing import Callable

from src.repositories.user import UserRepository
from src.security.password import PasswordManager
from src.validators import password_validator


class ReplacePasswordUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_manager: PasswordManager,
        password_validator: Callable[[str], tuple[bool, str]],
    ):
        self.user_repository = user_repository
        self.password_manager = password_manager
        self.password_validator = password_validator

    def execute(
        self, id: int, new_password: str
    ) -> tuple[bool | None, str | None]:
        if not self.user_repository.exists(id):
            return False, 'Usuário não encontrado.'

        user = self.user_repository.get_by_id_with_all_relations(id)
        if not user:
            return False, 'Usuário não encontrado.'

        valid, err = self.password_validator(new_password)

        if err:
            return False, err

        new_hash_password, new_salt = self.password_manager.hash_password(
            new_password
        )
        user.password = new_hash_password
        user.salt = new_salt
        self.user_repository.save(user)

        return True, None

    @staticmethod
    def factory():
        return ReplacePasswordUseCase(
            UserRepository(), PasswordManager(), password_validator
        )
