# tests/use_cases/test_register_user.py
import sqlite3

import pytest

from src.repositories.users import UserRepository
from src.security.password import PasswordManager
from src.use_cases.register import RegisterUserUseCase
from src.validators import email_validator, password_validator


def test_register_new_user_successfully(db_connection: sqlite3.Connection):
    """
    Testa se um novo usuário pode ser registrado com sucesso.
    """
    # --- Arrange (Preparação) ---
    # Instancia as dependências usando a conexão em memória da fixture
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()

    use_case = RegisterUserUseCase(
        user_repository=user_repo,
        password_manager=password_manager,
        email_validator=email_validator,
        password_validator=password_validator,
    )

    email = 'newuser@example.com'
    password = 'ValidPassword123*'

    # --- Act (Ação) ---
    user, error = use_case.execute(email, password)

    # --- Assert (Verificação) ---
    assert error is None
    assert user is not None
    assert user.id is not None
    assert user.email == email

    # Verifica se o usuário foi realmente salvo no banco
    saved_user = user_repo.get_by_id(user.id)
    assert saved_user is not None
    assert saved_user.email == email


def test_register_existing_user_should_fail(db_connection: sqlite3.Connection):
    """
    Testa que o registro falha se o e-mail já existir.
    """
    # --- Arrange (Preparação) ---
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    use_case = RegisterUserUseCase(
        user_repo, password_manager, email_validator, password_validator
    )

    # Cria um usuário pré-existente usando o mesmo use_case
    existing_email = 'existing@example.com'
    initial_user, error = use_case.execute(existing_email, 'anypassword*A1')

    # Garante que o primeiro usuário foi criado com sucesso
    assert error is None
    assert initial_user is not None
    assert user_repo.exists(existing_email) is True

    # --- Act (Ação) ---
    user, error = use_case.execute(existing_email, 'anotherpassword*B2')

    # --- Assert (Verificação)---
    assert user is None
    assert isinstance(error, ValueError)
    assert str(error) == 'Usuário já existe'


def test_register_user_with_invalid_email_format(
    db_connection: sqlite3.Connection,
):
    """
    Testa que o registro falha se o formato do e-mail for inválido.
    """
    # Arrange
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    use_case = RegisterUserUseCase(
        user_repo, password_manager, email_validator, password_validator
    )

    # Act
    user, error = use_case.execute('not-an-email', 'ValidPassword123*')

    # Assert
    assert user is None
    assert isinstance(error, ValueError)
    assert str(error) == 'E-mail deve conter "@".'


def test_register_user_with_invalid_password(
    db_connection: sqlite3.Connection,
):
    """
    Testa que o registro falha se a senha não atender aos critérios de segurança.
    """
    # Arrange
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    use_case = RegisterUserUseCase(
        user_repo, password_manager, email_validator, password_validator
    )

    # Act
    user, error = use_case.execute('valid.email@test.com', '123')

    # Assert
    assert user is None
    assert isinstance(error, ValueError)
    # A mensagem de erro exata pode variar dependendo da sua implementação do validador
    assert 'Senha deve ter no mínimo 8 caracteres.' == str(error)
