from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
PICKLE_PATH = BASE_PATH / 'pickle'
SEEDS_PATH = BASE_PATH / 'seeds'

import sys

from loguru import logger
from textual.logging import TextualHandler

logger.remove()
logger.add(TextualHandler(), level='DEBUG')
logger.add(
    'meu_app.log',
    level='DEBUG',
    rotation='10 MB',
    retention=5,
    format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}',  # Formato detalhado
)
