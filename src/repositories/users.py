import pickle
from typing import TypeAlias, TypedDict

from src import PICKLE_PATH
from src.exceptions import UserNotFoundException
from src.models.users import User

email_type: str


class UserRepository:
    class LoadUser(TypedDict):
        email: str
        user: User

    def __init__(self, pickle_path=PICKLE_PATH):
        self._file_name = pickle_path / 'users.pkl'
        self.users = self._load_users()

    def find_user(self, email: str):
        user = self.users.get(email)

        if user is not None:
            return user

        raise UserNotFoundException('Usuário não encontrado')

    def exists(self, email: str) -> bool:
        return email in self.users

    def _load_users(self) -> LoadUser:
        try:
            with open(self._file_name, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}

    def save(self, user: User) -> None:
        self.users[user.email] = user
        with open(self._file_name, 'wb') as f:
            pickle.dump(self.users, f)
