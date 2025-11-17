class Hability:
    def __init__(
        self, name: str, description: str, domain: str, id: int = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.domain = domain

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'domain': self.domain,
        }

    def __repr__(self):
        return f"<Hability(id={self.id}, name='{self.name}')>"

    def __eq__(self, other):
        if not isinstance(other, Hability):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
