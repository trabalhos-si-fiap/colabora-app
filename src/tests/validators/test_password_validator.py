import pytest

from src.validators.password import password_validator


def test_password_validator_with_valid_password():
    """
    Testa se uma senha que atende a todos os critérios é considerada válida.
    """
    valid, message = password_validator('ValidPass123!')
    assert valid is True
    assert message is None


@pytest.mark.parametrize(
    'password, expected_message',
    [
        (None, 'Senha não informada.'),
        ('short', 'Senha deve ter no mínimo 8 caracteres.'),
        (
            'NoDigitsHere!',
            'Senha deve conter pelo menos um número.',
        ),
        (
            'nouppercase1!',
            'Senha deve conter pelo menos uma letra maiúscula.',
        ),
        (
            'NoSpecialChar1',
            'Senha deve conter pelo menos um caractere especial.',
        ),
    ],
)
def test_password_validator_with_invalid_passwords(password, expected_message):
    """Testa múltiplos cenários de senhas inválidas."""
    valid, message = password_validator(password)
    assert valid is False
    assert message == expected_message
