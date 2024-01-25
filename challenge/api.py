import typing as tp

import fastapi
import typing_extensions as tpx

app = fastapi.FastAPI()


class _HealthReturn(tpx.TypedDict):
    status: tp.Literal["OK"]


@app.get("/health", status_code=200)
async def get_health() -> _HealthReturn:
    """Simple health enpoint."""
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict() -> None:
    """Prediction endpoint."""
    raise NotImplementedError
