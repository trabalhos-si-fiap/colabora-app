from unittest.mock import MagicMock, patch

import pytest

from src.exceptions import UserNotFoundException
from src.models import User
from src.use_cases.login import LoginUseCase


@pytest.fixture
def mock_user_repository():
    """Um fixture do pytest para criar um mock do UserRepository."""
    return MagicMock()


@pytest.fixture
def mock_password_manager():
    """Um fixture do pytest para criar um mock do PasswordManager."""
    return MagicMock()


@pytest.fixture
def login_use_case(mock_user_repository, mock_password_manager):
    """Um fixture que cria uma instância de LoginUseCase com mocks."""
    return LoginUseCase(mock_user_repository, mock_password_manager)


def test_execute_success(
    login_use_case, mock_user_repository, mock_password_manager
):
    """
    Testa o fluxo de login bem-sucedido.
    """
    # Arrange
    sample_user = User('testuser', b'hashed_password', b'salt')
    mock_user_repository.find_user.return_value = sample_user
    mock_password_manager.check_password.return_value = True

    # Act
    result = login_use_case.execute('testuser', 'password123')

    # Assert
    mock_user_repository.find_user.assert_called_once_with('testuser')
    mock_password_manager.check_password.assert_called_once_with(
        'password123', sample_user
    )
    assert result == sample_user


def test_execute_user_not_found(
    login_use_case, mock_user_repository, mock_password_manager
):
    """
    Testa o fluxo de falha quando o usuário não é encontrado.
    """
    # Arrange
    mock_user_repository.find_user.side_effect = UserNotFoundException(
        'Usuário não encontrado'
    )

    # Act
    result = login_use_case.execute()

    # Assert
    mock_user_repository.find_user.assert_called_once_with('nonexistentuser')
    mock_password_manager.check_password.assert_not_called()
    assert result is None


def test_execute_incorrect_password(
    login_use_case, mock_user_repository, mock_password_manager
):
    """
    Testa o fluxo de falha quando a senha está incorreta.
    """
    # Arrange
    sample_user = User('testuser', b'hashed_password', b'salt')
    mock_user_repository.find_user.return_value = sample_user
    mock_password_manager.check_password.return_value = False

    # Act
    result = login_use_case.execute('testuser', 'wrongpassword')

    # Assert
    mock_user_repository.find_user.assert_called_once_with('testuser')
    mock_password_manager.check_password.assert_called_once_with(
        'wrongpassword', sample_user
    )
    assert result is None
