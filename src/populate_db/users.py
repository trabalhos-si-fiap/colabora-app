import json

from loguru import logger

from src import SEEDS_PATH
from src.models.hability import Hability
from src.models.organizations import Organization
from src.models.projects import Project
from src.repositories.hability import HabilityRepository
from src.repositories.organization import OrganizationRepository
from src.repositories.project import ProjectRepository
from src.repositories.user import UserRepository


class PopulateRawDB:
    def __init__(self):
        self.user_repository = UserRepository()
        self.organization_repository = OrganizationRepository()
        self.project_repository = ProjectRepository()
        self.hability_repository = HabilityRepository()

    def run(self):
        self.populate_users()
        self.populate_organizations()
        self.populate_habilities()
        self.populate_projects()

    def populate_users(self) -> None:
        """Popula o banco de dados com usuários do arquivo JSON."""

        if self.user_repository.count() != 0:
            return

        from src.use_cases.register import RegisterUserUseCase

        logger.info('Populando tabela de Usuários...')
        file_path = SEEDS_PATH / 'users.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            for user_data in users_data:
                user, _ = RegisterUserUseCase.factory().execute(
                    email=user_data['email'], password=user_data['password']
                )
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.role = user_data['role']
                self.user_repository.save(user)

        logger.info(
            f'Tabela de Usuários populada com {self.user_repository.count()} usuários.'
        )

    def populate_organizations(self) -> None:
        """Popula o banco de dados com organizações do arquivo JSON."""
        if self.organization_repository.count() != 0:
            return

        logger.info('Populando tabela de Organizações...')
        file_path = SEEDS_PATH / 'organizations.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            organizations_data = json.load(f)
            for org_data in organizations_data:
                organization = Organization(**org_data)
                self.organization_repository.save(organization)
        logger.info(
            f'Tabela de Organizações populada com {self.organization_repository.count()} organizações.'
        )

    def populate_projects(self) -> None:
        """Popula o banco de dados com projetos do arquivo JSON."""

        if self.project_repository.count() != 0:
            return

        logger.info('Populando tabela de Projetos...')
        file_path = SEEDS_PATH / 'projects.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for project_data in data['projects']:
                habilities_names = project_data.pop('required_habilities', [])
                project = Project(**project_data)
                project.habilities = self.hability_repository.find_by_names(
                    habilities_names
                )
                self.project_repository.save(project)

        logger.info(
            f'Tabela de Projetos populada com {self.project_repository.count()} projetos.'
        )

    def populate_habilities(self) -> None:
        """Popula o banco de dados com habilidades do arquivo JSON."""

        if self.hability_repository.count() != 0:
            return

        logger.info('Populando tabela de Habilidades...')
        file = SEEDS_PATH / 'habilities.json'
        populated_data = {}

        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

            for domain, habilities_list in data.items():
                populated_data[domain] = []
                for hability_dict in habilities_list:
                    hability_obj = Hability(
                        name=hability_dict['name'],
                        description=hability_dict['description'],
                        domain=domain,
                    )

                    hability_obj = self.hability_repository.save(hability_obj)

                    populated_data[domain].append(hability_obj)
        logger.info(
            f'Banco de dados populado com {self.hability_repository.count()} habilidades.'
        )
