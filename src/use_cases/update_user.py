from src.models import User
from src.repositories import UserRepository


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, id: int, **kwargs) -> User | None:
        if id is None:
            return

        if not self._user_repository.exists(id):
            return

        user = self._user_repository.get_by_id_with_habilities(id)
        if not user:
            # Caso de borda: usuário deletado entre as verificações.
            return

        user.update(**kwargs)

        self._user_repository.save(user)

        return user

    @staticmethod
    def factory():
        return UpdateUserUseCase(UserRepository())
