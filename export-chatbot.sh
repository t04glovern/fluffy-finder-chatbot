#!/bin/bash

## Install pip requirements
cd "$(dirname "$0")"
ACTIVATE_PATH=venv/bin/activate
source ${ACTIVATE_PATH}
pip install -r requirements.txt

## Export chatbot config as bot-definition-export.json
cd lex
python utils/lex-manager.py -e FluffyFinder