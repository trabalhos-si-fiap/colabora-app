from textwrap import dedent

from src.use_cases.login import LoginUseCase
from src.use_cases.register import RegisterUseCase


class View:
    def __init__(self):
        pass

    def run(self):
        while True:
            choice = input(
                dedent(
                    f"""{'='*80}
Escolha uma opção:
1. Registro
2. Login
{'='*80}\n"""
                )
            )

            match choice:
                case '1':
                    print('==============================')
                    RegisterUseCase.factory().execute()
                case '2':
                    print('==============================')
                    LoginUseCase.factory().execute()
