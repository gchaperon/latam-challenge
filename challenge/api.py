import typing as tp
import fastapi

app = fastapi.FastAPI()


class _HealthReturn(tp.TypedDict):
    status: tp.Literal["OK"]


@app.get("/health", status_code=200)
async def get_health() -> _HealthReturn:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict() -> None:
    raise NotImplementedError
