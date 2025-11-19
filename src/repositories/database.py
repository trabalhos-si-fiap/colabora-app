import sqlite3
from typing import Optional

from loguru import logger

from src import BASE_PATH

DB_FILE = BASE_PATH / 'project_db.sqlite3'


class Database:
    """
    Classe Singleton para gerenciar a conexão com o banco de dados SQLite.
    """

    _instance: Optional['Database'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, connection: Optional[sqlite3.Connection] = None):
        if self._initialized:
            return

        if connection:
            # Usa a conexão fornecida (para testes em memória)
            self.connection = connection
        else:
            # Comportamento padrão: cria a conexão com o arquivo
            try:
                # 'check_same_thread=False' é útil para aplicações mais simples
                self.connection = sqlite3.connect(
                    DB_FILE, check_same_thread=False
                )
                logger.debug(f"Conexão com '{DB_FILE}' estabelecida.")
            except sqlite3.Error as e:
                logger.debug(f'Erro ao conectar ou criar banco de dados: {e}')
                raise

        # Isso faz o sqlite retornar resultados como dicionários (ou tipo 'Row')
        # Facilita muito o 'get_by_id'
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        # Garante que o schema e os índices sejam criados
        self._create_schema()
        self._create_indexes()   # Essencial para performance O(log N)

        self._initialized = True

    def get_cursor(self) -> sqlite3.Cursor:
        return self.cursor

    def get_connection(self) -> sqlite3.Connection:
        return self.connection

    def close(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()
            logger.debug(f"Conexão com '{DB_FILE}' fechada.")

    def _execute_script(self, script: str):
        """Executa um script SQL (pode conter múltiplos comandos)."""
        try:
            self.cursor.executescript(script)
            self.connection.commit()
        except sqlite3.Error as e:
            logger.debug(f'Erro ao executar script: {e}')

    def _create_schema(self):
        """
        Cria as tabelas principais e as tabelas de junção para relacionamentos N-N.
        """
        schema_script = """
        -- Modelos Principais
        
        CREATE TABLE IF NOT EXISTS Organization (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            contact_email TEXT UNIQUE,
            contact_phone TEXT,
            website TEXT
        );

        CREATE TABLE IF NOT EXISTS Hability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            domain TEXT
        );

        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT, -- SQLite não tem tipo 'date', usamos TEXT (ISO 8601)
            phone TEXT,
            role TEXT NOT NULL DEFAULT 'USER'
        );

        CREATE TABLE IF NOT EXISTS Project (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            
            -- Relacionamento 1-para-N (ForeignKey)
            -- Um Projeto pertence a UMA Organização
            organization_id INTEGER,
            FOREIGN KEY (organization_id) REFERENCES Organization(id)
        );

        -- Tabelas de Junção (Relacionamentos N-para-N)

        CREATE TABLE IF NOT EXISTS User_Habilities (
            user_id INTEGER,
            hability_id INTEGER,
            PRIMARY KEY (user_id, hability_id),
            FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
            FOREIGN KEY (hability_id) REFERENCES Hability(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS User_Projects (
            user_id INTEGER,
            project_id INTEGER,
            PRIMARY KEY (user_id, project_id),
            FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
            FOREIGN KEY (project_id) REFERENCES Project(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Project_Habilities (
            project_id INTEGER,
            hability_id INTEGER,
            PRIMARY KEY (project_id, hability_id),
            FOREIGN KEY (project_id) REFERENCES Project(id) ON DELETE CASCADE,
            FOREIGN KEY (hability_id) REFERENCES Hability(id) ON DELETE CASCADE
        );
        """
        logger.debug('Criando esquema do banco de dados...')
        self._execute_script(schema_script)
        logger.debug('Esquema criado com sucesso.')

    def _create_indexes(self):
        """
        Cria índices para buscas rápidas O(log N).
        """
        index_script = """
        -- Índice para busca de usuário por email (O(log N))
        CREATE INDEX IF NOT EXISTS idx_user_email ON User(email);
        
        -- Índices para buscas por nome
        CREATE INDEX IF NOT EXISTS idx_hability_name ON Hability(name);
        CREATE INDEX IF NOT EXISTS idx_project_name ON Project(name);

        -- Índices nas chaves estrangeiras (aceleram JOINs)
        CREATE INDEX IF NOT EXISTS idx_project_organization_id ON Project(organization_id);
        CREATE INDEX IF NOT EXISTS idx_user_habilities_user ON User_Habilities(user_id);
        CREATE INDEX IF NOT EXISTS idx_user_habilities_hability ON User_Habilities(hability_id);
        CREATE INDEX IF NOT EXISTS idx_project_habilities_project ON Project_Habilities(project_id);
        CREATE INDEX IF NOT EXISTS idx_project_habilities_hability ON Project_Habilities(hability_id);
        CREATE INDEX IF NOT EXISTS idx_user_projects_user ON User_Projects(user_id);
        CREATE INDEX IF NOT EXISTS idx_user_projects_project ON User_Projects(project_id);
        """
        logger.debug('Criando índices para performance O(log N)...')
        self._execute_script(index_script)
        logger.debug('Índices criados com sucesso.')
