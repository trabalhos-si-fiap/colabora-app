import string


def password_validator(password: str) -> tuple[bool, str]:
    if password is None:
        return False, 'Senha não informada.'
    if len(password) < 8:
        return False, 'Senha deve ter no mínimo 8 caracteres.'
    if not any(char.isdigit() for char in password):
        return False, 'Senha deve conter pelo menos um número.'
    if not any(char.isupper() for char in password):
        return False, 'Senha deve conter pelo menos uma letra maiúscula.'
    if not any(char in string.punctuation for char in password):
        return False, 'Senha deve conter pelo menos um caractere especial.'
    return True, 'Senha válida'
