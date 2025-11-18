from datetime import date

from loguru import logger

from src.models import Hability, Project


class Role:
    ADMIN = 'ADMIN'
    USER = 'USER'


class User:
    def __init__(
        self,
        email: str,
        password: str,
        salt: str,
        first_name: str = None,
        last_name: str = None,
        birth_date: str = None,
        phone: str = None,
        id: int = None,
        role: str = None,
    ):
        self.id = id
        self._email = email
        self._password = password
        self._salt = salt
        self._role = Role.USER if role is None else role

        self._first_name = first_name
        self._last_name = last_name
        self._birth_date = birth_date   # Mantemos como string (ISO)
        self._phone = phone

        self._habilities: list[Hability] = list()
        self._projects: list[Project] = list()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self._email,
            'password': self._password,
            'salt': self._salt,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'birth_date': self._birth_date,
            'phone': self._phone,
            'role': self._role,
            'habilities': self._habilities,
            'projects': self._projects,
        }

    def __str__(self):
        return f'Usuário: {self._email} {self._role}'

    def __repr__(self):
        return self.__str__()

    def age(self) -> int | None:
        if self._birth_date is None:
            return None

        today = date.today()
        return (
            today.year
            - self._birth_date.year
            - (
                (today.month, today.day)
                < (self._birth_date.month, self._birth_date.day)
            )
        )

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key == 'habilities' and value is not None:
                self.habilities = value
            elif hasattr(self, f'_{key}') and value is not None:
                setattr(self, key, value)

    def add_hability(self, hability: Hability) -> None:
        if hability is None:
            return
        self._habilities.append(hability)
        logger.debug(
            f'Add hability {hability.id} to user {self.id} | {len(self.habilities)=}'
        )

    def remove_hability(self, hability: Hability) -> None:
        if hability is None:
            return

        if hability in self._habilities:
            self._habilities.remove(hability)

    def has_hability(self, hability: Hability) -> bool:
        if hability is None:
            return False
        return hability in self._habilities

    def is_subscribed_to(self, project: Project) -> bool:
        """Verifica se o usuário está inscrito em um projeto específico."""
        if project is None or project.id is None:
            return False
        return any(p.id == project.id for p in self._projects)

    def add_project(self, project: Project) -> None:
        """Inscreve o usuário em um projeto."""
        if project and not self.is_subscribed_to(project):
            self._projects.append(project)

    def remove_project(self, project: Project) -> None:
        """Remove a inscrição do usuário de um projeto."""
        self._projects = [p for p in self._projects if p.id != project.id]

    @property
    def salt(self):
        return self._salt

    @salt.setter
    def salt(self, value):
        self._salt = value

    @property
    def projects(self):
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = value

    @property
    def habilities(self):
        return self._habilities

    @habilities.setter
    def habilities(self, value):
        self._habilities = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value: Role):
        self._role = value
