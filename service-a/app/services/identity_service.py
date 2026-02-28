from app.models.identity import User, Vehicle
from app.repositories.identity_repository import (
    IdentityRepository,
    RepositoryConflictError,
    RepositoryError,
    RepositoryUnavailableError,
)
from app.services.errors import (
    ServiceConflictError,
    ServiceNotFoundError,
    ServiceUnavailableError,
)


class IdentityService:
    def __init__(self, repository: IdentityRepository, service_name: str) -> None:
        self.repository = repository
        self.service_name = service_name

    def bootstrap(self) -> None:
        try:
            self.repository.initialize_schema()
            if self.repository.has_any_user():
                return

            ana = self.create_user("Ana", "ana@example.com")
            luis = self.create_user("Luis", "luis@example.com")
            self.create_vehicle(ana.id, "ABC123", "car")
            self.create_vehicle(luis.id, "XYZ987", "motorcycle")
        except RepositoryUnavailableError as exc:
            raise ServiceUnavailableError(str(exc)) from exc
        except RepositoryError as exc:
            raise ServiceUnavailableError(str(exc)) from exc

    def health(self) -> dict:
        try:
            self.repository.ping()
            return {"service": self.service_name, "status": "ok", "database": "ok"}
        except RepositoryUnavailableError as exc:
            raise ServiceUnavailableError(str(exc)) from exc
        except RepositoryError as exc:
            raise ServiceUnavailableError(str(exc)) from exc

    def list_users(self) -> list[User]:
        try:
            return self.repository.list_users()
        except RepositoryUnavailableError as exc:
            raise ServiceUnavailableError(str(exc)) from exc
        except RepositoryError as exc:
            raise ServiceUnavailableError(str(exc)) from exc

    def create_user(self, name: str, email: str) -> User:
        normalized_name = name.strip()
        normalized_email = email.strip().lower()

        try:
            return self.repository.create_user(normalized_name, normalized_email)
        except RepositoryConflictError as exc:
            raise ServiceConflictError(str(exc)) from exc
        except RepositoryUnavailableError as exc:
            raise ServiceUnavailableError(str(exc)) from exc
        except RepositoryError as exc:
            raise ServiceUnavailableError(str(exc)) from exc

    def list_vehicles(self) -> list[Vehicle]:
        try:
            return self.repository.list_vehicles()
        except RepositoryUnavailableError as exc:
            raise ServiceUnavailableError(str(exc)) from exc
        except RepositoryError as exc:
            raise ServiceUnavailableError(str(exc)) from exc

    def create_vehicle(self, user_id: int, plate: str, vehicle_type: str) -> Vehicle:
        # Business rule: vehicle cannot exist without a valid owner.
        try:
            user = self.repository.get_user_by_id(user_id)
            if user is None:
                raise ServiceNotFoundError("User not found")

            normalized_plate = plate.strip().upper()
            normalized_type = vehicle_type.strip().lower()

            return self.repository.create_vehicle(user_id, normalized_plate, normalized_type)
        except RepositoryConflictError as exc:
            raise ServiceConflictError(str(exc)) from exc
        except RepositoryUnavailableError as exc:
            raise ServiceUnavailableError(str(exc)) from exc
        except RepositoryError as exc:
            raise ServiceUnavailableError(str(exc)) from exc

    def snapshot(self) -> dict:
        users = self.list_users()
        vehicles = self.list_vehicles()
        return {
            "service": self.service_name,
            "domain": "identity",
            "data": {"users": users, "vehicles": vehicles},
        }
