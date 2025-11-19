import json
import sqlite3
from typing import Optional, overload

from loguru import logger

from src import SEEDS_PATH
from src.models import Project
from src.models.hability import Hability
from src.models.users import User
from src.repositories.base_repository import BaseRepository
from src.repositories.hability import HabilityRepository
from src.repositories.project import ProjectRepository


class UserRepository(BaseRepository):
    def __init__(self, db_connection: Optional[sqlite3.Connection] = None):
        super().__init__('User', User, db_connection)
        self.hability_repo = HabilityRepository(db_connection)
        self.project_repo = ProjectRepository(db_connection)

    def save(self, user: User) -> User:
        """
        Sobrescreve o .save() base para lidar com o relacionamento
        N-N com Hability.
        """
        logger.info('Save user called.')
        habilities_to_save = user.habilities.copy()
        projects_to_save = user.projects.copy()

        saved_user = super().save(user)

        if saved_user and saved_user.id is not None:
            self._sync_habilities(saved_user.id, habilities_to_save)
            self._sync_projects(saved_user.id, projects_to_save)

        return saved_user

    def _sync_habilities(self, user_id: int, habilities: list[Hability]):
        """
        Sincroniza a tabela User_Habilities.
        A forma mais simples e robusta: apaga todos e insere os atuais.
        """
        logger.info(f'Sync Habilities called with user_id={user_id}')
        try:
            sql_delete = 'DELETE FROM User_Habilities WHERE user_id = ?'
            self.cursor.execute(sql_delete, (user_id,))

            habilities_with_ids = [
                h.id for h in habilities if h.id is not None
            ]

            logger.debug(f'{habilities_with_ids=}')

            if habilities_with_ids:
                # Prepara um INSERT em lote
                sql_insert = 'INSERT INTO User_Habilities (user_id, hability_id) VALUES (?, ?)'
                data_to_insert = [
                    (user_id, h_id) for h_id in habilities_with_ids
                ]

                self.cursor.executemany(sql_insert, data_to_insert)

            self.conn.commit()

        except sqlite3.Error as e:
            logger.error(
                f'Erro ao sincronizar habilidades para user_id {user_id}: {e}'
            )
            self.conn.rollback()   # Desfaz a transação em caso de erro
            raise

    def _sync_projects(self, user_id: int, projects: list[Project]):
        """
        Sincroniza a tabela User_Projects.
        Apaga todos os relacionamentos e insere os atuais.
        """
        logger.info(f'Sync Projects called with user_id={user_id}')
        try:
            sql_delete = 'DELETE FROM User_Projects WHERE user_id = ?'
            self.cursor.execute(sql_delete, (user_id,))

            projects_with_ids = [p.id for p in projects if p.id is not None]

            if projects_with_ids:
                sql_insert = 'INSERT INTO User_Projects (user_id, project_id) VALUES (?, ?)'
                data_to_insert = [
                    (user_id, p_id) for p_id in projects_with_ids
                ]
                self.cursor.executemany(sql_insert, data_to_insert)

            self.conn.commit()

        except sqlite3.Error as e:
            logger.error(
                f'Erro ao sincronizar projetos para user_id {user_id}: {e}'
            )
            self.conn.rollback()
            raise

    def get_by_email(self, email: str) -> Optional[User]:
        """Busca O(log N) por email e retorna um objeto User."""
        self.cursor.execute(
            f'SELECT * FROM {self.table_name} WHERE email = ?', (email,)
        )
        row = self.cursor.fetchone()
        return self._map_row_to_model(row)

    def get_by_id_with_habilities(self, user_id: int) -> Optional[User]:
        """Busca um usuário e já carrega suas habilidades."""
        user = self.get_by_id(user_id)
        if user:
            user.habilities = self.get_habilities_for_user(user_id)
        return user

    def get_by_id_with_all_relations(self, user_id: int) -> Optional[User]:
        """Busca um usuário e carrega todas as suas relações (habilidades e projetos)."""
        user = self.get_by_id(user_id)
        if user:
            user.habilities = self.get_habilities_for_user(user_id)
            user.projects = self.get_projects_for_user(user_id)
        return user

    def add_hability(self, user_id: int, hability_id: int) -> bool:
        """Adiciona um relacionamento N-N na tabela de junção."""
        sql = (
            'INSERT INTO User_Habilities (user_id, hability_id) VALUES (?, ?)'
        )
        try:
            self.cursor.execute(sql, (user_id, hability_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f'Erro ao relacionar usuário e habilidade: {e}')
            return False

    @overload
    def exists(self, id: int) -> bool:
        ...

    @overload
    def exists(self, email: str) -> bool:
        ...

    def exists(self, arg: int | str) -> bool:
        """
        Verifica de forma otimizada (O(log N)) se um email já existe.
        """

        match arg:
            case str():
                sql = f'SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE email = ?)'
            case int():
                sql = f'SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id = ?)'
            case _:
                return False

        self.cursor.execute(
            sql,
            (arg,),
        )
        result = self.cursor.fetchone()

        # O resultado será (1,) se existir ou (0,) se não existir.
        return result[0] == 1

    def get_habilities_for_user(self, user_id: int) -> list[Hability]:
        """Busca todas as HABILIDADES de um usuário."""
        sql = """
        SELECT h.* FROM Hability h
        JOIN User_Habilities uh ON h.id = uh.hability_id
        WHERE uh.user_id = ?
        """
        self.cursor.execute(sql, (user_id,))
        rows = self.cursor.fetchall()
        # Usa o mapper do repositório de Habilidade!
        return [self.hability_repo._map_row_to_model(row) for row in rows]

    def get_projects_for_user(self, user_id: int) -> list[Project]:
        """Busca todos os PROJETOS de um usuário."""
        sql = """
        SELECT p.* FROM Project p
        JOIN User_Projects up ON p.id = up.project_id
        WHERE up.user_id = ?
        """
        self.cursor.execute(sql, (user_id,))
        rows = self.cursor.fetchall()
        return [self.project_repo._map_row_to_model(row) for row in rows]
