import argparse
import hashlib
import json
import pprint
import shlex
import subprocess
import sys


def image_tag() -> None:
    """Compute a hash for the Docker image."""
    m = hashlib.md5()
    paths = subprocess.run(
        shlex.split("git ls-files challenge checkpoints"),
        capture_output=True,
        text=True,
    ).stdout.split()
    paths = ["pyproject.toml", "requirements.txt", "Dockerfile", *paths]
    print("Hashing files", file=sys.stderr)
    pprint.pp(paths, stream=sys.stderr)
    for path in paths:
        with open(path, "rb") as file:
            m.update(file.read())
    print(m.hexdigest()[:16])


def is_tag_available(tag: str, location: str, repository: str, package: str) -> None:
    """Find if the given tag is available in Google Artifacts Registry.

    This command exits succesfully if the tag is available, and return an error
    code 1 if the tag is already taken.

    Args:
        tag: The tag to search.
        location: The GCP zone of the repository.
        repository: The name of the Goocle Artifacts Registry repository.
        package: The name of the package inside the repository.
    """
    resources = json.loads(
        subprocess.run(
            [
                "gcloud",
                "artifacts",
                "tags",
                "list",
                "--location",
                location,
                "--repository",
                repository,
                "--package",
                package,
                "--filter",
                tag,
                "--format=json",
            ],
            capture_output=True,
            text=True,
        ).stdout
    )
    if resources:
        print("Following resources match:")
        pprint.pp(resources, stream=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(required=True)

    parser_image_tag = subparsers.add_parser("image_tag")
    parser_image_tag.set_defaults(func=image_tag)

    parser_is_tag_available = subparsers.add_parser("is_tag_available")
    parser_is_tag_available.add_argument("tag")
    parser_is_tag_available.add_argument("--location", required=True)
    parser_is_tag_available.add_argument("--repository", required=True)
    parser_is_tag_available.add_argument("--package", required=True)
    parser_is_tag_available.set_defaults(func=is_tag_available)

    args = parser.parse_args()
    args.func(**{k: v for k, v in vars(args).items() if k != "func"})
