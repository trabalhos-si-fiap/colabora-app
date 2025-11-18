import json
import sqlite3
from typing import Optional

from loguru import logger

from src import SEEDS_PATH
from src.models import Organization
from src.repositories import BaseRepository


class OrganizationRepository(BaseRepository):
    def __init__(self, db_connection: Optional[sqlite3.Connection] = None):
        super().__init__('Organization', Organization, db_connection)
        if db_connection is None and self.count() == 0:
            self._populate()

    def _populate(self):
        """Popula o banco de dados com organizações do arquivo JSON."""
        logger.info('Populando tabela de Organizações...')
        file_path = SEEDS_PATH / 'organizations.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            organizations_data = json.load(f)
            for org_data in organizations_data:
                organization = Organization(**org_data)
                self.save(organization)
        logger.info(
            f'Tabela de Organizações populada com {self.count()} organizações.'
        )
