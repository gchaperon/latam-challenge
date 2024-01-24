import typing as tp
import pandas as pd


class Classifier(tp.Protocol):
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        ...


class DelayModel:
    _model: Classifier

    def __init__(self) -> None:
        raise NotImplementedError

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
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        raise NotImplementedError

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        raise NotImplementedError

    def predict(self, features: pd.DataFrame) -> list[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        raise NotImplementedError
