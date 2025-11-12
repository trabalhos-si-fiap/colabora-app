
import unittest
from unittest.mock import patch, MagicMock
from src.models import User
from src.use_cases import RegisterUseCase

class TestRegisterUseCase(unittest.TestCase):

    @patch('builtins.input', side_effect=['testuser', 'password123'])
    @patch('src.use_cases.register.PasswordManager')
    @patch('src.use_cases.register.UserRepository')
    def test_execute_registers_user(self, mock_user_repository, mock_password_manager, mock_input):
        # Arrange
        mock_repo_instance = MagicMock()
        mock_user_repository.return_value = mock_repo_instance

        mock_pm_instance = MagicMock()
        mock_pm_instance.hash_password.return_value = ('hashed_password', 'salt')
        mock_password_manager.return_value = mock_pm_instance

        use_case = RegisterUseCase(mock_repo_instance)

        # Act
        use_case.execute()

        # Assert
        mock_input.assert_any_call("Digite o seu nome de usuário: ")
        mock_input.assert_any_call("Digite a sua senha: ")

        mock_pm_instance.hash_password.assert_called_once_with('password123')

        saved_user = mock_repo_instance.save.call_args[0][0]
        self.assertEqual(saved_user.username, 'testuser')
        self.assertEqual(saved_user.password, 'hashed_password')
        self.assertEqual(saved_user.salt, 'salt')

if __name__ == '__main__':
    unittest.main()
