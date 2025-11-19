import sqlite3
from typing import List, Optional, Type, TypeVar

from loguru import logger

from .database import Database

T = TypeVar('T')


class BaseRepository:
    """
    Classe base para Repositórios que mapeia automaticamente
    linhas do banco para instâncias de modelo.
    """

    def __init__(
        self,
        table_name: str,
        model_cls: Type[T],
        db_connection: Optional[sqlite3.Connection] = None,
    ):
        # Se uma conexão for passada, usa-a. Senão, usa o Singleton.
        self.db = Database(connection=db_connection)
        self.conn = self.db.connection
        self.cursor = self.db.cursor
        self.table_name = table_name
        self.model_cls = model_cls

    def _map_row_to_model(self, row: sqlite3.Row) -> Optional[T]:
        """Converte uma linha do sqlite3 (que age como dict) em uma instância do modelo."""
        if row is None:
            return None
        # Usa **dict(row) para "desempacotar" os nomes das colunas
        # nos argumentos do __init__ do modelo
        return self.model_cls(**dict(row))

    def save(self, model_instance: T) -> T:
        """
        Salva uma instância no banco (cria ou atualiza).
        Chama _create() se o ID for None, ou _update() se o ID existir.
        Retorna a instância salva (com ID, se for nova).
        """
        if model_instance.id is None:
            # É um novo registro -> INSERT
            logger.debug(f'Chamando _create para {model_instance}')
            return self._create(model_instance)
        else:
            # É um registro existente -> UPDATE
            logger.debug(f'Chamando _update para {model_instance}')
            return self._update(model_instance)

    def count(self) -> int:
        """Retorna a contagem de registros na tabela."""
        sql = f'SELECT COUNT(*) FROM {self.table_name}'
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def _pop_relations(self, data):
        data.pop('organization', None)
        data.pop('habilities', None)
        data.pop('projects', None)
        data.pop('hability_ids', None)
        return data

    def _create(self, model_instance: T) -> T:
        """
        Cria um novo registro a partir de uma instância de modelo.
        Atualiza a instância com o ID gerado e a retorna.
        """
        # Converte o objeto em um dict

        data = model_instance.to_dict()

        # Remove atributos que não são colunas (como os objetos de relacionamento)
        data.pop(
            'id', None
        )  # Remove 'id' se existir (para não enviar no INSERT)

        data = self._pop_relations(data)

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = list(data.values())

        sql = f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})'

        try:
            self.cursor.execute(sql, values)
            new_id = self.cursor.lastrowid
            self.conn.commit()

            # ATUALIZA a instância original com o novo ID
            model_instance.id = new_id
            return model_instance
        except sqlite3.Error as e:
            logger.error(f"Erro ao criar em '{self.table_name}': {e}")
            raise  # Lança a exceção para a camada de serviço tratar

    def get_by_id(self, id: int) -> Optional[T]:
        """Busca um registro pelo ID e o retorna como uma instância do modelo."""
        sql = f'SELECT * FROM {self.table_name} WHERE id = ?'
        self.cursor.execute(sql, (id,))
        row = self.cursor.fetchone()
        return self._map_row_to_model(row)

    def find_all(self) -> List[T]:
        """Retorna todos os registros da tabela como uma lista de instâncias do modelo."""
        sql = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [self._map_row_to_model(row) for row in rows]

    def find_paginated(self, page: int = 1, per_page: int = 5):
        if page < 1:
            raise ValueError('page must be >= 1')

        offset = (page - 1) * per_page

        sql = f'SELECT * FROM {self.table_name} LIMIT ? OFFSET ?'
        self.cursor.execute(sql, (per_page, offset))

        rows = self.cursor.fetchall()
        return [self._map_row_to_model(row) for row in rows]

    def _update(self, model_instance: T) -> T:
        """
        Atualiza um registro a partir de uma instância de modelo (deve ter um ID).
        Retorna a instância do modelo atualizada.
        """
        if model_instance.id is None:
            raise ValueError('Não é possível atualizar um modelo sem ID.')

        data = model_instance.to_dict().copy()
        id_val = data.pop('id')

        data = self._pop_relations(data)

        set_clauses = ', '.join([f'{key} = ?' for key in data.keys()])
        values = list(data.values())
        values.append(id_val)

        sql = f'UPDATE {self.table_name} SET {set_clauses} WHERE id = ?'

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            if self.cursor.rowcount == 0:
                logger.warning(
                    f'Aviso: UPDATE em {self.table_name} (id={id_val}) não afetou linhas.'
                )
            return model_instance

        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar em '{self.table_name}': {e}")
            raise

    def delete(self, id: int) -> bool:
        """Deleta um registro pelo ID."""
        sql = f'DELETE FROM {self.table_name} WHERE id = ?'
        try:
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.debug(f"Erro ao deletar em '{self.table_name}': {e}")
            return False
