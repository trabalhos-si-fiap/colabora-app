from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Markdown

from src.use_cases import RegisterUserUseCase


class RegisterScreen(Screen):
    """Tela de registro de usuário."""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(classes='bg with-border center'):
            yield Markdown('# 📝 Tela de registro 📝')
            yield Label('Crie sua conta', id='title', classes='text')
            yield Input(
                placeholder='Seu e-mail',
                id='email-input-register',
                classes='input-margin',
            )
            yield Input(
                placeholder='Sua senha',
                password=True,
                id='password-input-register',
                classes='input-margin',
            )
            yield Input(
                placeholder='Confirme a senha',
                password=True,
                id='password-input-register-confirmation',
                classes='input-margin',
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
        confirm_password = self.query_one(
            '#password-input-register-confirmation'
        ).value

        if password != confirm_password:
            self.notify('⚠️  As senhas não coincidem.', title='Falha ao cadastrar', severity='error')
            return

        user, err = RegisterUserUseCase.factory().execute(email, password)

        if err:
            self.notify('⚠️  ' + str(err), title='Falha ao cadastrar', severity='error')
        else:
            self.notify(
                f'Você foi registrado! Agora, faça login.',
                title='🎉  Registro bem-sucedido  🥳',
                severity='information',
            )
            self.app.pop_screen()

    @on(Button.Pressed, '#back-button')
    def on_back_button_pressed(self, event: Button.Pressed):
        self.app.pop_screen()
