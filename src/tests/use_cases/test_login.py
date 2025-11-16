import unittest
from unittest.mock import MagicMock, patch

from src.exceptions import UserNotFoundException
from src.models import User
from src.use_cases import LoginUseCase


class TestLoginUseCase(unittest.TestCase):
    @patch('builtins.input', side_effect=['testuser', 'password123'])
    @patch('src.use_cases.login.UserRepository')
    @patch('src.use_cases.login.PasswordManager')
    def test_execute_login_success(
        self, mock_password_manager, mock_user_repository, mock_input
    ):
        # Arrange
        mock_repo_instance = MagicMock()
        mock_user = User('testuser', 'hashed_password', 'salt')
        mock_repo_instance.find_user.return_value = mock_user
        mock_user_repository.return_value = mock_repo_instance

        mock_pm_instance = MagicMock()
        mock_pm_instance.check_password.return_value = True
        mock_password_manager.return_value = mock_pm_instance

        use_case = LoginUseCase(mock_repo_instance, mock_pm_instance)

        # Act
        result = use_case.execute()

        # Assert
        mock_input.assert_any_call('Digite seu nome de usuário: ')
        mock_input.assert_any_call('Digite sua senha: ')
        mock_repo_instance.find_user.assert_called_once_with('testuser')
        mock_pm_instance.check_password.assert_called_once_with(
            'password123', mock_user
        )
        self.assertEqual(result, mock_user)

    @patch('builtins.input', side_effect=['nonexistentuser', 'password123'])
    @patch('src.use_cases.login.UserRepository')
    @patch('src.use_cases.login.PasswordManager')
    def test_execute_login_user_not_found(
        self, mock_password_manager, mock_user_repository, mock_input
    ):
        # Arrange
        mock_repo_instance = MagicMock()
        mock_repo_instance.find_user.side_effect = UserNotFoundException
        mock_user_repository.return_value = mock_repo_instance

        mock_pm_instance = MagicMock()
        mock_password_manager.return_value = mock_pm_instance

        use_case = LoginUseCase(mock_repo_instance, mock_pm_instance)

        # Act
        result = use_case.execute()

        # Assert
        mock_repo_instance.find_user.assert_called_once_with('nonexistentuser')
        self.assertIsNone(result)

    @patch('builtins.input', side_effect=['testuser', 'wrongpassword'])
    @patch('src.use_cases.login.UserRepository')
    @patch('src.use_cases.login.PasswordManager')
    def test_execute_login_incorrect_password(
        self, mock_password_manager, mock_user_repository, mock_input
    ):
        # Arrange
        mock_repo_instance = MagicMock()
        mock_user = User('testuser', 'hashed_password', 'salt')
        mock_repo_instance.find_user.return_value = mock_user
        mock_user_repository.return_value = mock_repo_instance

        mock_pm_instance = MagicMock()
        mock_pm_instance.check_password.return_value = False
        mock_password_manager.return_value = mock_pm_instance

        use_case = LoginUseCase(mock_repo_instance, mock_pm_instance)

        # Act
        result = use_case.execute()

        # Assert
        mock_repo_instance.find_user.assert_called_once_with('testuser')
        mock_pm_instance.check_password.assert_called_once_with(
            'wrongpassword', mock_user
        )
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
