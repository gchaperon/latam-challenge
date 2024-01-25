# Documentation

## Install
Run `make install` on a fresh environment (possibly created by running `make venv` or however you like).

### Dev environment setup
Setup `pre-commit` hooks to have certainty that your code will pass CI checks. With the project installed run
```console
$ pre-commit install
```

## Conventions

### Code
Most (if not all) code conventions should be handled by the lint and formatting
rules enforced by `pre-commit`. Make sure yo have installed and configured,
see [here](dev-environment-setup).

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
