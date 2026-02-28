from functools import lru_cache
from typing import Callable

import psycopg
from psycopg.rows import dict_row

from app.core.config import Settings, load_settings
from app.repositories.postgres_identity_repository import PostgresIdentityRepository
from app.services.identity_service import IdentityService

ConnectionFactory = Callable[[], psycopg.Connection]


@lru_cache
def get_settings() -> Settings:
    return load_settings()


def get_connection_factory() -> ConnectionFactory:
    database_url = get_settings().database_url

    def factory() -> psycopg.Connection:
        return psycopg.connect(database_url, row_factory=dict_row)

    return factory


def build_identity_service() -> IdentityService:
    repository = PostgresIdentityRepository(connection_factory=get_connection_factory())
    settings = get_settings()
    return IdentityService(repository=repository, service_name=settings.service_name)


def get_identity_service() -> IdentityService:
    return build_identity_service()
