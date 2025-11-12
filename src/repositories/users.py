import pickle

from src import PICKLE_PATH
from src.exceptions import UserNotFoundException


class UserRepository:
    def __init__(self, pickle_path=PICKLE_PATH):
        self._filename = pickle_path / "users.pkl"
        self.users = self._load_users()

    def find_user(self, username):
        print(f"{self.users=}")
        for user in self.users:
            print(f"{user.username=} :: {username=}")
            if user.username == username:
                return user
        raise UserNotFoundException("Usuário não encontrado")
    
    def _load_users(self):
        try:
            with open(self._filename, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            print("DEU MERDA")
            return []

    def save(self, user):
        self.users.append(user)
        with open(self._filename, 'wb') as f:
            pickle.dump(self.users, f)
        print("Usuário salvo com sucesso!")