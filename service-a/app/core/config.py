import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    service_name: str
    database_url: str


def load_settings() -> Settings:
    return Settings(
        service_name=os.getenv("SERVICE_NAME", "identity-service"),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql://identity_user:identity_pass@postgres:5432/db_identity",
        ),
    )
