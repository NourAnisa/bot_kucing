#!/usr/bin/env bash
cd "$(dirname "$0")"
if [ -x .venv/bin/python ]; then exec .venv/bin/python nekocat.py; fi
exec python3 nekocat.py
