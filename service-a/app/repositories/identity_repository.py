from typing import Protocol

from app.models.identity import User, Vehicle


class RepositoryError(Exception):
    pass


class RepositoryConflictError(RepositoryError):
    pass


class RepositoryUnavailableError(RepositoryError):
    pass


class IdentityRepository(Protocol):
    def ping(self) -> None:
        ...

    def initialize_schema(self) -> None:
        ...

    def has_any_user(self) -> bool:
        ...

    def get_user_by_id(self, user_id: int) -> User | None:
        ...

    def list_users(self) -> list[User]:
        ...

    def create_user(self, name: str, email: str) -> User:
        ...

    def list_vehicles(self) -> list[Vehicle]:
        ...

    def create_vehicle(self, user_id: int, plate: str, vehicle_type: str) -> Vehicle:
        ...
