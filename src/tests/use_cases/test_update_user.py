import sqlite3
from unittest.mock import patch

from src.models.hability import Hability
from src.repositories.hability import HabilityRepository
from src.repositories.users import UserRepository
from src.use_cases.update_user import UpdateUserUseCase


def test_update_user_basic_info_and_preserve_habilities(
    db_connection: sqlite3.Connection, registered_user
):
    """
    Testa a atualização de um campo simples (first_name) e verifica se as
    habilidades existentes do usuário são preservadas.
    """
    # --- Arrange ---
    user_repo = UserRepository(db_connection=db_connection)
    hability_repo = HabilityRepository(db_connection=db_connection)
    use_case = UpdateUserUseCase(user_repo)

    user, _ = registered_user

    # Cria e associa habilidades iniciais ao usuário
    h1 = hability_repo.save(
        Hability(name='Python', description='d1', domain='Tech')
    )
    h2 = hability_repo.save(
        Hability(name='SQL', description='d2', domain='Tech')
    )
    user.habilities = [h1, h2]
    user_repo.save(user)

    # Confirma o estado inicial
    user_before = user_repo.get_by_id_with_habilities(user.id)
    assert user_before.first_name is None
    assert len(user_before.habilities) == 2

    # --- Act ---
    updated_user = use_case.execute(
        id=user.id, first_name='John', last_name='Doe'
    )

    # --- Assert ---
    assert updated_user is not None
    assert updated_user.first_name == 'John'
    assert updated_user.last_name == 'Doe'

    # Verifica o estado final no banco de dados
    user_after = user_repo.get_by_id_with_habilities(user.id)
    assert user_after.first_name == 'John'
    assert (
        len(user_after.habilities) == 2
    ), 'As habilidades do usuário foram perdidas!'
    assert {h.id for h in user_after.habilities} == {h1.id, h2.id}


def test_update_user_habilities_list(
    db_connection: sqlite3.Connection, registered_user
):
    """
    Testa a substituição completa da lista de habilidades de um usuário.
    """
    # --- Arrange ---
    user_repo = UserRepository(db_connection=db_connection)
    hability_repo = HabilityRepository(db_connection=db_connection)
    use_case = UpdateUserUseCase(user_repo)

    user, _ = registered_user

    # Cria habilidades iniciais e novas
    h1 = hability_repo.save(
        Hability(name='Python', description='d1', domain='Tech')
    )
    h2 = hability_repo.save(
        Hability(name='SQL', description='d2', domain='Tech')
    )
    h3_new = hability_repo.save(
        Hability(name='Docker', description='d3', domain='DevOps')
    )
    h4_new = hability_repo.save(
        Hability(name='Git', description='d4', domain='Tools')
    )

    user.habilities = [h1, h2]
    user_repo.save(user)

    # Confirma o estado inicial
    habilities_before = user_repo.get_habilities_for_user(user.id)
    assert {h.id for h in habilities_before} == {h1.id, h2.id}

    # --- Act ---
    new_habilities = [h3_new, h4_new]
    use_case.execute(id=user.id, habilities=new_habilities)

    # --- Assert ---
    habilities_after = user_repo.get_habilities_for_user(user.id)
    assert len(habilities_after) == 2
    assert {h.id for h in habilities_after} == {h3_new.id, h4_new.id}


def test_update_non_existent_user(db_connection: sqlite3.Connection):
    """
    Testa que o caso de uso não faz nada e retorna None se o usuário não existir.
    """
    # Arrange
    user_repo = UserRepository(db_connection=db_connection)
    use_case = UpdateUserUseCase(user_repo)
    non_existent_id = 999

    # Garante que o usuário não existe
    assert user_repo.exists(non_existent_id) is False

    # Act
    result = use_case.execute(id=non_existent_id, first_name='Ghost')

    # Assert
    assert result is None


def test_update_user_fails_if_user_vanishes_between_checks(
    db_connection: sqlite3.Connection, registered_user
):
    """
    Testa o caso de borda onde o usuário existe na verificação `exists()`,
    mas não é encontrado na busca seguinte (ex: race condition).
    Cobre o `if not user:`
    """
    # Arrange
    user_repo = UserRepository(db_connection=db_connection)
    use_case = UpdateUserUseCase(user_repo)
    user, _ = registered_user

    # Garante que o usuário existe inicialmente
    assert user_repo.exists(user.id) is True

    # Simula que o usuário "desapareceu" entre a verificação `exists` e a `get`
    with patch.object(
        user_repo, 'get_by_id_with_habilities', return_value=None
    ):
        # Act
        result = use_case.execute(id=user.id, first_name='Vanished')

    # Assert
    assert result is None


def test_update_with_none_id(db_connection: sqlite3.Connection):
    """
    Testa que o caso de uso retorna None imediatamente se o id for None.
    """
    # Arrange
    user_repo = UserRepository(db_connection=db_connection)
    use_case = UpdateUserUseCase(user_repo)

    # Act
    result = use_case.execute(id=None, first_name='Test')

    # Assert
    assert result is None
