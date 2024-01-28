# Documentation

## Install
Run `make install` on a fresh environment (possibly created by running `make
venv` or however you like).

### Dev environment setup
Setup `pre-commit` hooks to have certainty that your code will pass CI checks.
With the project installed run
```console
$ pre-commit install
```

Setup `terraform`. Run
```console
$ terraform -chdir=infra init
```
Validate the intialization by running `terraform -chdir=infra output app_uri`.
It should show the URI of the deployed app.

### Testing
Model and API tests are run with the following
```console
$ make model-test
$ make api-test
```

The API can be run locally with
```console
$ uvicorn challenge:app --reload
```

## Model migration
### Selection rationale
I choose the `LogisticRegression` model (with most important features and class
balance), because I belive in the [Occam's
razor](https://en.wikipedia.org/wiki/Occam%27s_razor) principle (a fancy way of
saying simpler is better).

### Training CLI
I have build a simple CLI to train a new model and store in the `checkpoints`
directory. This should help when new models need to be trained in a
standardized pipeline, and also when loading checkpoints for inference.

The CLI can be invoked with running `python -m challenge train <options>`, with
the package properly installed (see [Install](install).

Here is the synopsis for the command.
```console
$ python -m challenge train --help
Usage: python -m challenge train [OPTIONS]

  Command to train the model using a data source.

  The command trains the model and saves a checkpoint to the ``checkpoints``
  directory.

  Args:     data_file: The data file with features for training.

Options:
  --data-file FILE  [required]
  --help            Show this message and exit.
```

## Deployment
### Manual Instructions
Requieres a functional `gcloud` and `docker` installation.

1. Set up the infraestructure to hold the Docker images. Run `terraform
   -chdir=infra apply`.
2. Configure Docker to use the Artifacts Registry. Run `gcloud auth
   configure-docker $(terraform -chdir=infra output -raw
   docker_repository_location)-docker.pkg.dev`
3. Create image and push. Run
   ```console
   $ FULL_TAG=$(terraform -chdir=infra output -raw docker_tag_base):$(python scripts/deploy_utils.py image_tag)
   $ docker build -t $FULL_TAG .
   $ docker push $FULL_TAG
   ```
4. Deploy using Terraform. Run `terraform -chdir=infra apply
   -var="docker_tag=$TAG"`.

The deployed URI can be checked using `terraform -chdir=infra output app_uri`.
Ping it [here](https://latam-challenge-ubomd35csa-uc.a.run.app/) or check the
API docs [here](https://latam-challenge-ubomd35csa-uc.a.run.app/docs/)

### Continuous Deployment description
The cotinuous deployment configuration has two jobs: `build` and `deploy`. In
the `build` job steps 1 through 3 are run, while in the `deploy` job step 4 is
applied.

CD is configured so that if an attempt is made to rebuild an existing image in
the artifacts repository, the build process will detect this and stop, as to
not waste resources. In case of an skipped build process, the `deploy` job will
be executed anyways, so that changes to the infrastructure not related to the
image deployment are applied.

If Terraform is asked to "redeploy" the current image, no expensive operation
will be performed because the configuration will match the state exactly.


## Conventions

### Code
Most (if not all) code conventions should be handled by the lint and formatting
rules provided by `ruff` and enforced by `pre-commit`. Make sure yo have
installed and configured, see [here](dev-environment-setup).

### PR naming convention
All pull request will have a title in the form `[(Part X|Base)] <short
description>`, to document which part of the challenge the PR is addressing.
The `Base` tag refers to general requirements in the challenge, most notably
documentation.

It is possible that a single pull request modifies code related to different
parts of the challenge, in which case there I will use a comma separated list
between squeare brackets.

**Examples**: `[Part IV] Configure CI`, `[Part II, Part
III] Update API and deployment method`, `[Base] Document API`
