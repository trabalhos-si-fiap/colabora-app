def email_validator(email: str) -> tuple[bool, str]:
    if email is None:
        return False, 'E-mail não informado.'

    if '@' not in email:
        return False, 'E-mail deve conter "@".'

    if '.' not in email:
        return False, 'E-mail deve conter ".".'

    return True, 'E-mail válido.'
