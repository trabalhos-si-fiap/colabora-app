from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Header, Footer, Input
from textual.containers import Container
from textual import on


from src.use_cases import RegisterUserUseCase


class RegisterScreen(Screen):
    """Tela de registro de usuário."""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(classes='bg with-border center'):
            yield Label('Crie sua conta', id='title', classes='text')
            yield Label('-', id='response', classes='text')
            yield Input(placeholder='Seu e-mail', id='email-input-register')
            yield Input(
                placeholder='Sua senha',
                password=True,
                id='password-input-register',
            )
            with Container(classes='buttons'):
                yield Button(
                    'Registrar', variant='primary', id='register-button-screen'
                )
                yield Button('Voltar', id='back-button')
        yield Footer()

    @on(Button.Pressed, '#register-button-screen')
    def on_register_button_pressed(self, event: Button.Pressed):
        email = self.query_one('#email-input-register').value
        password = self.query_one('#password-input-register').value
        user, err = RegisterUserUseCase.factory().execute(email, password)

        if err:
            self.query_one('#response').update(str(err))
        else:
            self.app.query_one('#output').update(f'Você foi registrado! Agora, faça login.')
            self.app.pop_screen()

    @on(Button.Pressed, '#back-button')
    def on_back_button_pressed(self, event: Button.Pressed):
        self.app.pop_screen()