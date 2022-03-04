#!/usr/bin/env bash

DOMAIN_OWNER="774774188620"
DOMAIN="linius"
REGION="ap-southeast-2"
REPO="pypi-store"

# If you require use of a named profile, run this script like:
# AWS_PROFILE=prod ./pypi_auth.sh

AUTH_TOKEN=$(
    aws codeartifact \
    get-authorization-token \
    --domain-owner "$DOMAIN_OWNER" \
    --domain "$DOMAIN" \
    --profile "$PROFILE" \
    --region "$REGION" \
    --query authorizationToken \
    --output text
)

export PIP_EXTRA_INDEX_URL="https://aws:$AUTH_TOKEN@$DOMAIN-$DOMAIN_OWNER.d.codeartifact.$REGION.amazonaws.com/pypi/$REPO/simple"
echo "$PIP_EXTRA_INDEX_URL"