import pathlib
import pickle
import sys

import click
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from challenge.model import DelayModel


@click.group(context_settings={"show_default": True})
def cli() -> None:
    """Top level command line group."""
    pass


@cli.command()
@click.option(
    "--data-file",
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
    required=True,
)
def train(data_file: pathlib.Path) -> None:
    """Command to train the model using a data source.

    The command trains the model and saves a checkpoint to the ``checkpoints``
    directory.

    Args:
        data_file: The data file with features for training.
    """
    # Load stuff
    data = pd.read_csv(data_file, low_memory=False)
    model = DelayModel(for_training=True)

    # Split data
    features, target = model.preprocess(data=data, target_column="delay")
    _, features_validation, _, target_validation = train_test_split(
        features, target, test_size=0.33, random_state=42
    )
    # Fit and predict
    model.fit(features, target)
    predicted_target = model.predict(features_validation)

    # Log metrics and save model
    print(classification_report(target_validation, predicted_target), file=sys.stderr)
    model.DEFAULT_CHECKPOINT.parent.mkdir(exist_ok=True)
    with open(model.DEFAULT_CHECKPOINT, "wb") as checkpoint_file:
        pickle.dump(model, checkpoint_file)
    print("Trained model saved to", str(model.DEFAULT_CHECKPOINT), file=sys.stderr)
