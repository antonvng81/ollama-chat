#!/bin/bash
# Ejecutar el chat

set -x

source "secret/SECRET_KEY"
source "venv/bin/activate"
flet run --web main.py


