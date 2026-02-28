from typing import Callable

import psycopg

from app.models.identity import User, Vehicle
from app.repositories.identity_repository import (
    IdentityRepository,
    RepositoryConflictError,
    RepositoryError,
    RepositoryUnavailableError,
)

ConnectionFactory = Callable[[], psycopg.Connection]


class PostgresIdentityRepository(IdentityRepository):
    def __init__(self, connection_factory: ConnectionFactory) -> None:
        self.connection_factory = connection_factory

    def ping(self) -> None:
        try:
            with self.connection_factory() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
                    cur.fetchone()
        except (psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise RepositoryUnavailableError(f"Database unavailable: {exc}") from exc
        except psycopg.Error as exc:
            raise RepositoryError(f"Database error: {exc}") from exc

    def initialize_schema(self) -> None:
        try:
            with self.connection_factory() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            name TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                        );
                        """
                    )
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS vehicles (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                            plate TEXT UNIQUE NOT NULL,
                            vehicle_type TEXT NOT NULL,
                            active BOOLEAN NOT NULL DEFAULT TRUE,
                            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                        );
                        """
                    )
                    conn.commit()
        except (psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise RepositoryUnavailableError(f"Database unavailable: {exc}") from exc
        except psycopg.Error as exc:
            raise RepositoryError(f"Database error: {exc}") from exc

    def has_any_user(self) -> bool:
        try:
            with self.connection_factory() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) AS total FROM users;")
                    return cur.fetchone()["total"] > 0
        except (psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise RepositoryUnavailableError(f"Database unavailable: {exc}") from exc
        except psycopg.Error as exc:
            raise RepositoryError(f"Database error: {exc}") from exc

    def get_user_by_id(self, user_id: int) -> User | None:
        try:
            with self.connection_factory() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, name, email, created_at
                        FROM users
                        WHERE id = %s;
                        """,
                        (user_id,),
                    )
                    row = cur.fetchone()
                    return self._map_user(row) if row else None
        except (psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise RepositoryUnavailableError(f"Database unavailable: {exc}") from exc
        except psycopg.Error as exc:
            raise RepositoryError(f"Database error: {exc}") from exc

    def list_users(self) -> list[User]:
        try:
            with self.connection_factory() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, name, email, created_at
                        FROM users
                        ORDER BY id;
                        """
                    )
                    rows = cur.fetchall()
                    return [self._map_user(row) for row in rows]
        except (psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise RepositoryUnavailableError(f"Database unavailable: {exc}") from exc
        except psycopg.Error as exc:
            raise RepositoryError(f"Database error: {exc}") from exc

    def create_user(self, name: str, email: str) -> User:
        try:
            with self.connection_factory() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO users (name, email)
                        VALUES (%s, %s)
                        RETURNING id, name, email, created_at;
                        """,
                        (name, email),
                    )
                    row = cur.fetchone()
                    conn.commit()
                    return self._map_user(row)
        except psycopg.errors.UniqueViolation as exc:
            raise RepositoryConflictError("Email already registered") from exc
        except (psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise RepositoryUnavailableError(f"Database unavailable: {exc}") from exc
        except psycopg.Error as exc:
            raise RepositoryError(f"Database error: {exc}") from exc

    def list_vehicles(self) -> list[Vehicle]:
        try:
            with self.connection_factory() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, user_id, plate, vehicle_type, active, created_at
                        FROM vehicles
                        ORDER BY id;
                        """
                    )
                    rows = cur.fetchall()
                    return [self._map_vehicle(row) for row in rows]
        except (psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise RepositoryUnavailableError(f"Database unavailable: {exc}") from exc
        except psycopg.Error as exc:
            raise RepositoryError(f"Database error: {exc}") from exc

    def create_vehicle(self, user_id: int, plate: str, vehicle_type: str) -> Vehicle:
        try:
            with self.connection_factory() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO vehicles (user_id, plate, vehicle_type)
                        VALUES (%s, %s, %s)
                        RETURNING id, user_id, plate, vehicle_type, active, created_at;
                        """,
                        (user_id, plate, vehicle_type),
                    )
                    row = cur.fetchone()
                    conn.commit()
                    return self._map_vehicle(row)
        except psycopg.errors.UniqueViolation as exc:
            raise RepositoryConflictError("Plate already registered") from exc
        except (psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise RepositoryUnavailableError(f"Database unavailable: {exc}") from exc
        except psycopg.Error as exc:
            raise RepositoryError(f"Database error: {exc}") from exc

    @staticmethod
    def _map_user(row: dict) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            created_at=row["created_at"],
        )

    @staticmethod
    def _map_vehicle(row: dict) -> Vehicle:
        return Vehicle(
            id=row["id"],
            user_id=row["user_id"],
            plate=row["plate"],
            vehicle_type=row["vehicle_type"],
            active=row["active"],
            created_at=row["created_at"],
        )
