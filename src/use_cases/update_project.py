from src.models import Project
from src.repositories import ProjectRepository


class UpdateProjectUseCase:
    """
    Caso de uso para atualizar um projeto existente, incluindo suas
    habilidades associadas.
    """

    def __init__(self, project_repository: ProjectRepository):
        self._project_repository = project_repository

    def execute(self, id: int, **kwargs) -> Project | None:
        if id is None:
            return None

        project = self._project_repository.get_by_id_with_habilities(id)
        if not project:
            return None

        project.update(**kwargs)

        self._project_repository.save(project)

        return project

    @staticmethod
    def factory():
        return UpdateProjectUseCase(ProjectRepository())
