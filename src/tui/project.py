from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Collapsible,
    Footer,
    Header,
    Input,
    Static,
)

from src.models import Project, User
from src.repositories import ProjectRepository, UserRepository


class ProjectScreen(Screen):
    """Tela para listar e interagir com projetos."""

    BINDINGS = [('escape', 'app.pop_screen', 'Voltar')]

    def __init__(
        self,
        user: Optional[User],
        user_repository: UserRepository,
        project_repository: ProjectRepository,
    ):
        self.user = user
        self.user_id = user.id if user else None
        self._user_repo = user_repository
        self._project_repo = project_repository
        self.all_projects = []  # Armazena todos os projetos para filtrar
        super().__init__()

    def compose(self) -> ComposeResult:
        # Carrega os dados mais recentes ao compor a tela
        if self.user_id:
            self.user = self._user_repo.get_by_id_with_all_relations(
                self.user_id
            )
        self.all_projects = self._project_repo.find_all_with_habilities()

        yield Header(show_clock=True)
        with VerticalScroll(classes='bg with-border'):
            yield Static('Projetos Disponíveis', classes='text title')
            yield Static(
                'Explore os projetos e inscreva-se naqueles que te interessam.',
                classes='text',
            )

            yield Input(
                placeholder='🔎 Buscar por nome ou descrição...',
                id='search-project',
            )
            # Este contêiner será preenchido dinamicamente
            yield VerticalScroll(id='project-list-container')

        yield Footer()

    def on_mount(self) -> None:
        """Popula a lista de projetos quando a tela é montada."""
        self._update_project_list(self.all_projects)

    def _update_project_list(self, projects: list[Project]) -> None:
        """Limpa e repopula o contêiner da lista de projetos."""
        # This method is now only called once from on_mount
        # The filtering logic will hide/show widgets instead of recreating them.
        container = self.query_one('#project-list-container')
        for project in projects:
            container.mount(self._create_project_widget(project))

    @on(Input.Changed, '#search-project')
    def _filter_projects(self, event: Input.Changed) -> None:
        """Filtra a lista de projetos com base no texto de busca."""
        search_term = event.value.lower()
        for collapsible in self.query(Collapsible):
            # Find the corresponding project object for this widget
            project_id = int(collapsible.id.split('_')[-1])
            project = next(
                (p for p in self.all_projects if p.id == project_id), None
            )
            if project:
                # Show or hide the widget based on the filter
                matches = (
                    search_term in project.name.lower()
                    or search_term in project.description.lower()
                )
                collapsible.display = matches

    @on(Button.Pressed)
    def handle_subscription(self, event: Button.Pressed):
        """Lida com a inscrição e desinscrição de projetos."""
        if 'subscribe_btn_' in event.button.id:
            project_id = int(event.button.id.split('_')[-1])
            project_to_toggle = self._project_repo.get_by_id(project_id)

            if not project_to_toggle:
                return

            # Recarrega o usuário para garantir que temos o estado mais recente
            self.user = self._user_repo.get_by_id_with_all_relations(
                self.user_id
            )

            if self.user.is_subscribed_to(project_to_toggle):
                self.user.remove_project(project_to_toggle)
                event.button.label = 'Inscrever-se'
                event.button.variant = 'success'
            else:
                self.user.add_project(project_to_toggle)
                event.button.label = 'Desinscrever-se'
                event.button.variant = 'error'

            # Salva o estado atualizado do usuário (com sua nova lista de projetos)
            self._user_repo.save(self.user)

    def _create_project_widget(self, project: Project) -> Collapsible:
        """Cria um widget Collapsible para um único projeto."""
        children = [
            Static(project.description, classes='text'),
            Static('[bold]Habilidades Necessárias:[/bold]', classes='text'),
        ]
        for hability in project.habilities:
            has_it = self.user.has_hability(hability) if self.user else False
            icon = '✅' if has_it else '❌'
            children.append(Static(f' {icon} {hability.name}', classes='text'))

        if self.user:
            is_subscribed = self.user.is_subscribed_to(project)
            children.append(
                Button(
                    'Desinscrever-se' if is_subscribed else 'Inscrever-se',
                    variant='error' if is_subscribed else 'success',
                    id=f'subscribe_btn_{project.id}',
                    classes='subscribe-button',
                )
            )

        collapsible = Collapsible(
            *children, title=project.name, id=f'project_{project.id}'
        )
        collapsible.border_subtitle = (
            f'{len(project.habilities)} habilidades necessárias'
        )
        return collapsible
