import pytest

from src.validators.email import email_validator


def test_email_validator_with_valid_email():
    """
    Testa se um e-mail que atende aos critérios básicos é considerado válido.
    """
    valid, message = email_validator('test.user@example.com')
    assert valid is True
    assert message is None


@pytest.mark.parametrize(
    'email, expected_message',
    [
        (None, 'E-mail não informado.'),
        ('plainaddress', 'E-mail deve conter "@".'),
        ('test.example.com', 'E-mail deve conter "@".'),
        ('test@examplecom', 'E-mail deve conter ".".'),
    ],
)
def test_email_validator_with_invalid_emails(email, expected_message):
    """
    Testa múltiplos cenários de e-mails inválidos, cobrindo todas as
    regras de falha da função.
    """
    valid, message = email_validator(email)
    assert valid is False
    assert message == expected_message
