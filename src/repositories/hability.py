import json
import sqlite3
from typing import Optional

from loguru import logger

from src import SEEDS_PATH
from src.models.hability import Hability
from src.repositories.base_repository import BaseRepository


class HabilityRepository(BaseRepository):
    def __init__(self, db_connection: Optional[sqlite3.Connection] = None):
        super().__init__('Hability', Hability, db_connection)

    def get_dict_by_domain(self) -> dict:
        habilities = self.find_all()

        result = {}

        for hability in habilities:
            if hability.domain not in result:
                result[hability.domain] = []
            result[hability.domain].append(hability)
        return result
    
    def find_by_ids(self, hability_ids: list[int]) -> list[Hability]:
        """Busca uma lista de habilidades por seus IDs."""
        if not hability_ids:
            return []
        placeholders = ','.join('?' for _ in hability_ids)
        sql = f'SELECT * FROM {self.table_name} WHERE id IN ({placeholders})'
        self.cursor.execute(sql, hability_ids)
        rows = self.cursor.fetchall()
        return [self._map_row_to_model(row) for row in rows]

    def find_by_names(self, names: list[str]) -> list[Hability]:
        """Busca uma lista de habilidades por seus nomes."""
        if not names:
            return []
        placeholders = ','.join('?' for _ in names)
        sql = f'SELECT * FROM {self.table_name} WHERE name IN ({placeholders})'
        self.cursor.execute(sql, names)
        rows = self.cursor.fetchall()
        return [self._map_row_to_model(row) for row in rows]


