from src.models import Hability, Organization


class Project:
    def __init__(
        self,
        name: str,
        description: str,
        organization: Organization,
        habilities: list[Hability],
    ):
        self.name = name
        self.description = description
        self.organization = organization
        self.habilities = habilities

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'organization': self.organization,
            'habilities': self.habilities,
        }
