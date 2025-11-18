import json
import sqlite3
from typing import Optional

from loguru import logger

from src import SEEDS_PATH
from src.models import Hability, Project
from src.repositories import (
    BaseRepository,
    HabilityRepository,
    OrganizationRepository,
)


class ProjectRepository(BaseRepository):
    def __init__(self, db_connection: Optional[sqlite3.Connection] = None):
        super().__init__('Project', Project, db_connection)
        # Garante que as dependências sejam inicializadas (e populadas) primeiro
        self.hability_repo = HabilityRepository(db_connection)
        self.org_repo = OrganizationRepository(db_connection)
        if db_connection is None and self.count() == 0:
            self._populate()

    def save(self, project: Project) -> Project:
        """
        Sobrescreve o .save() base para lidar com o relacionamento
        N-N com Hability.
        """
        habilities_to_save = project.habilities.copy()
        saved_project = super().save(project)

        if saved_project and saved_project.id is not None:
            self._sync_habilities(saved_project.id, habilities_to_save)

        return saved_project

    def _sync_habilities(self, project_id: int, habilities: list[Hability]):
        """Sincroniza a tabela Project_Habilities."""
        try:
            sql_delete = 'DELETE FROM Project_Habilities WHERE project_id = ?'
            self.cursor.execute(sql_delete, (project_id,))

            habilities_with_ids = [
                h.id for h in habilities if h.id is not None
            ]
            if habilities_with_ids:
                sql_insert = 'INSERT INTO Project_Habilities (project_id, hability_id) VALUES (?, ?)'
                data_to_insert = [
                    (project_id, h_id) for h_id in habilities_with_ids
                ]
                self.cursor.executemany(sql_insert, data_to_insert)

            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(
                f'Erro ao sincronizar habilidades para project_id {project_id}: {e}'
            )
            self.conn.rollback()
            raise

    def _populate(self):
        """Popula o banco de dados com projetos do arquivo JSON."""
        logger.info('Populando tabela de Projetos...')
        file_path = SEEDS_PATH / 'projects.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for project_data in data['projects']:
                habilities_names = project_data.pop('required_habilities', [])
                project = Project(**project_data)
                project.habilities = self.hability_repo.find_by_names(
                    habilities_names
                )
                self.save(project)
        logger.info(
            f'Tabela de Projetos populada com {self.count()} projetos.'
        )

    def get_by_id_with_habilities(self, project_id: int) -> Optional[Project]:
        """Busca um projeto e já carrega suas habilidades necessárias."""
        project = self.get_by_id(project_id)
        if project:
            project.habilities = self.get_habilities_for_project(project_id)
        return project

    def find_all_with_habilities(self) -> list[Project]:
        """Busca todos os projetos e suas habilidades."""
        projects = self.find_all()
        for project in projects:
            project.habilities = self.get_habilities_for_project(project.id)
        return projects

    def get_habilities_for_project(self, project_id: int) -> list[Hability]:
        """Busca todas as HABILIDADES de um projeto."""
        sql = """
        SELECT h.* FROM Hability h
        JOIN Project_Habilities ph ON h.id = ph.hability_id
        WHERE ph.project_id = ?
        """
        self.cursor.execute(sql, (project_id,))
        rows = self.cursor.fetchall()
        return [self.hability_repo._map_row_to_model(row) for row in rows]
