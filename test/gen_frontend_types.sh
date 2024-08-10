#!/bin/bash

pushd ..
PYTHONPATH=. ./venv/bin/python ./scripts/gen_frontend_types.py starter_app test/frontend
popd
