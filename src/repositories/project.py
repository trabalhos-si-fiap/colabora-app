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


    def find_by_ids_with_all_relations(self, project_ids: list[int]) -> list[Project]:
        """
        Busca uma lista de projetos por seus IDs e carrega suas relações
        (habilidades e organização) de forma otimizada (evitando N+1 queries).
        """
        if not project_ids:
            return []

        # 1. Busca todos os projetos de uma vez
        placeholders = ','.join('?' for _ in project_ids)
        sql_projects = f'SELECT * FROM {self.table_name} WHERE id IN ({placeholders}) ORDER BY name'
        self.cursor.execute(sql_projects, project_ids)
        projects = [self._map_row_to_model(r) for r in self.cursor.fetchall()]
        projects_dict = {p.id: p for p in projects}

        # 2. Busca todas as organizações necessárias de uma vez
        org_ids = {p.organization_id for p in projects if p.organization_id}
        if org_ids:
            orgs = self.org_repo.find_by_ids(list(org_ids))
            orgs_dict = {o.id: o for o in orgs}
            for project in projects:
                if project.organization_id in orgs_dict:
                    project.organization = orgs_dict[project.organization_id]

        # 3. Busca todas as habilidades para esses projetos de uma vez
        sql_habilities = f"""
            SELECT p.id as project_id, h.* FROM Hability h
            JOIN Project_Habilities ph ON h.id = ph.hability_id
            JOIN Project p ON p.id = ph.project_id
            WHERE p.id IN ({placeholders})
        """
        self.cursor.execute(sql_habilities, project_ids)
        for db_row in self.cursor.fetchall():
            row_dict = dict(db_row)
            project_id = row_dict.pop('project_id')
            hability = self.hability_repo._map_row_to_model(row_dict)
            if project_id in projects_dict and hability:
                projects_dict[project_id].habilities.append(hability)

        return projects

    def get_by_id_with_habilities(self, project_id: int) -> Optional[Project]:
        """Busca um projeto e já carrega suas relações (habilidades e organização)."""
        results = self.find_by_ids_with_all_relations([project_id])
        return results[0] if results else None

    def find_all_with_habilities(self) -> list[Project]:
        """Busca todos os projetos e suas relações (habilidades e organização)."""
        projects = self.find_all()
        if not projects:
            return []

        project_ids = [p.id for p in projects]
        return self.find_by_ids_with_all_relations(project_ids)

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
