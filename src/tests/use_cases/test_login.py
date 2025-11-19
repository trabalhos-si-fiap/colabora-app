import sqlite3

from src.repositories.user import UserRepository
from src.security.password import PasswordManager
from src.use_cases.login import LoginUseCase


def test_login_with_valid_credentials(
    db_connection: sqlite3.Connection, registered_user
):
    """
    Testa o cenário de sucesso, onde um usuário com credenciais corretas
    consegue fazer login.
    """
    # --- Arrange ---
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    login_uc = LoginUseCase(user_repo, password_manager)

    user, password = registered_user

    # --- Act ---
    logged_in_user, error = login_uc.execute(user.email, password)

    # --- Assert ---
    assert error is None
    assert logged_in_user is not None
    assert logged_in_user.id == user.id
    assert logged_in_user.email == user.email


def test_login_with_invalid_password(
    db_connection: sqlite3.Connection, registered_user
):
    """
    Testa a falha de login quando a senha está incorreta.
    Cobre o `else` do `check_password`.
    """
    # --- Arrange ---
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    login_uc = LoginUseCase(user_repo, password_manager)

    user, _ = registered_user

    # --- Act ---
    logged_in_user, error = login_uc.execute(user.email, 'wrong-password')

    # --- Assert ---
    assert logged_in_user is None
    assert error == 'Credenciais inválidas.'


def test_login_with_non_existent_user(db_connection: sqlite3.Connection):
    """
    Testa a falha de login quando o e-mail não está cadastrado.
    Cobre o `if user is None:`.
    """
    # --- Arrange ---
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    login_uc = LoginUseCase(user_repo, password_manager)

    # --- Act ---
    logged_in_user, error = login_uc.execute(
        'no-one@example.com', 'any-password'
    )

    # --- Assert ---
    assert logged_in_user is None
    assert error == 'Credenciais inválidas.'
