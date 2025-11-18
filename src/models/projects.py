from typing import Optional

from src.models import Hability, Organization


class Project:
    def __init__(
        self,
        name: str,
        description: str,
        organization: Optional[Organization] = None,
        habilities: list[Hability] = None,
        id: Optional[int] = None,
        organization_id: Optional[int] = None,
        hability_ids: list[int] = None,
    ):
        self.name = name
        self.description = description
        self.organization = organization
        # O organization_id é usado principalmente para a criação a partir do banco de dados
        self.organization_id = (
            organization.id if organization else organization_id
        )
        self.habilities = [] if habilities is None else habilities
        self.hability_ids = hability_ids or []
        self.id = id

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'organization_id': self.organization_id,
            'habilities': self.habilities,
            'hability_ids': self.hability_ids,
        }

    def has_hability(self, hability: Hability) -> bool:
        """Verifica se o projeto requer uma habilidade específica."""
        if hability is None or hability.id is None:
            return False
        return any(h.id == hability.id for h in self.habilities)
