from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    Markdown,
    Static,
)

from src.populate_db.users import PopulateRawDB
from src.repositories import (
    HabilityRepository,
    ProjectRepository,
    UserRepository,
)
from src.tui.project import ProjectScreen
from src.tui.register import RegisterScreen
from src.tui.user import UserScreen
from src.use_cases import (
    LoginUseCase,
    ReplacePasswordUseCase,
    UpdateUserUseCase,
)

css_path = Path(__file__).parent / 'css' / 'styles.css'


class ColaboraApp(App):
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

    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()
        self.project_repository = ProjectRepository()
        self.hability_repository = HabilityRepository()
        self.login_use_case = LoginUseCase.factory()
        self.update_user_use_case = UpdateUserUseCase.factory()
        self.replace_password_use_case = ReplacePasswordUseCase.factory()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Container(classes='bg with-border center'):
            with Container(classes='label'):
                yield Markdown('# 📒 Bem vido ao app Colabora! ✏️')
                yield Label(
                    '✨ Conectando talentos a projetos de impacto social. ✨',
                    classes='text',
                )
                yield Static(
                    'Entre em sua conta ou registre-se.',
                    id='login-output',
                    classes='text',
                )

            yield Input(
                placeholder='Digite o seu e-mail',
                value='admin@admin.com',
                id='email-input',
                classes='input-margin',
            )
            yield Input(
                placeholder='Digite a sua senha',
                value='SenhaForte123*',
                password=True,
                id='password-input',
                classes='input-margin',
            )

            with Container(classes='buttons'):
                yield Button('Entrar', variant='primary', id='login-button')
                yield Button('Registrar', id='register-button')
                yield Button('Ver Projetos', id='view-projects-button')

            with Container(classes='label'):
                yield Label('Ctrl + "+" aumenta o zoom da interface.')
                yield Label('Ctrl + "-" diminui o zoom da interface.')

        yield Footer()

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'login-button':
            email = self.query_one('#email-input').value
            password = self.query_one('#password-input').value

            user, err_msg = self.login_use_case.execute(email, password)

            if user:
                self.push_screen(
                    UserScreen(
                        user=user,
                        user_repository=self.user_repository,
                        hability_repository=self.hability_repository,
                        update_user_use_case=self.update_user_use_case,
                        replace_password_use_case=self.replace_password_use_case,
                    )
                )
            else:
                self.notify(
                    '⚠️  ' + err_msg,
                    title='Erro ao fazer login',
                    severity='error',
                )

        elif event.button.id == 'register-button':
            self.push_screen('register')

        elif event.button.id == 'view-projects-button':
            self.push_screen(
                ProjectScreen(
                    user=None,  # Usuário não logado
                    user_repository=self.user_repository,
                    project_repository=self.project_repository,
                )
            )
