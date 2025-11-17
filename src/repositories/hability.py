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

        # Popula o banco de dados apenas se a conexão não for externa (evita popular em testes)
        if db_connection is None and self.count() == 0:
            self._populate()

    def get_dict_by_domain(self) -> dict:
        habilities = self.find_all()

        result = {}

        for hability in habilities:
            if hability.domain not in result:
                result[hability.domain] = []
            result[hability.domain].append(hability)
        return result

    def _populate(self) -> dict:
        populated_data = {}

        file = SEEDS_PATH / 'habilities.json'

        empty_db = self.count() == 0
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

                    if empty_db:
                        hability_obj = self.save(hability_obj)

                    populated_data[domain].append(hability_obj)
        logger.info(f'Banco de dados populado com {self.count()} habilidades.')
        return populated_data
