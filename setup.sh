#!/bin/bash

env="$1"

if [ "${env}" != "dev" -a "${env}" != "prod" ]; then
    echo "usage: setup.sh [env]"
    echo "  env: Use 'dev' or 'prod'"
    exit 1
fi

python3.9 -m venv .venv
echo "Created virtual environment"

source .venv/bin/activate
pip3.9 install -r "requirements/${env}.txt"
echo "Installed dependencies"

cp .env.default .env
echo "Created .env file"
