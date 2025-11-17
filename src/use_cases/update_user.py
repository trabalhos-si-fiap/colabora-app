from src.models import User
from src.repositories import UserRepository


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, email: str, **kwargs) -> User | None:
        if email is None:
            return

        if not self._user_repository.exists(email):
            return

        user = self._user_repository.find_user(email)

        user.update(**kwargs)

        self._user_repository.save(user)

        return user

    @staticmethod
    def factory():
        return UpdateUserUseCase(UserRepository())
