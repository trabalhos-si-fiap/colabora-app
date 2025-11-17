import pickle

from src import PICKLE_PATH
from src.exceptions import UserNotFoundException
from src.models.users import User


class UserRepository:
    def __init__(self, pickle_path=PICKLE_PATH):
        self._file_name = pickle_path / 'users.pkl'
        self.users = self._load_users()

    def find_user(self, email: str):
        for user in self.users:
            if user.email == email:
                return user
        raise UserNotFoundException('Usuário não encontrado')

    def exists(self, email: str) -> bool:
        for user in self.users:
            if user.email == email:
                return True
        return False

    def _load_users(self) -> list[User]:
        try:
            with open(self._file_name, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return []

    def save(self, user):
        self.users.append(user)
        with open(self._file_name, 'wb') as f:
            pickle.dump(self.users, f)
