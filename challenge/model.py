from __future__ import annotations

import datetime as dt
import typing as tp
import warnings

import pandas as pd
import sklearn.linear_model as linear_model


def _compute_delay(row: pd.Series[tp.Any], threshold_minutes: int = 15) -> int:
    """Compute delay for a data point.

    A flight is delayed if the difference between ``Fecha-I`` and ``Fecha-O``
    is greater than a configurable threshold.

    Args:
        row: A data point.
        threshold_minutes: A configurable threshold (in minutes) to determine a
            delay. Defaults to 15.

    Returns:
        int: 1 if delayed, 0 otherwise.
    """
    fecha_o = dt.datetime.strptime(row["Fecha-O"], "%Y-%m-%d %H:%M:%S")
    fecha_i = dt.datetime.strptime(row["Fecha-I"], "%Y-%m-%d %H:%M:%S")
    min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
    return int(min_diff > threshold_minutes)


class DelayModel:
    _model: linear_model.LogisticRegression
    _trained: bool
    _class_weight: dict[int, float] | None

    _TOP_10_FEATURES: tp.Final[list[str]] = [
        "OPERA_Latin American Wings",
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air",
    ]

    def __init__(self, model: linear_model.LogisticRegression | None = None) -> None:
        """Initialize DelayModel from checkpoint or from scratch.

        Args:
            model: A model checkpoint or None. If None, initialize with a model
                that requires fitting before being useful.
        """
        self._trained = model is not None
        self._model = model or linear_model.LogisticRegression()
        # NOTE: _class_weight will be set by de preprocess method if the model
        # hasn't been fitted
        self._class_weight = None

    @tp.overload
    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        ...

    @tp.overload
    def preprocess(
        self, data: pd.DataFrame, target_column: str
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        ...

    def preprocess(
        self, data: pd.DataFrame, target_column: str | None = None
    ) -> tuple[pd.DataFrame, pd.DataFrame] | pd.DataFrame:
        """Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        data["delay"] = data.apply(_compute_delay, axis="columns")
        features = pd.concat(
            [
                pd.get_dummies(data["OPERA"], prefix="OPERA"),
                pd.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
                pd.get_dummies(data["MES"], prefix="MES"),
            ],
            axis=1,
        )

        X = features[self._TOP_10_FEATURES]
        if target_column:
            y = data[target_column]
            if not self._trained:
                n_y0 = len(y[y == 0])
                n_y1 = len(y[y == 1])

                self._class_weight = {1: n_y0 / len(y), 0: n_y1 / len(y)}
            return X, pd.DataFrame({y.name: y})
        else:
            return X

    def fit(self, features: pd.DataFrame, target: pd.Series[tp.Any]) -> None:
        """Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        if self._trained:
            warnings.warn(
                "You are calling fit on an already fitted model. "
                "This might not be what you want"
            )
        assert (
            self._class_weight is not None
        ), "Model shouldn't be trained with unbalanced classes"
        self._model.set_params(class_weight=self._class_weight)
        self._model.fit(features, target)
        self._trained = True

    def predict(self, features: pd.DataFrame) -> list[int]:
        """Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        if not self._trained:
            warnings.warn(
                "You are calling predict on a non-fitted model. "
                "This might not be what you want"
            )
        return list(self._model.predict(features))
