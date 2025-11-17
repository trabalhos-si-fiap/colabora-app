from textual.app import App, ComposeResult
from textual.widgets import Button, Label, Header, Footer, Input, Markdown
from textual.containers import Horizontal, Center, Vertical, Container
from textual import on

from pathlib import Path

from src.tui.register import RegisterScreen
from src.tui.user import UserScreen
from src.use_cases.login import LoginUseCase

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

            user = LoginUseCase.factory().execute(email, password)

            if user:
                self.push_screen(UserScreen(user))
            else:
                self.query_one('#output').update('E-mail ou senha incorretos')

        elif event.button.id == 'register-button':
            self.push_screen('register')
