#!/usr/bin/env bash

DOMAIN_OWNER="774774188620"
DOMAIN="linius"
REGION="ap-southeast-2"
REPOSITORY="pypi-store"

aws codeartifact login \
    --tool twine \
    --domain $DOMAIN \
    --domain-owner $DOMAIN_OWNER \
    --repository $REPOSITORY \
    --region $REGION

rm -rf dist/
python -m pip install --upgrade build
python -m build

twine upload -r codeartifact dist/* --verbose