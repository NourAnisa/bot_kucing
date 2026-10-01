# -*- coding: utf-8 -*-
"""Definisi 35 Agen AI & Divisi untuk SondeR AI Office."""

import os
import json

_DIR = os.path.dirname(os.path.abspath(__file__))
_JSON_PATH = os.path.join(_DIR, "agents_data.json")

with open(_JSON_PATH, "r", encoding="utf-8") as _f:
    _DATA = json.load(_f)

AGENTS = _DATA.get("agents", [])
DEFAULT_DATASET = _DATA.get("dataset", {})
SAMPLE_DOC = _DATA.get("sample_doc", {})
