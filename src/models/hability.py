import json
from src import SEEDS_PATH


class Hability:
    def __init__(self, name: str, description: str, domain: str):
        self.name = name
        self.description = description
        self.domain = domain

    def __eq__(self, other):
        if not isinstance(other, Hability):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    def populate() -> dict:
        populated_data = {}

        file = SEEDS_PATH / 'habilities.json'
        with open(file, 'r') as f:
            data = json.load(f)

            for domain, habilities_list in data.items():
                populated_data[domain] = []
                for hability_dict in habilities_list:
                    populated_data[domain].append(
                        Hability(
                            hability_dict['name'],
                            hability_dict['description'],
                            domain,
                        )
                    )
        return populated_data
