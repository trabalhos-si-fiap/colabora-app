import sqlite3
from typing import Optional

from src import PICKLE_PATH
from src.models import Project
from src.models.hability import Hability
from src.repositories import (
    BaseRepository,
    HabilityRepository,
    OrganizationRepository,
)


class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__('Project', Project)
        self.org_repo = OrganizationRepository()
        self.hability_repo = HabilityRepository()

    def get_by_id_with_details(self, project_id: int) -> Optional[Project]:
        """
        Busca um projeto e já carrega sua Organização (1-N)
        e suas Habilidades (N-N). (Eager Loading)
        """
        project = self.get_by_id(project_id)
        if project:
            project.organization = self.org_repo.get_by_id(
                project.organization_id
            )
            project.habilities = self.get_habilities_for_project(project_id)
        return project

    def add_hability(self, project_id: int, hability_id: int) -> bool:
        """Adiciona um relacionamento N-N na tabela de junção."""
        sql = 'INSERT INTO Project_Habilities (project_id, hability_id) VALUES (?, ?)'
        try:
            self.cursor.execute(sql, (project_id, hability_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f'Erro ao relacionar projeto e habilidade: {e}')
            return False

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
