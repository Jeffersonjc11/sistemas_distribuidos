import os

import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Gateway")

SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://service-a:8001")
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://service-b:8002")
SERVICE_C_URL = os.getenv("SERVICE_C_URL", "http://service-c:8003")
TIMEOUT_SECONDS = 5.0


async def _call_service(base_url: str, path: str) -> dict:
    url = f"{base_url}{path}"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Gateway error calling {url}: {exc}") from exc


@app.get("/")
async def root() -> dict:
    return {
        "message": "Gateway activo",
        "routes": ["/health", "/api/service-a", "/api/service-b" , "/api/service-c"],
    }


@app.get("/health")
async def health() -> dict:
    services = {}

    for name, url in (("service-a", SERVICE_A_URL), ("service-b", SERVICE_B_URL), ("service-c", SERVICE_C_URL)):
        try:
            services[name] = await _call_service(url, "/health")
        except HTTPException as exc:
            services[name] = {"status": "unreachable", "error": exc.detail}

    return {"gateway": "ok", "services": services}


@app.get("/api/service-a")
async def service_a_proxy() -> dict:
    return await _call_service(SERVICE_A_URL, "/data")


@app.get("/api/service-b")
async def service_b_proxy() -> dict:
    return await _call_service(SERVICE_B_URL, "/data")

@app.get("/api/service-c")
async def service_c_proxy() -> dict:
    return await _call_service(SERVICE_C_URL, "/data")

