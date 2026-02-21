from fastapi import FastAPI

app = FastAPI(title="Service B")


@app.get("/health")
def health() -> dict:
    return {"service": "service-b", "status": "ok"}


@app.get("/data")
def data() -> dict:
    return {
        "service": "service-b",
        "domain": "ordenes",
        "data": [
            {"id": 101, "total": 120.5},
            {"id": 102, "total": 89.9},
        ],
    }

