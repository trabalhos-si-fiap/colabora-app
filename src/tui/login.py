from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, Markdown

from src.repositories.hability import HabilityRepository
from src.repositories.users import UserRepository
from src.tui.register import RegisterScreen
from src.tui.user import UserScreen
from src.use_cases.login import LoginUseCase
from src.use_cases.replace_password import ReplacePasswordUseCase
from src.use_cases.update_user import UpdateUserUseCase

css_path = Path(__file__).parent / 'css' / 'styles.css'


class MyApp(App):
    """Um aplicativo TUI para o Colabora."""

    TITLE = 'Colabora APP'

    CSS_PATH = css_path

    BINDINGS = [
        ('t', 'change_theme()', 'Muda o tema'),
        ('q', 'quit()', 'Sair'),
    ]

    SCREENS = {
        'register': RegisterScreen,
    }

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Container(classes='bg with-border center'):
            with Container(classes='label'):
                yield Markdown('# 📒 Bem vido ao app Colabora! ✏️')
                yield Label(
                    '✨ O aplicativo que conecta talentos a projetos de impacto social. ✨',
                    classes='text',
                )
                yield Label(
                    'Entre em sua conta ou registre-se.',
                    id='output',
                    classes='text',
                )

            yield Input(
                placeholder='Digite o seu e-mail',
                value='elias@gmail.com',
                id='email-input',
                classes='input-margin',
            )
            yield Input(
                placeholder='Digite a sua senha',
                value='12345678*A',
                password=True,
                id='password-input',
                classes='input-margin',
            )

            with Container(classes='buttons'):
                yield Button('Entrar', variant='primary', id='login-button')
                yield Button('Registrar', id='register-button')

            with Container(classes='label'):
                yield Label('Ctrl + "+" aumenta o zoom da interface.')
                yield Label('Ctrl + "-" diminui o zoom da interface.')

        yield Footer()

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'login-button':
            email = self.query_one('#email-input').value
            password = self.query_one('#password-input').value

            user, err_msg = LoginUseCase.factory().execute(email, password)

            if user:
                self.push_screen(
                    UserScreen(
                        user=user,
                        user_repository=UserRepository(),
                        hability_repository=HabilityRepository(),
                        update_user_use_case=UpdateUserUseCase.factory(),
                        replace_password_use_case=ReplacePasswordUseCase.factory(),
                    )
                )
            else:
                self.query_one('#output').update('⚠️  ' + err_msg)

        elif event.button.id == 'register-button':
            self.push_screen('register')
