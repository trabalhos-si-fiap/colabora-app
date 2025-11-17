import sqlite3
from unittest.mock import patch

import pytest

from src.models.hability import Hability
from src.repositories.hability import HabilityRepository
from src.repositories.users import UserRepository
from src.security.password import PasswordManager
from src.use_cases.replace_password import ReplacePasswordUseCase
from src.validators import password_validator


def test_replace_password_successfully_and_preserve_habilities(
    db_connection: sqlite3.Connection, registered_user
):
    """
    Testa o cenário de sucesso: a senha é trocada e as habilidades do usuário
    são mantidas.
    """
    # --- Arrange ---
    user_repo = UserRepository(db_connection=db_connection)
    hability_repo = HabilityRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    use_case = ReplacePasswordUseCase(
        user_repo, password_manager, password_validator
    )

    user, _ = registered_user
    initial_password_hash = user.password

    hability1 = hability_repo.save(
        Hability(
            name='Gestão de Projetos',
            description='Desc 1',
            domain='Gestão',
        )
    )
    hability2 = hability_repo.save(
        Hability(
            name='Desenvolvimento Web',
            description='Desc 2',
            domain='Tecnologia',
        )
    )

    # Associa as habilidades ao usuário e salva
    user.habilities = [hability1, hability2]
    user_repo.save(user)

    # Confirma que as habilidades foram salvas
    habilities_before = user_repo.get_habilities_for_user(user_id=user.id)
    assert len(habilities_before) == 2

    # --- Act ---
    new_password = 'NewStrongPassword456!'
    success, error = use_case.execute(id=user.id, new_password=new_password)

    # --- Assert ---
    assert success is True
    assert error is None

    # Verifica se a senha foi realmente alterada no banco
    updated_user = user_repo.get_by_id(user.id)
    assert updated_user.password != initial_password_hash
    assert password_manager.check_password(new_password, updated_user) is True

    # A verificação mais importante: as habilidades foram preservadas
    habilities_after = user_repo.get_habilities_for_user(user_id=user.id)
    assert len(habilities_after) == 2
    assert {h.id for h in habilities_after} == {hability1.id, hability2.id}


def test_replace_password_for_non_existent_user(
    db_connection: sqlite3.Connection,
):
    """
    Testa a falha ao tentar trocar a senha de um usuário que não existe.
    Cobre o `if not self.user_repository.exists(id):`
    """
    # Arrange
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    use_case = ReplacePasswordUseCase(
        user_repo, password_manager, password_validator
    )
    non_existent_id = 999

    # Act
    success, error = use_case.execute(id=non_existent_id, new_password='any')

    # Assert
    assert success is False
    assert error == 'Usuário não encontrado.'


def test_replace_password_with_invalid_new_password(
    db_connection: sqlite3.Connection, registered_user
):
    """
    Testa a falha ao usar uma nova senha que não passa na validação.
    Cobre o `if err:`
    """
    # Arrange
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    use_case = ReplacePasswordUseCase(
        user_repo, password_manager, password_validator
    )
    user, _ = registered_user

    # Act
    success, error = use_case.execute(id=user.id, new_password='123')

    # Assert
    assert success is False
    assert 'Senha deve ter no mínimo 8 caracteres.' in error


def test_replace_password_fails_if_user_vanishes_between_checks(
    db_connection: sqlite3.Connection, registered_user
):
    """
    Testa o caso de borda onde o usuário existe na verificação `exists()`,
    mas não é encontrado na busca seguinte (ex: race condition).
    Cobre o `if not user:`
    """
    # Arrange
    user_repo = UserRepository(db_connection=db_connection)
    password_manager = PasswordManager()
    use_case = ReplacePasswordUseCase(
        user_repo, password_manager, password_validator
    )
    user, _ = registered_user

    # Garante que o usuário existe inicialmente
    assert user_repo.exists(user.id) is True

    # Simula que o usuário "desapareceu" entre a verificação `exists` e a `get`
    with patch.object(
        user_repo, 'get_by_id_with_habilities', return_value=None
    ):
        # Act
        success, error = use_case.execute(
            id=user.id, new_password='any-password'
        )

    # Assert
    assert success is False
    assert error == 'Usuário não encontrado.'
