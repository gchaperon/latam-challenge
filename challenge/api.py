from __future__ import annotations

import functools
import typing as tp

import fastapi
import pandas as pd
import pydantic
import starlette.status as status

from challenge.model import DelayModel

if tp.TYPE_CHECKING:
    import starlette.requests
    import starlette.responses


app = fastapi.FastAPI()


class HealthReturn(pydantic.BaseModel):
    status: tp.Literal["OK"]


class PayloadItem(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        alias_generator=str.upper,
        json_schema_extra={
            "examples": [{"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3}]
        },
    )

    # NOTE: I'm not too proud of this, but I am in a hurry
    opera: tp.Literal[
        "American Airlines",
        "Air Canada",
        "Air France",
        "Aeromexico",
        "Aerolineas Argentinas",
        "Austral",
        "Avianca",
        "Alitalia",
        "British Airways",
        "Copa Air",
        "Delta Air",
        "Gol Trans",
        "Iberia",
        "K.L.M.",
        "Qantas Airways",
        "United Airlines",
        "Grupo LATAM",
        "Sky Airline",
        "Latin American Wings",
        "Plus Ultra Lineas Aereas",
        "JetSmart SPA",
        "Oceanair Linhas Aereas",
        "Lacsa",
    ]
    tipovuelo: tp.Literal["I", "N"]
    mes: int = pydantic.Field(gt=1, le=12)


class PredictionPayload(pydantic.BaseModel):
    flights: list[PayloadItem]


class PredictionResponse(pydantic.BaseModel):
    predict: list[int]


@app.get("/health", status_code=200)
async def get_health() -> HealthReturn:
    """Simple health enpoint."""
    return HealthReturn(status="OK")


@app.post("/predict", status_code=200)
async def post_predict(payload: PredictionPayload) -> PredictionResponse:
    """Prediction endpoint.

    Receives a prediction payload in the format defined by
    ``PredictionPayload``, converts to features each item in the body and
    passes it trough ``DelayModel.predict``. Return the predictions as a list.
    """
    model = _lazy_model()
    features = model.preprocess(
        pd.DataFrame([item.model_dump(by_alias=True) for item in payload.flights])
    )
    prediction = model.predict(features)
    return PredictionResponse(predict=prediction)


@app.exception_handler(fastapi.exceptions.RequestValidationError)
async def validation_exception_handler(
    request: starlette.requests.Request,
    exc: fastapi.exceptions.RequestValidationError,
) -> starlette.responses.JSONResponse:
    """Validation exception handler sets status code to 400.

    The default validation exception handler uses the 422 code, but for this
    assignment the tests expect a 400 error.

    Args:
        request: The request tha triggered this error.
        exc: The exception produced.

    Returns:
        starlette.response.JSONResponse: The 400 response.
    """
    response = await fastapi.exception_handlers.request_validation_exception_handler(
        request, exc
    )
    response.status_code = status.HTTP_400_BAD_REQUEST
    return response


@functools.lru_cache
def _lazy_model() -> DelayModel:
    """Lazy model getter.

    This allows for a fast app startup, by deferring model loading to the first
    request received. Since the model is cached via ``functools.lru_cache``,
    subsequent calls to this functions simply return the model previously
    created.

    The idea is to make importing project components snappier, and avoid
    running expensive code at module initialization time.
    """
    return DelayModel()


def custom_openapi() -> dict[str, tp.Any]:
    """Comfigure a custom OpenAPI schema.

    This function changes the response code 422 for a response code 400, to
    match the ValidationError configured for this app.

    Returns:
        dict[str, tp.Any]: The altered OpenAPI schema.
    """
    openapi_schema = fastapi.openapi.utils.get_openapi(
        title="Latam Challenge",
        version="0.0.1",
        summary="Predict delays given flight data.",
        routes=app.routes,
    )
    responses = openapi_schema["paths"]["/predict"]["post"]["responses"]
    responses["400"] = responses["422"]
    del responses["422"]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# NOTE: on ignore[method-assign];  asigning methods _is_ possible, but frawned
# upon. Mypy catches the code smell, but I am allowing it here because it's the
# recommended way of customizing the OpenAPI documentation. See
# [here](https://fastapi.tiangolo.com/how-to/extending-openapi/) for more
# details.
app.openapi = custom_openapi  # type: ignore[method-assign]
