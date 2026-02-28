from fastapi import FastAPI

from app.controllers.identity_controller import router as identity_router
from app.core.dependencies import build_identity_service, get_settings



def create_application() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.service_name)

    @app.on_event("startup")
    def on_startup() -> None:
        # Startup keeps main clean: schema and seed are delegated to the service layer.
        build_identity_service().bootstrap()

    app.include_router(identity_router)
    return app


app = create_application()
