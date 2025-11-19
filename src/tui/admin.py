from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Collapsible,
    Footer,
    Header,
    Input,
    Label,
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


class AdminScreen(Screen):
    """Tela administrativa para criação de entidades."""

    BINDINGS = [('escape', 'app.pop_screen', 'Voltar')]

    def __init__(self):
        self._org_repo = OrganizationRepository()
        self._proj_repo = ProjectRepository()
        self._hab_repo = HabilityRepository()
        self._user_repo = UserRepository()
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

            with TabbedContent(id='main-tabs'):
                # --- Aba de Organizações ---
                with TabPane('Organizações', id='org-tab'):
                    with TabbedContent(id='org-crud-tabs'):
                        # --- Criar Organização ---
                        with TabPane('Criar', id='org-create-tab'):
                            yield Input(
                                placeholder='Nome da Organização',
                                id='org-name',
                            )
                            yield Input(
                                placeholder='Descrição',
                                id='org-description',
                                classes='mt1',
                            )
                            yield Input(
                                placeholder='E-mail de Contato',
                                id='org-email',
                                classes='mt1',
                            )
                            yield Input(
                                placeholder='Telefone de Contato',
                                id='org-phone',
                                classes='mt1',
                            )
                            yield Input(
                                placeholder='Website',
                                id='org-website',
                                classes='mt1',
                            )
                            yield Button(
                                'Salvar Nova Organização',
                                variant='primary',
                                id='save-org-button',
                                classes='mt1',
                            )
                        # --- Listar/Editar Organização ---
                        with TabPane('Listar/Editar', id='org-edit-tab'):
                            yield SelectionList[int](
                                *self._get_org_options(),
                                id='org-edit-list',
                            )
                            with Container(
                                id='org-edit-form', classes='hidden'
                            ):
                                yield Static(
                                    'Editando Organização:', classes='text'
                                )
                                yield Input(id='org-edit-name')
                                yield Input(id='org-edit-description')
                                yield Input(id='org-edit-email')
                                yield Input(id='org-edit-phone')
                                yield Input(id='org-edit-website')
                                yield Button(
                                    'Salvar Alterações',
                                    id='update-org-button',
                                    variant='success',
                                )

                        # --- Deletar Organização ---
                        with TabPane('Deletar', id='org-delete-tab'):
                            yield SelectionList[int](
                                *self._get_org_options(),
                                id='org-delete-list',
                            )
                            yield Button(
                                'Deletar Selecionada',
                                variant='error',
                                id='delete-org-button',
                                classes='mt1',
                            )

                # --- Aba de Projetos ---
                with TabPane('Projetos', id='proj-tab'):
                    with TabbedContent(id='proj-crud-tabs'):
                        # --- Criar Projeto ---
                        with TabPane('Criar', id='proj-create-tab'):
                            yield Input(
                                placeholder='Nome do Projeto', id='proj-name'
                            )
                            yield Input(
                                placeholder='Descrição do Projeto',
                                id='proj-description',
                                classes='mt1',
                            )
                            yield Select(
                                self._get_org_options(),
                                prompt='Selecione a Organização',
                                id='proj-org-select',
                            )
                            yield Label(
                                'Habilidades Necessárias:',
                                classes='text mt1',
                            )
                            yield SelectionList[int](
                                *self._get_hab_options(), id='proj-hab-list'
                            )
                            yield Button(
                                'Salvar Novo Projeto',
                                variant='primary',
                                id='save-proj-button',
                                classes='mt1',
                            )

                        # --- Listar/Editar Projeto ---
                        with TabPane('Listar/Editar', id='proj-edit-tab'):
                            yield SelectionList[int](
                                *self._get_proj_options(),
                                id='proj-edit-list',
                            )
                            with Container(
                                id='proj-edit-form', classes='hidden'
                            ):
                                yield Static(
                                    'Editando Projeto:', classes='text'
                                )
                                yield Input(id='proj-edit-name')
                                yield Input(
                                    id='proj-edit-description', classes='mt1'
                                )
                                yield Select(
                                    self._get_org_options(),
                                    prompt='Selecione a Organização',
                                    id='proj-edit-org-select',
                                )
                                yield Label(
                                    'Habilidades Necessárias:',
                                    classes='text mt1',
                                )
                                yield SelectionList[int](
                                    *self._get_hab_options(),
                                    id='proj-edit-hab-list',
                                )
                                yield Button(
                                    'Salvar Alterações',
                                    id='update-proj-button',
                                    variant='success',
                                    classes='mt1',
                                )

                        # --- Deletar Projeto ---
                        with TabPane('Deletar', id='proj-delete-tab'):
                            yield SelectionList[int](
                                *self._get_proj_options(),
                                id='proj-delete-list',
                            )
                            yield Button(
                                'Deletar Selecionado',
                                variant='error',
                                id='delete-proj-button',
                                classes='mt1',
                            )

                # --- Aba de Usuários ---
                with TabPane('Usuários', id='user-tab'):
                    with TabbedContent(id='user-crud-tabs'):
                        # --- Criar Usuário ---
                        with TabPane('Criar', id='user-create-tab'):
                            yield Input(
                                placeholder='E-mail do Usuário',
                                id='user-email',
                            )
                            yield Input(
                                placeholder='Senha',
                                id='user-password',
                                password=True,
                                classes='mt1',
                            )
                            yield Select(
                                [('Admin', Role.ADMIN), ('User', Role.USER)],
                                prompt='Selecione a Role',
                                id='user-role-select',
                            )
                            yield Button(
                                'Salvar Novo Usuário',
                                variant='primary',
                                id='save-user-button',
                                classes='mt1',
                            )

                        # --- Listar/Editar Usuário ---
                        with TabPane('Listar/Editar', id='user-edit-tab'):
                            yield SelectionList[int](
                                *self._get_user_options(),
                                id='user-edit-list',
                            )
                            with Container(
                                id='user-edit-form', classes='hidden'
                            ):
                                yield Static(
                                    'Editando Usuário:', classes='text'
                                )
                                yield Input(
                                    id='user-edit-firstname',
                                    placeholder='Primeiro Nome',
                                )
                                yield Input(
                                    id='user-edit-lastname',
                                    placeholder='Sobrenome',
                                    classes='mt1',
                                )
                                yield Input(
                                    id='user-edit-email',
                                    disabled=True,
                                    classes='mt1',
                                )
                                yield Select(
                                    [
                                        ('Admin', Role.ADMIN),
                                        ('User', Role.USER),
                                    ],
                                    prompt='Selecione a Role',
                                    id='user-edit-role-select',
                                )
                                yield Button(
                                    'Salvar Alterações',
                                    id='update-user-button',
                                    variant='success',
                                    classes='mt1',
                                )

                        # --- Deletar Usuário ---
                        with TabPane('Deletar', id='user-delete-tab'):
                            yield SelectionList[int](
                                *self._get_user_options(),
                                id='user-delete-list',
                            )
                            yield Button(
                                'Deletar Selecionado',
                                variant='error',
                                id='delete-user-button',
                                classes='mt1',
                            )

        yield Footer()

    def _clear_and_repopulate_org_lists(self):
        """Atualiza todas as listas de organizações na tela."""
        new_options = self._get_org_options()

        # Atualiza lista de edição
        edit_list = self.query_one('#org-edit-list', SelectionList)
        edit_list.clear_options()
        edit_list.add_options(new_options)

        # Atualiza lista de deleção
        delete_list = self.query_one('#org-delete-list', SelectionList)
        delete_list.clear_options()
        delete_list.add_options(new_options)

        # Atualiza select no formulário de projetos
        proj_org_select = self.query_one('#proj-org-select', Select)
        proj_org_select.set_options(new_options)

    def _clear_and_repopulate_proj_lists(self):
        """Atualiza todas as listas de projetos na tela."""
        new_options = self._get_proj_options()

        # Atualiza lista de edição
        edit_list = self.query_one('#proj-edit-list', SelectionList)
        edit_list.clear_options()
        edit_list.add_options(new_options)

        # Atualiza lista de deleção
        delete_list = self.query_one('#proj-delete-list', SelectionList)
        delete_list.clear_options()
        delete_list.add_options(new_options)

    def _clear_and_repopulate_user_lists(self):
        """Atualiza todas as listas de usuários na tela."""
        new_options = self._get_user_options()

        # Atualiza lista de edição
        edit_list = self.query_one('#user-edit-list', SelectionList)
        edit_list.clear_options()
        edit_list.add_options(new_options)

        # Atualiza lista de deleção
        delete_list = self.query_one('#user-delete-list', SelectionList)
        delete_list.clear_options()
        delete_list.add_options(new_options)

    @on(SelectionList.SelectedChanged, '#org-edit-list')
    def on_org_selection_changed(self, event: SelectionList.SelectedChanged):
        """Preenche o formulário de edição quando uma organização é selecionada."""
        edit_form = self.query_one('#org-edit-form')
        # Acessa a lista de seleção a partir do evento
        if event.selection_list.selected:
            # Como é seleção única, pegamos o primeiro item da lista
            org_id = event.selection_list.selected[0]
            org = self._org_repo.get_by_id(org_id)

            if org:
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
                self.query_one('#org-edit-website', Input).value = org.website
                edit_form.remove_class('hidden')
        else:
            edit_form.add_class('hidden')

    @on(SelectionList.SelectedChanged, '#proj-edit-list')
    def on_proj_selection_changed(self, event: SelectionList.SelectedChanged):
        """Preenche o formulário de edição quando um projeto é selecionado."""
        edit_form = self.query_one('#proj-edit-form')
        if event.selection_list.selected:
            proj_id = event.selection_list.selected[0]
            # Usamos find_all_with_habilities para garantir que as habilidades venham juntas
            all_projects = self._proj_repo.find_all_with_habilities()
            proj = next((p for p in all_projects if p.id == proj_id), None)

            if proj:
                self.query_one('#proj-edit-name', Input).value = proj.name
                self.query_one(
                    '#proj-edit-description', Input
                ).value = proj.description
                self.query_one(
                    '#proj-edit-org-select', Select
                ).value = proj.organization_id

                hab_list = self.query_one('#proj-edit-hab-list', SelectionList)
                hab_list.deselect_all()
                for hability in proj.habilities:
                    hab_list.select(hability.id)
                edit_form.remove_class('hidden')
        else:
            edit_form.add_class('hidden')

    @on(SelectionList.SelectedChanged, '#user-edit-list')
    def on_user_selection_changed(self, event: SelectionList.SelectedChanged):
        """Preenche o formulário de edição quando um usuário é selecionado."""
        edit_form = self.query_one('#user-edit-form')
        if event.selection_list.selected:
            user_id = event.selection_list.selected[0]
            user = self._user_repo.get_by_id(user_id)

            if user:
                self.query_one('#user-edit-firstname', Input).value = (
                    user.first_name or ''
                )
                self.query_one('#user-edit-lastname', Input).value = (
                    user.last_name or ''
                )
                self.query_one('#user-edit-email', Input).value = user.email
                self.query_one(
                    '#user-edit-role-select', Select
                ).value = user.role.value
                edit_form.remove_class('hidden')
        else:
            edit_form.add_class('hidden')

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
                output_label.update('✅ Organização salva com sucesso!')
                self._clear_and_repopulate_org_lists()
                for input_widget in self.query('Input'):
                    if input_widget.id.startswith('org-'):
                        input_widget.value = ''
            except Exception as e:
                output_label.update(f'❌ Erro ao salvar organização: {e}')

        elif event.button.id == 'update-org-button':
            try:
                # Pega o primeiro (e único) ID da lista de seleção
                org_id = self.query_one('#org-edit-list').selected[0]
                if not org_id:
                    raise ValueError('Nenhuma organização selecionada.')

                updated_org = Organization(
                    id=org_id,
                    name=self.query_one('#org-edit-name').value,
                    description=self.query_one('#org-edit-description').value,
                    contact_email=self.query_one('#org-edit-email').value,
                    contact_phone=self.query_one('#org-edit-phone').value,
                    website=self.query_one('#org-edit-website').value,
                )
                self._org_repo.save(updated_org)
                output_label.update('✅ Organização atualizada com sucesso!')
                self._clear_and_repopulate_org_lists()
                self.query_one('#org-edit-form').add_class('hidden')
            except Exception as e:
                output_label.update(f'❌ Erro ao atualizar organização: {e}')

        elif event.button.id == 'delete-org-button':
            try:
                # Pega o primeiro (e único) ID da lista de seleção
                org_id = self.query_one('#org-delete-list').selected[0]
                if not org_id:
                    raise ValueError('Nenhuma organização selecionada.')

                deleted = self._org_repo.delete(org_id)
                if deleted:
                    output_label.update('✅ Organização deletada com sucesso!')
                    self._clear_and_repopulate_org_lists()
                else:
                    output_label.update('⚠️ Organização não encontrada.')
            except Exception as e:
                output_label.update(f'❌ Erro ao deletar organização: {e}')

        # --- Lógica de Projetos ---
        elif event.button.id == 'save-proj-button':
            try:
                hab_list = self.query_one('#proj-hab-list', SelectionList)

                proj = Project(
                    name=self.query_one('#proj-name').value,
                    description=self.query_one('#proj-description').value,
                    organization_id=self.query_one('#proj-org-select').value,
                    hability_ids=hab_list.selected,
                )
                self._proj_repo.save(proj)
                output_label.update('✅ Projeto salvo com sucesso!')
                self._clear_and_repopulate_proj_lists()
                for widget in self.query():
                    if isinstance(widget, Input) and widget.id.startswith(
                        'proj-'
                    ):
                        widget.value = ''
                hab_list.deselect_all()
            except Exception as e:
                output_label.update(f'❌ Erro ao salvar projeto: {e}')

        elif event.button.id == 'update-proj-button':
            try:
                proj_id = self.query_one('#proj-edit-list').selected[0]
                if not proj_id:
                    raise ValueError('Nenhum projeto selecionado.')

                hab_list = self.query_one('#proj-edit-hab-list', SelectionList)

                updated_proj = Project(
                    id=proj_id,
                    name=self.query_one('#proj-edit-name').value,
                    description=self.query_one('#proj-edit-description').value,
                    organization_id=self.query_one(
                        '#proj-edit-org-select'
                    ).value,
                    hability_ids=hab_list.selected,
                )
                self._proj_repo.save(updated_proj)
                output_label.update('✅ Projeto atualizado com sucesso!')
                self._clear_and_repopulate_proj_lists()
                self.query_one('#proj-edit-form').add_class('hidden')
            except Exception as e:
                output_label.update(f'❌ Erro ao atualizar projeto: {e}')

        elif event.button.id == 'delete-proj-button':
            try:
                proj_id = self.query_one('#proj-delete-list').selected[0]
                if not proj_id:
                    raise ValueError('Nenhum projeto selecionado.')

                deleted = self._proj_repo.delete(proj_id)
                if deleted:
                    output_label.update('✅ Projeto deletado com sucesso!')
                    self._clear_and_repopulate_proj_lists()
                else:
                    output_label.update('⚠️ Projeto não encontrado.')
            except Exception as e:
                output_label.update(f'❌ Erro ao deletar projeto: {e}')

        # --- Lógica de Usuários ---
        elif event.button.id == 'save-user-button':
            try:
                user = User(
                    email=self.query_one('#user-email').value,
                    password=self.query_one('#user-password').value,
                    role=self.query_one('#user-role-select').value,
                )
                self._user_repo.save(user)
                output_label.update('✅ Usuário salvo com sucesso!')
                self._clear_and_repopulate_user_lists()
                self.query_one('#user-email', Input).value = ''
                self.query_one('#user-password', Input).value = ''
            except Exception as e:
                output_label.update(f'❌ Erro ao salvar usuário: {e}')

        elif event.button.id == 'update-user-button':
            try:
                user_id = self.query_one('#user-edit-list').selected[0]
                if not user_id:
                    raise ValueError('Nenhum usuário selecionado.')

                # A senha não é atualizada aqui, apenas outros dados
                user_to_update = self._user_repo.get_by_id(user_id)
                if user_to_update:
                    user_to_update.first_name = self.query_one(
                        '#user-edit-firstname'
                    ).value
                    user_to_update.last_name = self.query_one(
                        '#user-edit-lastname'
                    ).value
                    user_to_update.role = self.query_one(
                        '#user-edit-role-select'
                    ).value

                    self._user_repo.save(user_to_update)
                    output_label.update('✅ Usuário atualizado com sucesso!')
                    self._clear_and_repopulate_user_lists()
                    self.query_one('#user-edit-form').add_class('hidden')
                else:
                    output_label.update('⚠️ Usuário não encontrado.')
            except Exception as e:
                output_label.update(f'❌ Erro ao atualizar usuário: {e}')

        elif event.button.id == 'delete-user-button':
            try:
                user_id = self.query_one('#user-delete-list').selected[0]
                if not user_id:
                    raise ValueError('Nenhum usuário selecionado.')

                # Adicionar verificação para não se auto-deletar
                if self.app.user and self.app.user.id == user_id:
                    output_label.update('❌ Você não pode deletar a si mesmo.')
                    return

                deleted = self._user_repo.delete(user_id)
                if deleted:
                    output_label.update('✅ Usuário deletado com sucesso!')
                    self._clear_and_repopulate_user_lists()
                else:
                    output_label.update('⚠️ Usuário não encontrado.')
            except Exception as e:
                output_label.update(f'❌ Erro ao deletar usuário: {e}')
