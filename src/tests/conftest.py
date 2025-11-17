# tests/conftest.py
import json
import sqlite3
from pathlib import Path

import pytest

from src.models.users import User
from src.repositories.database import Database
from src.repositories.hability import HabilityRepository
from src.repositories.users import UserRepository
from src.security.password import PasswordManager
from src.use_cases.register import RegisterUserUseCase
from src.validators import email_validator, password_validator

# Ajuste o caminho para encontrar a pasta 'seeds' a partir da raiz do projeto
SEEDS_PATH = Path(__file__).parent.parent / 'seeds'


@pytest.fixture
def db_connection() -> sqlite3.Connection:
    """
    Fixture do Pytest para criar e gerenciar um banco de dados SQLite em memória.
    """
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row

    db_instance = Database(connection=conn)

    # Disponibiliza a conexão para o teste
    yield conn

    # --- Limpeza (Teardown) ---
    # Fecha a conexão, destruindo o banco em memória
    conn.close()
    # Reseta o Singleton para garantir que o próximo teste crie uma nova instância
    Database._instance = None
    Database._initialized = False


@pytest.fixture
def registered_user(
    db_connection: sqlite3.Connection,
) -> tuple[User, str]:
    """
    Fixture que registra um usuário no banco de dados em memória e o retorna
    junto com sua senha em texto plano.
    """
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    register_uc = RegisterUserUseCase(
        user_repository=user_repo,
        password_manager=password_manager,
        email_validator=email_validator,
        password_validator=password_validator,
    )
    email = 'test.user@example.com'
    password = 'ValidPassword123*'
    user, error = register_uc.execute(email, password)
    assert error is None, 'Falha ao criar usuário na fixture'
    return user, password
