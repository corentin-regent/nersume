#!/bin/bash

set -e

VENV=.venv
if [ ! -d "$VENV" ]; then
    python -m venv "$VENV"
fi
source "$VENV/bin/activate"
python -m pip install -r requirements.txt
