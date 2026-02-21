from fastapi import FastAPI

app = FastAPI(title="Service A")


@app.get("/health")
def health() -> dict:
    return {"service": "service-a", "status": "ok"}


@app.get("/data")
def data() -> dict:
    return {
        "service": "service-a",
        "domain": "usuarios",
        "data": [
            {"id": 1, "name": "Ana"},
            {"id": 2, "name": "Luis"},
        ],
    }

