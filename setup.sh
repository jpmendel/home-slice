#!/bin/bash

env="$1"

if [ "${env}" != "dev" -a "${env}" != "prod" ]; then
    echo "usage: setup.sh [env]"
    echo "  env: Use 'dev' or 'prod'"
    exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
pip install -r "requirements/${env}.txt"
