from fastapi import FastAPI

app = FastAPI(title="Service c")


@app.get("/health")
def health() -> dict:
    return {"service": "service-c", "status": "ok"}


@app.get("/data")
def data() -> dict:
    return {
        "service": "service-c",
        "domain": "menu",
        "data": [
            {"id": 1, "comida": "arroz"},
            {"id": 2, "comida": "sopa"},
        ],
    }

