import json
import sqlite3
from typing import Optional

from src.models import Organization
from src.repositories import BaseRepository


class OrganizationRepository(BaseRepository):
    def __init__(self, db_connection: Optional[sqlite3.Connection] = None):
        super().__init__('Organization', Organization, db_connection)

    def find_by_ids(self, org_ids: list[int]) -> list[Organization]:
        """Busca uma lista de organizações por seus IDs."""
        if not org_ids:
            return []
        placeholders = ','.join('?' for _ in org_ids)
        sql = f'SELECT * FROM {self.table_name} WHERE id IN ({placeholders})'
        self.cursor.execute(sql, org_ids)
        return [self._map_row_to_model(r) for r in self.cursor.fetchall()]