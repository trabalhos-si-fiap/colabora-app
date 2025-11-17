from src.models import Organization
from src.repositories import BaseRepository


class OrganizationRepository(BaseRepository):
    def __init__(self):
        super().__init__('Organization', Organization)
