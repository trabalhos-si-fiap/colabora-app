from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    RadioButton,
    RadioSet,
    Select,
    SelectionList,
    Static,
    TabbedContent,
    TabPane,
)

from src.models import Hability, Organization, Project, Role, User
from src.repositories import (
    HabilityRepository,
    OrganizationRepository,
    ProjectRepository,
    UserRepository,
)
from src.use_cases import (
    UpdateProjectUseCase,
)
from src.use_cases.register import RegisterUserUseCase
from src.use_cases.update_user import UpdateUserUseCase


class AdminScreen(Screen):
    """Tela administrativa para criação de entidades."""

    BINDINGS = [('escape', 'app.pop_screen', 'Voltar')]

    def __init__(
        self,
        user_logged: User,
        organization_repo: OrganizationRepository = None,
        project_repo: ProjectRepository = None,
        hability_repo: HabilityRepository = None,
        user_repo: UserRepository = None,
        update_project_use_case: UpdateProjectUseCase = None,
        register_user_use_case: RegisterUserUseCase = None,
        update_user_uc: UpdateUserUseCase = None,
    ):
        self._user_logged = user_logged
        self._org_repo = (
            organization_repo
            if organization_repo
            else OrganizationRepository()
        )
        self._proj_repo = project_repo if project_repo else ProjectRepository()
        self._hab_repo = (
            hability_repo if hability_repo else HabilityRepository()
        )
        self._user_repo = user_repo if user_repo else UserRepository()
        self._update_proj_uc = (
            update_project_use_case
            if update_project_use_case
            else UpdateProjectUseCase.factory()
        )
        self._register_user_uc = (
            register_user_use_case
            if register_user_use_case
            else RegisterUserUseCase.factory()
        )
        self._update_user_uc = (
            update_user_uc if update_user_uc else UpdateUserUseCase.factory()
        )
        super().__init__()

    def _get_org_options(self) -> list[tuple[str, int]]:
        """Busca organizações e as formata para widgets de seleção."""
        return [(org.name, org.id) for org in self._org_repo.find_all()]

    def _get_hab_options(self) -> list[tuple[str, int]]:
        """Busca habilidades e as formata para widgets de seleção."""
        return [(hab.name, hab.id) for hab in self._hab_repo.find_all()]

    def _get_proj_options(self) -> list[tuple[str, int]]:
        """Busca projetos e os formata para widgets de seleção."""
        return [(proj.name, proj.id) for proj in self._proj_repo.find_all()]

    def _get_user_options(self) -> list[tuple[str, int]]:
        """Busca usuários e os formata para widgets de seleção."""
        users = self._user_repo.find_all()
        return [
            (
                f'{user.first_name or ""} {user.last_name or ""} ({user.email})',
                user.id,
            )
            for user in users
        ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(classes='bg with-border'):
            yield Static('Painel Administrativo', classes='text title')
            yield Label('', id='admin-output', classes='text')

            with TabbedContent(id='main-tabs', classes='input-margin'):
                # --- Aba de Organizações ---
                with TabPane('Organizações', id='org-tab'):
                    with TabbedContent(id='org-crud-tabs'):
                        # --- Criar Organização ---
                        with TabPane('Criar', id='org-create-tab'):
                            yield Input(
                                placeholder='Nome da Organização',
                                id='org-name',
                                classes='input-margin-sm',
                            )
                            yield Input(
                                placeholder='Descrição',
                                id='org-description',
                                classes='input-margin-sm',
                            )
                            yield Input(
                                placeholder='E-mail de Contato',
                                id='org-email',
                                classes='input-margin-sm',
                            )
                            yield Input(
                                placeholder='Telefone de Contato',
                                id='org-phone',
                                classes='input-margin-sm',
                            )
                            yield Input(
                                placeholder='Website',
                                id='org-website',
                                classes='input-margin-sm',
                            )
                            with Container(classes='full-width h3 center'):
                                yield Button(
                                    'Salvar Nova Organização',
                                    variant='primary',
                                    id='save-org-button',
                                    classes='',
                                )
                        # --- Listar/Editar Organização ---
                        with TabPane(
                            'Listar/Editar', id='org-edit-tab', classes='mt1'
                        ):
                            with RadioSet(id='org-edit-list', classes='mx4'):
                                for name, org_id in self._get_org_options():
                                    rb = RadioButton(name)
                                    rb.db_id = org_id
                                    yield rb

                            with Container(
                                id='org-edit-form',
                                classes='hidden full-width h-auto',
                            ):
                                yield Static(
                                    'Editando Organização:', classes='text mb1'
                                )
                                yield Label(
                                    '[b]Selecione uma Organização para editar.[/]',
                                    id='org-edit-id-label',
                                    classes='text',
                                )

                                yield Input(
                                    id='org-edit-name',
                                    classes='input-margin-sm',
                                    disabled=True,
                                )
                                yield Input(
                                    id='org-edit-description',
                                    classes='input-margin-sm',
                                    disabled=True,
                                )
                                yield Input(
                                    id='org-edit-email',
                                    classes='input-margin-sm',
                                    disabled=True,
                                )
                                yield Input(
                                    id='org-edit-phone',
                                    classes='input-margin-sm',
                                    disabled=True,
                                )
                                yield Input(
                                    id='org-edit-website',
                                    classes='input-margin-sm',
                                    disabled=True,
                                )
                                with Container(classes='full-width h3 center'):
                                    yield Button(
                                        'Salvar Alterações',
                                        id='update-org-button',
                                        variant='success',
                                        disabled=True,
                                    )

                        # --- Deletar Organização ---
                        with TabPane(
                            'Deletar', id='org-delete-tab', classes='mt1'
                        ):
                            with RadioSet(id='org-delete-list', classes='mx4'):
                                for name, org_id in self._get_org_options():
                                    rb = RadioButton(name)
                                    rb.db_id = org_id
                                    yield rb
                            with Container(classes='full-width h3 center mt1'):
                                yield Button(
                                    'Deletar Selecionada',
                                    variant='error',
                                    id='delete-org-button',
                                )

                # --- Aba de Projetos ---
                with TabPane('Projetos', id='proj-tab'):
                    with TabbedContent(id='proj-crud-tabs'):
                        # --- Criar Projeto ---
                        with TabPane('Criar', id='proj-create-tab'):
                            yield Input(
                                classes='input-margin-sm',
                                placeholder='Nome do Projeto',
                                id='proj-name',
                            )
                            yield Input(
                                classes='input-margin-sm',
                                placeholder='Descrição do Projeto',
                                id='proj-description',
                            )
                            yield Select(
                                self._get_org_options(),
                                classes='input-margin-sm',
                                prompt='Selecione a Organização',
                                id='proj-org-select',
                            )
                            yield Label(
                                '[b]Habilidades Necessárias:[/]',
                                classes='text mt1',
                            )
                            yield SelectionList[int](
                                *self._get_hab_options(),
                                id='proj-hab-list',
                                classes='input-margin-sm',
                            )
                            with Container(classes='full-width h3 center mt1'):
                                yield Button(
                                    'Salvar Novo Projeto',
                                    variant='primary',
                                    id='save-proj-button',
                                )

                        # --- Listar/Editar Projeto ---
                        with TabPane(
                            'Listar/Editar', id='proj-edit-tab', classes='mt1'
                        ):
                            with RadioSet(id='proj-edit-list', classes='mx4'):
                                for name, proj_id in self._get_proj_options():
                                    rb = RadioButton(name)
                                    rb.db_id = proj_id
                                    yield rb

                            with Container(
                                id='proj-edit-form',
                                classes='hidden full-width h-auto',
                            ):
                                yield Static(
                                    'Editando Projeto:', classes='text mb1'
                                )
                                yield Label(
                                    '[b]Selecione um projeto para editar[/]',
                                    id='proj-edit-id-label',
                                    classes='text',
                                )
                                yield Input(
                                    id='proj-edit-name',
                                    classes='input-margin-sm',
                                )

                                yield Input(
                                    id='proj-edit-description',
                                    classes='input-margin-sm',
                                )
                                yield Select(
                                    self._get_org_options(),
                                    prompt='Selecione a Organização',
                                    id='proj-edit-org-select',
                                    classes='input-margin-sm',
                                )
                                yield Label(
                                    '[b]Habilidades Necessárias:[/]',
                                    classes='text mt1',
                                )
                                yield SelectionList[int](
                                    *self._get_hab_options(),
                                    id='proj-edit-hab-list',
                                    classes='input-margin-sm',
                                )
                                with Container(
                                    classes='full-width h3 center mt1'
                                ):
                                    yield Button(
                                        'Salvar Alterações',
                                        id='update-proj-button',
                                        variant='success',
                                    )

                        # --- Deletar Projeto ---
                        with TabPane(
                            'Deletar', id='proj-delete-tab', classes='mt1'
                        ):
                            with RadioSet(
                                id='proj-delete-list', classes='mx4'
                            ):
                                for name, proj_id in self._get_proj_options():
                                    rb = RadioButton(name)
                                    rb.db_id = proj_id
                                    yield rb

                            with Container(classes='full-width h3 center mt1'):
                                yield Button(
                                    'Deletar Selecionado',
                                    variant='error',
                                    id='delete-proj-button',
                                )

                # --- Aba de Usuários ---
                with TabPane('Usuários', id='user-tab'):
                    with TabbedContent(id='user-crud-tabs'):
                        # --- Criar Usuário ---
                        with TabPane('Criar', id='user-create-tab'):
                            yield Input(
                                classes='input-margin-sm',
                                placeholder='E-mail do Usuário',
                                id='user-email',
                            )
                            yield Input(
                                classes='input-margin-sm',
                                placeholder='Senha',
                                id='user-password',
                                password=True,
                            )
                            yield Select(
                                [('Admin', Role.ADMIN), ('User', Role.USER)],
                                prompt='Selecione a Role',
                                id='user-role-select',
                                classes='input-margin-sm',
                            )
                            with Container(classes='full-width h3 center mt1'):
                                yield Button(
                                    'Salvar Novo Usuário',
                                    variant='primary',
                                    id='save-user-button',
                                )

                        # --- Listar/Editar Usuário ---
                        with TabPane(
                            'Listar/Editar', id='user-edit-tab', classes='mt1'
                        ):
                            with RadioSet(id='user-edit-list', classes='mx4'):
                                for name, user_id in self._get_user_options():
                                    rb = RadioButton(name)
                                    rb.db_id = user_id
                                    yield rb

                            with Container(
                                id='user-edit-form',
                                classes='hidden full-width h-auto',
                            ):
                                yield Static(
                                    'Editando Usuário:', classes='text mb1'
                                )
                                yield Label(
                                    '', id='user-edit-id-label', classes='text'
                                )
                                yield Input(
                                    classes='input-margin-sm',
                                    id='user-edit-firstname',
                                    placeholder='Primeiro Nome',
                                )
                                yield Input(
                                    classes='input-margin-sm',
                                    id='user-edit-lastname',
                                    placeholder='Sobrenome',
                                )
                                yield Input(
                                    classes='input-margin-sm',
                                    id='user-edit-email',
                                    disabled=True,
                                )
                                yield Select(
                                    [
                                        ('Admin', Role.ADMIN),
                                        ('User', Role.USER),
                                    ],
                                    prompt='Selecione a Role',
                                    id='user-edit-role-select',
                                    classes='input-margin-sm',
                                )
                                with Container(
                                    classes='full-width h3 center mt1'
                                ):
                                    yield Button(
                                        'Salvar Alterações',
                                        id='update-user-button',
                                        variant='success',
                                    )

                        # --- Deletar Usuário ---
                        with TabPane(
                            'Deletar', id='user-delete-tab', classes='mt1'
                        ):
                            with RadioSet(
                                id='user-delete-list', classes='mx4'
                            ):
                                for name, user_id in self._get_user_options():
                                    rb = RadioButton(name)
                                    rb.db_id = user_id
                                    yield rb
                            with Container(classes='full-width h3 center mt1'):
                                yield Button(
                                    'Deletar Selecionado',
                                    variant='error',
                                    id='delete-user-button',
                                )

        yield Footer()

    def _repopulate_org_radio_sets(self, clear_selection: bool = True):
        """Atualiza os RadioSets de organização."""
        new_options = self._get_org_options()
        for list_id in ['#org-edit-list', '#org-delete-list']:
            radio_set = self.query_one(list_id, RadioSet)
            radio_set.blur()  # Remove o foco para evitar problemas de estado
            if clear_selection:
                ...
                # radio_set.pressed_button = None
            radio_set.remove_children()
            for name, org_id in new_options:
                rb = RadioButton(name)
                rb.db_id = org_id
                radio_set.mount(rb)

    def _repopulate_org_selects(self):
        """Atualiza os Selects de organização nos formulários de projeto."""
        new_options = self._get_org_options()
        proj_org_select = self.query_one('#proj-org-select', Select)
        proj_org_select.set_options(new_options)
        proj_edit_org_select = self.query_one('#proj-edit-org-select', Select)
        proj_edit_org_select.set_options(new_options)

    def _clear_and_repopulate_org_lists(self, clear_selection: bool = True):
        """Atualiza todas as listas de organizações na tela."""
        self._repopulate_org_radio_sets(clear_selection)
        self._repopulate_org_selects()

    def _clear_and_repopulate_proj_lists(self):
        """Atualiza todas as listas de projetos na tela."""
        new_options = self._get_proj_options()

        # Atualiza lista de edição
        edit_list = self.query_one('#proj-edit-list', RadioSet)
        edit_list.remove_children()
        for name, proj_id in new_options:
            rb = RadioButton(name)
            rb.db_id = proj_id
            edit_list.mount(rb)

        # Atualiza lista de deleção
        delete_list = self.query_one('#proj-delete-list', RadioSet)
        delete_list.remove_children()
        for name, proj_id in new_options:
            rb = RadioButton(name)
            rb.db_id = proj_id
            delete_list.mount(rb)

    def _clear_and_repopulate_user_lists(self):
        """Atualiza todas as listas de usuários na tela."""
        new_options = self._get_user_options()

        # Atualiza lista de edição
        edit_list = self.query_one('#user-edit-list', RadioSet)
        edit_list.remove_children()
        for name, user_id in new_options:
            rb = RadioButton(name)
            rb.db_id = user_id
            edit_list.mount(rb)

        # Atualiza lista de deleção
        delete_list = self.query_one('#user-delete-list', RadioSet)
        delete_list.remove_children()
        for name, user_id in new_options:
            rb = RadioButton(name)
            rb.db_id = user_id
            delete_list.mount(rb)

    @on(RadioSet.Changed, '#org-edit-list')
    def on_org_selection_changed(self, event: RadioSet.Changed):
        """Preenche o formulário de edição quando uma organização é selecionada."""
        edit_form = self.query_one('#org-edit-form')
        # O evento Changed é emitido duas vezes: ao desmarcar o antigo e marcar o novo.
        # Ignoramos o evento de "desmarcar" onde `event.pressed` é None.
        if event.pressed:
            org_id = getattr(event.pressed, 'db_id', None)
            if org_id is not None:
                org = self._org_repo.get_by_id(org_id)

                if org:
                    self.query_one('#org-edit-id-label', Label).update(
                        f'[b]ID:[/b] {org.id}'
                    )
                    self.query_one('#org-edit-name', Input).value = org.name
                    self.query_one(
                        '#org-edit-description', Input
                    ).value = org.description
                    self.query_one(
                        '#org-edit-email', Input
                    ).value = org.contact_email
                    self.query_one(
                        '#org-edit-phone', Input
                    ).value = org.contact_phone
                    self.query_one(
                        '#org-edit-website', Input
                    ).value = org.website
                    # Habilita todos os inputs no formulário de edição
                    for input_widget in edit_form.query(Input):
                        input_widget.disabled = False

                    edit_form.query_one(Button).disabled = False
                    edit_form.remove_class('hidden')
        else:
            # Esconde o formulário e desabilita os inputs se nada for selecionado
            for input_widget in edit_form.query(Input):
                input_widget.disabled = True
            edit_form.add_class('hidden')

    @on(RadioSet.Changed, '#proj-edit-list')
    def on_proj_selection_changed(self, event: RadioSet.Changed):
        """Preenche o formulário de edição quando um projeto é selecionado."""
        edit_form = self.query_one('#proj-edit-form')

        # Ignoramos o evento de "desmarcar" onde `event.pressed` é None.
        if event.pressed:
            # Limpa a seleção de habilidades anterior antes de preencher
            self.query_one('#proj-edit-hab-list', SelectionList).deselect_all()
            proj_id = getattr(event.pressed, 'db_id', None)
            if proj_id is not None:
                # Usamos find_all_with_habilities para garantir que as habilidades venham juntas
                all_projects = self._proj_repo.find_all_with_habilities()
                proj = next((p for p in all_projects if p.id == proj_id), None)
            if proj_id is not None:
                # Busca o projeto com suas habilidades associadas
                proj = self._proj_repo.get_by_id_with_habilities(proj_id)

                if proj:
                    self.query_one('#proj-edit-id-label', Label).update(
                        f'[b]ID:[/b] {proj.id}'
                    )
                    self.query_one('#proj-edit-name', Input).value = proj.name
                    self.query_one(
                        '#proj-edit-description', Input
                    ).value = proj.description
                    self.query_one(
                        '#proj-edit-org-select', Select
                    ).value = proj.organization_id

                    hab_list = self.query_one(
                        '#proj-edit-hab-list', SelectionList
                    )
                    hab_list.deselect_all()
                    for hability in proj.habilities:
                        hab_list.select(hability.id)
                    edit_form.remove_class('hidden')

    @on(RadioSet.Changed, '#user-edit-list')
    def on_user_selection_changed(self, event: RadioSet.Changed):
        """Preenche o formulário de edição quando um usuário é selecionado."""
        edit_form = self.query_one('#user-edit-form')

        # Ignoramos o evento de "desmarcar" onde `event.pressed` é None.
        if event.pressed:
            user_id = getattr(event.pressed, 'db_id', None)
            if user_id is not None:
                user = self._user_repo.get_by_id(user_id)

                if user:
                    self.query_one('#user-edit-id-label', Label).update(
                        f'[b]ID:[/b] {user.id}'
                    )
                    self.query_one('#user-edit-firstname', Input).value = (
                        user.first_name or ''
                    )
                    self.query_one('#user-edit-lastname', Input).value = (
                        user.last_name or ''
                    )
                    self.query_one(
                        '#user-edit-email', Input
                    ).value = user.email
                    self.query_one(
                        '#user-edit-role-select', Select
                    ).value = user.role
                    edit_form.remove_class('hidden')

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed):
        output_label = self.query_one('#admin-output')

        # --- Lógica de Organizações ---
        if event.button.id == 'save-org-button':
            try:
                org = Organization(
                    name=self.query_one('#org-name').value,
                    description=self.query_one('#org-description').value,
                    contact_email=self.query_one('#org-email').value,
                    contact_phone=self.query_one('#org-phone').value,
                    website=self.query_one('#org-website').value,
                )
                self._org_repo.save(org)
                self.notify('✅ Organização salva com sucesso!')
                self._repopulate_org_radio_sets(clear_selection=True)
                self._repopulate_org_selects()
                for input_widget in self.query('Input'):
                    if input_widget.id.startswith('org-'):
                        input_widget.value = ''
            except Exception as e:
                self.notify(
                    f'❌ Erro ao salvar organização: {e}', severity='error'
                )

        elif event.button.id == 'update-org-button':
            try:
                radio_set = self.query_one('#org-edit-list', RadioSet)
                if radio_set.pressed_button is None:
                    raise ValueError('Nenhuma organização selecionada.')

                org_id = getattr(radio_set.pressed_button, 'db_id', None)
                updated_org = Organization(
                    id=org_id,
                    name=self.query_one('#org-edit-name').value,
                    description=self.query_one('#org-edit-description').value,
                    contact_email=self.query_one('#org-edit-email').value,
                    contact_phone=self.query_one('#org-edit-phone').value,
                    website=self.query_one('#org-edit-website').value,
                )
                self._org_repo.save(updated_org)
                self.notify('✅ Organização atualizada com sucesso!')
                self._repopulate_org_radio_sets(clear_selection=False)
                self._repopulate_org_selects()
                self.query_one('#org-edit-form').add_class('hidden')
            except Exception as e:
                self.notify(
                    f'❌ Erro ao atualizar organização: {e}', severity='error'
                )

        elif event.button.id == 'delete-org-button':
            try:
                radio_set = self.query_one('#org-delete-list', RadioSet)
                if radio_set.pressed_button is None:
                    raise ValueError('Nenhuma organização selecionada.')
                org_id = getattr(radio_set.pressed_button, 'db_id', None)

                deleted = self._org_repo.delete(org_id)
                if deleted:
                    self.notify('✅ Organização deletada com sucesso!')
                    self._repopulate_org_radio_sets(clear_selection=True)
                    self._repopulate_org_selects()
                else:
                    self.notify('⚠️ Organização não encontrada.')
            except Exception as e:
                self.notify(
                    f'❌ Erro ao deletar organização: {e}', severity='error'
                )

        # --- Lógica de Projetos ---
        elif event.button.id == 'save-proj-button':
            try:
                hab_list = self.query_one('#proj-hab-list', SelectionList)
                selected_hability_ids = hab_list.selected

                proj = Project(
                    name=self.query_one('#proj-name').value,
                    description=self.query_one('#proj-description').value,
                    organization_id=self.query_one('#proj-org-select').value,
                )
                # Busca os objetos Hability e os atribui ao projeto
                proj.habilities = self._hab_repo.find_by_ids(
                    selected_hability_ids
                )

                self._proj_repo.save(proj)
                self.notify('✅ Projeto salvo com sucesso!')
                self._clear_and_repopulate_proj_lists()
                for widget in self.query():
                    if isinstance(widget, Input) and widget.id.startswith(
                        'proj-'
                    ):
                        widget.value = ''
                hab_list.deselect_all()
            except Exception as e:
                self.notify(f'❌ Erro ao salvar projeto: {e}', severity='error')

        elif event.button.id == 'update-proj-button':
            try:
                radio_set = self.query_one('#proj-edit-list', RadioSet)
                if radio_set.pressed_button is None:
                    raise ValueError('Nenhum projeto selecionado.')
                proj_id = getattr(radio_set.pressed_button, 'db_id', None)

                hab_list = self.query_one('#proj-edit-hab-list', SelectionList)

                # Busca os objetos Hability a partir dos IDs selecionados
                selected_habilities = self._hab_repo.find_by_ids(
                    hab_list.selected
                )

                updated_proj = self._update_proj_uc.execute(
                    id=proj_id,
                    name=self.query_one('#proj-edit-name').value,
                    description=self.query_one('#proj-edit-description').value,
                    organization_id=self.query_one(
                        '#proj-edit-org-select'
                    ).value,
                    habilities=selected_habilities,
                )

                if updated_proj:
                    self.notify('✅ Projeto atualizado com sucesso!')
                    self._clear_and_repopulate_proj_lists()
                    self.query_one('#proj-edit-form').add_class('hidden')
                else:
                    self.notify(
                        '❌ Erro ao atualizar projeto.', severity='error'
                    )
            except Exception as e:
                self.notify(
                    f'❌ Erro ao atualizar projeto: {e}', severity='error'
                )

        elif event.button.id == 'delete-proj-button':
            try:
                radio_set = self.query_one('#proj-delete-list', RadioSet)
                if radio_set.pressed_button is None:
                    raise ValueError('Nenhum projeto selecionado.')
                proj_id = getattr(radio_set.pressed_button, 'db_id', None)

                deleted = self._proj_repo.delete(proj_id)
                if deleted:
                    self.notify('✅ Projeto deletado com sucesso!')
                    self._clear_and_repopulate_proj_lists()
                else:
                    self.notify('⚠️ Projeto não encontrado.')
            except Exception as e:
                self.notify(
                    f'❌ Erro ao deletar projeto: {e}', severity='error'
                )

        # --- Lógica de Usuários ---
        elif event.button.id == 'save-user-button':
            try:
                user, error = self._register_user_uc.execute(
                    email=self.query_one('#user-email').value,
                    password=self.query_one('#user-password').value,
                )

                if error is not None:
                    raise Exception(str(error))

                self.notify('✅ Usuário salvo com sucesso!')
                self._clear_and_repopulate_user_lists()
                self.query_one('#user-email', Input).value = ''
                self.query_one('#user-password', Input).value = ''
            except Exception as e:
                self.notify(f'❌ Erro ao salvar usuário: {e}', severity='error')

        elif event.button.id == 'update-user-button':
            try:
                radio_set = self.query_one('#user-edit-list', RadioSet)
                if radio_set.pressed_button is None:
                    raise ValueError('Nenhum usuário selecionado.')
                user_id = getattr(radio_set.pressed_button, 'db_id', None)

                # A senha não é atualizada aqui, apenas outros dados

                user = self._update_user_uc.execute(
                    id=user_id,
                    first_name=self.query_one('#user-edit-firstname').value,
                    last_name=self.query_one('#user-edit-lastname').value,
                    role=self.query_one('#user-edit-role-select').value,
                )
                if user is None:
                    raise ValueError('Usuário não encontrado.')

                self.notify('✅ Usuário atualizado com sucesso!')
                self._clear_and_repopulate_user_lists()
                self.query_one('#user-edit-form').add_class('hidden')

            except Exception as e:
                self.notify(
                    f'❌ Erro ao atualizar usuário: {e}', severity='error'
                )

        elif event.button.id == 'delete-user-button':
            try:
                radio_set = self.query_one('#user-delete-list', RadioSet)
                if radio_set.pressed_button is None:
                    raise ValueError('Nenhum usuário selecionado.')
                user_id = getattr(radio_set.pressed_button, 'db_id', None)

                # Adicionar verificação para não se auto-deletar
                if self._user_logged and self._user_logged.id == user_id:
                    self.notify(
                        '❌ Você não pode deletar a si mesmo.', severity='error'
                    )
                    return

                deleted = self._user_repo.delete(user_id)
                if deleted:
                    self.notify('✅ Usuário deletado com sucesso!')
                    self._clear_and_repopulate_user_lists()
                else:
                    self.notify('⚠️ Usuário não encontrado.')
            except Exception as e:
                self.notify(
                    f'❌ Erro ao deletar usuário: {e}', severity='error'
                )
