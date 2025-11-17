from loguru import logger
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Collapsible,
    Footer,
    Header,
    Input,
    Label,
    Static,
    Switch,
)

from src.models import User
from src.repositories.hability import HabilityRepository
from src.repositories.users import UserRepository
from src.use_cases import UpdateUserUseCase
from src.use_cases.replace_password import ReplacePasswordUseCase


class UserScreen(Screen):
    """Tela de perfil do usuário."""

    BINDINGS = [
        ('l', 'logout', 'Logout'),
    ]

    def __init__(
        self,
        user: User,
        user_repository: UserRepository,
        hability_repository: HabilityRepository,
        update_user_use_case: UpdateUserUseCase,
        replace_password_use_case: ReplacePasswordUseCase,
    ) -> None:
        self.user = user_repository.get_by_id_with_habilities(user.id)
        self.habilities_data = hability_repository.get_dict_by_domain()
        # Cria um mapa de nome da habilidade para o objeto Hability para fácil acesso
        self.hability_map = {
            hability.name: hability
            for domain_habilities in self.habilities_data.values()
            for hability in domain_habilities
        }
        self._update_user_uc = update_user_use_case
        self._replace_password_uc = replace_password_use_case
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(classes='bg with-border'):
            yield Static(
                f'Olá, {self.user.first_name or self.user.email}!',
                classes='text title',
            )
            yield Static('Edite suas informações:', classes='text')
            yield Label('#', id='output', classes='text')

            with Horizontal(classes='horizontal-inputs'):
                yield Label('Nome', classes='small-input text-center')
                yield Label('Sobrenome', classes='small-input text-center')

            with Horizontal(classes='horizontal-inputs'):
                yield Input(
                    value=self.user.first_name,
                    placeholder='Primeiro nome',
                    id='first-name',
                    classes='small-input',
                )
                yield Input(
                    value=self.user.last_name,
                    placeholder='Sobrenome',
                    id='last-name',
                    classes='small-input',
                )

            with Horizontal(classes='horizontal-inputs'):
                yield Label(
                    'Data de Nascimento', classes='small-input text-center'
                )
                yield Label('E-mail', classes='small-input text-center')

            with Horizontal(classes='horizontal-inputs'):
                yield Input(
                    value=str(self.user.birth_date)
                    if self.user.birth_date
                    else '',
                    placeholder='AAAA-MM-DD',
                    id='birth-date',
                    classes='small-input',
                )
                yield Input(
                    value=self.user.email, classes='small-input', disabled=True
                )

            with Horizontal(classes='horizontal-inputs'):
                yield Label('Projetos', classes='small-input text-center')
                yield Label('Habilidades', classes='small-input text-center')

            with Horizontal(classes='horizontal-inputs'):
                yield Label(
                    f'{len(self.user.projects)}',
                    id='projects-count',
                    classes='small-input small-input text-center',
                )
                yield Label(
                    f'{len(self.user.habilities)}',
                    id='habilities-count',
                    classes='small-input small-input text-center',
                )

            with Collapsible(title='Trocar senha', classes='input-margin'):
                yield Label('', id='output-pw', classes='text')
                yield Input(
                    placeholder='Digite a nova senha',
                    password=True,
                    id='new-password',
                    classes='input-margin-sm',
                )
                yield Input(
                    placeholder='Repita a nova senha',
                    password=True,
                    id='new-password-confirmation',
                    classes='input-margin-sm',
                )
                with Container(classes='btn-save-pw'):
                    yield Button(
                        'Salvar', variant='primary', id='save-password-button'
                    )

            yield Static('Selecione suas habilidades:', classes='text')
            with VerticalScroll(classes='center input-margin'):
                for domain in self.habilities_data.keys():
                    with Collapsible(title=domain):
                        for hability in self.habilities_data[domain]:
                            yield Horizontal(
                                Switch(
                                    value=self.user.has_hability(hability),
                                    name=hability.name,
                                ),
                                Static(hability.name, classes='label-switch'),
                                classes='container',
                            )

            with Container(classes='buttons'):
                yield Button(
                    'Salvar Alterações', variant='primary', id='save-button'
                )
                yield Button('Logout', id='logout-button')

        yield Footer()

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'save-button':

            updated_user = self._update_user_uc.execute(
                id=self.user.id,
                first_name=self.query_one('#first-name').value,
                last_name=self.query_one('#last-name').value,
                birth_date=self.query_one('#birth-date').value,
                habilities=self.user.habilities,
            )

            if updated_user:
                self.user = updated_user

            self.query_one('#projects-count').update(
                f'{len(self.user.projects)}'
            )
            self.query_one('#habilities-count').update(
                f'{len(self.user.habilities)}'
            )
            self.query_one('#output').update(
                f'✅ alterações salvas com sucesso!'
            )

        elif event.button.id == 'save-password-button':
            new_password = self.query_one('#new-password').value
            new_password_confirmation = self.query_one(
                '#new-password-confirmation'
            ).value
            if new_password != new_password_confirmation:
                self.query_one('#output-pw').update('As senhas não conferem!')
                return

            _, err = self._replace_password_uc.execute(
                id=self.user.id, new_password=new_password
            )

            if err:
                self.query_one('#output-pw').update(err)
                return

            self.query_one('#output-pw').update('Senha alterada com sucesso!')

    @on(Button.Pressed, '#logout-button')
    def action_logout(self) -> None:
        self.app.pop_screen()

    @on(Switch.Changed)
    def on_switch_changed(self, event: Switch.Changed) -> None:
        """Chamado quando o estado de um Switch de habilidade muda."""
        hability_name = event.switch.name
        hability = self.hability_map.get(hability_name)

        if hability:
            if event.value:  # Switch foi ativado
                logger.debug(f'Switch ativado para habilidade {hability.id}')
                self.user.add_hability(hability)
            else:  # Switch foi desativado
                self.user.remove_hability(hability)
