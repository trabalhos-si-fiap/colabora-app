from typing import Optional

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
    Static,
    TabbedContent,
    TabPane,
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
        self.all_projects: list[Project] = []  # projetos da página atual
        self.current_page: int = 1
        self.per_page: int = 2
        self.total_pages: int = 1
        super().__init__()

    def compose(self) -> ComposeResult:
        # Carrega os dados mais recentes ao compor a tela
        if self.user_id:
            self.user = self._user_repo.get_by_id_with_all_relations(
                self.user_id
            )

        yield Header(show_clock=True)
        with VerticalScroll(classes='bg with-border'):
            yield Static()  # Para funcionar o espaçamento
            yield Static(
                '[b]Projetos Disponíveis[/]', classes='text title pb pt'
            )
            yield Static(
                'Explore os projetos e inscreva-se naqueles que te interessam.',
                classes='text',
            )
            yield Static(
                'Para participar, você deve ter ao menos uma habilidade solicitada.',
                classes='text pb',
            )
            yield Input(
                placeholder='🔎  Buscar por nome ou descrição...',
                id='search-project',
                classes='input-margin-sm',
            )
            with TabbedContent(id='tabs'):
                with TabPane('Todos os Projetos', id='all-projects-tab'):
                    yield VerticalScroll(
                        id='project-list-container', classes='container'
                    )
                    yield Static(
                        'Página 1/1',
                        id='pagination-info',
                        classes='pagination-info',
                    )
                    with Horizontal(
                        id='pagination-container',
                    ):
                        yield Button(
                            '← Anterior',
                            id='prev-page',
                            classes='page-button',
                        )
                        yield Button(
                            'Próxima →',
                            id='next-page',
                            classes='page-button',
                        )
                with TabPane('Meus Projetos', id='my-projects-tab'):
                    yield VerticalScroll(
                        id='my-projects-container', classes='container'
                    )

        yield Footer()

    def on_mount(self) -> None:
        """Popula a lista de projetos quando a tela é montada."""
        self._update_my_projects_list()
        self._load_projects_page()

    def _load_projects_page(self) -> None:
        """Carrega a página atual de projetos do repositório, com paginação."""
        result = self._project_repo.find_all_with_habilities_paginated(
            page=self.current_page,
            per_page=self.per_page,
        )

        self.all_projects = result['data']
        self.total_pages = result['total_pages']
        self.current_page = result['page']  # garante que está consistente

        self._update_project_list(self.all_projects)
        self._update_pagination_info()

    def _update_pagination_info(self) -> None:
        """Atualiza o texto 'Página X/Y' e o estado dos botões."""
        info = self.query_one('#pagination-info', Static)
        info.update(f'Página {self.current_page}/{self.total_pages}')

        prev_btn = self.query_one('#prev-page', Button)
        next_btn = self.query_one('#next-page', Button)

        prev_btn.disabled = self.current_page <= 1
        next_btn.disabled = self.current_page >= self.total_pages

    @on(Button.Pressed, '#next-page')
    def _go_next_page(self, event: Button.Pressed) -> None:
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._load_projects_page()

    @on(Button.Pressed, '#prev-page')
    def _go_prev_page(self, event: Button.Pressed) -> None:
        if self.current_page > 1:
            self.current_page -= 1
            self._load_projects_page()

    def _update_project_list(self, projects: list[Project]) -> None:
        """Limpa e repopula o contêiner da lista de projetos."""
        # This method is now only called once from on_mount
        # The filtering logic will hide/show widgets instead of recreating them.
        container = self.query_one('#project-list-container')
        container.remove_children()
        for project in projects:
            container.mount(self._create_project_widget(project, prefix='all'))

    def _update_my_projects_list(self) -> None:
        """Popula a lista de projetos do usuário."""
        container = self.query_one('#my-projects-container')
        container.remove_children()
        if self.user:
            # Busca os projetos com as habilidades carregadas para evitar problemas
            project_ids = [p.id for p in self.user.projects]
            user_projects = self._project_repo.find_by_ids_with_all_relations(
                project_ids
            )
            for project in user_projects:
                container.mount(
                    self._create_project_widget(project, prefix='my')
                )

    @on(Input.Changed, '#search-project')
    def _filter_projects(self, event: Input.Changed) -> None:
        """Filtra a lista de projetos com base no texto de busca."""
        search_term = event.value.lower()
        all_projects_container = self.query_one('#project-list-container')

        # Filtra pela classe '.project-card' que é mais robusto
        for collapsible in all_projects_container.query('.project-card'):
            # Garante que estamos filtrando apenas os widgets da aba "Todos os Projetos"
            if collapsible.id and collapsible.id.startswith('all_project_'):
                project_id = int(collapsible.id.split('_')[-1])
                project = next(
                    (p for p in self.all_projects if p.id == project_id),
                    None,
                )
                if project:
                    matches = (
                        search_term in project.name.lower()
                        or search_term in project.description.lower()
                    )
                    collapsible.display = matches

    @on(Button.Pressed)
    def handle_subscription(self, event: Button.Pressed):
        """Lida com a inscrição e desinscrição de projetos."""
        if 'subscribe_btn' in event.button.id:
            project_id = int(
                event.button.id.split('_')[-1]
            )  # Ex: 'my_subscribe_btn_2' -> '2'
            project_to_toggle = self._project_repo.get_by_id(project_id)

            if not project_to_toggle:
                return

            # Recarrega o usuário para garantir que temos o estado mais recente
            self.user = self._user_repo.get_by_id_with_all_relations(
                self.user_id
            )

            msg = ''
            title = ''
            if self.user.is_subscribed_to(project_to_toggle):
                self.user.remove_project(project_to_toggle)
                msg = 'Remoção realizada com sucesso.'
                title = 'Cancelamento realizado'
                # Atualiza os dois botões (se existirem) para 'Inscrever-se'
                for btn in self.query(Button):
                    if btn.id and btn.id.endswith(
                        f'_subscribe_btn_{project_id}'
                    ):
                        btn.label = 'Inscrever-se'
                        btn.variant = 'success'
                # Remove o widget da aba "Meus Projetos"
                my_project_widget = self.query(f'#my_project_{project_id}')
                if my_project_widget:
                    my_project_widget.first().remove()
            else:
                self.user.add_project(project_to_toggle)
                msg = 'A organização entrará em contato com você.'
                title = 'Inscrição realizada com sucesso'
                # Atualiza os dois botões (se existirem) para 'Desinscrever-se'
                for btn in self.query(Button):
                    if btn.id and btn.id.endswith(
                        f'_subscribe_btn_{project_id}'
                    ):
                        btn.label = 'Desinscrever-se'
                        btn.variant = 'error'
                # Adiciona o widget na aba "Meus Projetos"
                my_projects_container = self.query_one(
                    '#my-projects-container'
                )
                project_with_habilities = (
                    self._project_repo.get_by_id_with_habilities(project_id)
                )
                my_projects_container.mount(
                    self._create_project_widget(
                        project_with_habilities, prefix='my'
                    )
                )

            # Salva o estado atualizado do usuário (com sua nova lista de projetos)
            self._user_repo.save(self.user)
            self.notify(msg, severity='information', title=title)

    def _create_project_widget(
        self, project: Project, prefix: str
    ) -> Collapsible:
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
            user_has_any_hability = any(
                self.user.has_hability(h) for h in project.habilities
            )

            if user_has_any_hability:
                is_subscribed = self.user.is_subscribed_to(project)
                children.append(
                    Container(
                        Button(
                            'Desinscrever-se'
                            if is_subscribed
                            else 'Inscrever-se',
                            variant='error' if is_subscribed else 'success',
                            id=f'{prefix}_subscribe_btn_{project.id}',
                            classes='subscribe-button center',
                        ),
                        classes='btn-save-pw mt',
                    )
                )
            else:
                children.append(
                    Static(
                        '\n[i]Você não tem ao menos uma habilidade solicitada.[/i]',
                        classes='text-center warning',
                    )
                )

        collapsible = Collapsible(
            *children,
            title=project.name,
            id=f'{prefix}_project_{project.id}',
            classes='input-margin-sm project-card',
        )
        collapsible.border_subtitle = (
            f'{len(project.habilities)} habilidades necessárias'
        )
        return collapsible
