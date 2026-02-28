from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_identity_service
from app.schemas.identity_schema import (
    HealthResponse,
    UserCreateRequest,
    UserResponse,
    VehicleCreateRequest,
    VehicleResponse,
)
from app.services.errors import (
    ServiceConflictError,
    ServiceNotFoundError,
    ServiceUnavailableError,
)
from app.services.identity_service import IdentityService

router = APIRouter(tags=["identity"])


def _raise_http_error(exc: Exception) -> None:
    # Centralized translation keeps controller methods focused on HTTP contract only.
    if isinstance(exc, ServiceNotFoundError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, ServiceConflictError):
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if isinstance(exc, ServiceUnavailableError):
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    raise HTTPException(status_code=500, detail="Unexpected error") from exc


@router.get("/health", response_model=HealthResponse)
def health(service: IdentityService = Depends(get_identity_service)) -> dict:
    try:
        return service.health()
    except Exception as exc:  # noqa: BLE001
        _raise_http_error(exc)


@router.get("/users")
def list_users(service: IdentityService = Depends(get_identity_service)) -> dict:
    try:
        users = service.list_users()
        payload = [UserResponse.model_validate(user, from_attributes=True).model_dump() for user in users]
        return {"service": service.service_name, "count": len(payload), "users": payload}
    except Exception as exc:  # noqa: BLE001
        _raise_http_error(exc)


@router.post("/users", status_code=201)
def create_user(
    request: UserCreateRequest, service: IdentityService = Depends(get_identity_service)
) -> dict:
    try:
        user = service.create_user(name=request.name, email=str(request.email))
        payload = UserResponse.model_validate(user, from_attributes=True).model_dump()
        return {"service": service.service_name, "user": payload}
    except Exception as exc:  # noqa: BLE001
        _raise_http_error(exc)


@router.get("/vehicles")
def list_vehicles(service: IdentityService = Depends(get_identity_service)) -> dict:
    try:
        vehicles = service.list_vehicles()
        payload = [
            VehicleResponse.model_validate(vehicle, from_attributes=True).model_dump()
            for vehicle in vehicles
        ]
        return {"service": service.service_name, "count": len(payload), "vehicles": payload}
    except Exception as exc:  # noqa: BLE001
        _raise_http_error(exc)


@router.post("/vehicles", status_code=201)
def create_vehicle(
    request: VehicleCreateRequest, service: IdentityService = Depends(get_identity_service)
) -> dict:
    try:
        vehicle = service.create_vehicle(
            user_id=request.user_id,
            plate=request.plate,
            vehicle_type=request.vehicle_type,
        )
        payload = VehicleResponse.model_validate(vehicle, from_attributes=True).model_dump()
        return {"service": service.service_name, "vehicle": payload}
    except Exception as exc:  # noqa: BLE001
        _raise_http_error(exc)


@router.get("/data")
def data(service: IdentityService = Depends(get_identity_service)) -> dict:
    try:
        snapshot = service.snapshot()
        users = [
            UserResponse.model_validate(user, from_attributes=True).model_dump()
            for user in snapshot["data"]["users"]
        ]
        vehicles = [
            VehicleResponse.model_validate(vehicle, from_attributes=True).model_dump()
            for vehicle in snapshot["data"]["vehicles"]
        ]
        return {"service": snapshot["service"], "domain": snapshot["domain"], "data": {"users": users, "vehicles": vehicles}}
    except Exception as exc:  # noqa: BLE001
        _raise_http_error(exc)
