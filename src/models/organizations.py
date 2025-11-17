class Organization:
    def __init__(
        self,
        name: str,
        description: str,
        contact_email: str,
        contact_phone: str,
        website: str,
        id: int = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.website = website

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'website': self.website,
        }
