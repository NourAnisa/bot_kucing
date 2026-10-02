# -*- coding: utf-8 -*-
"""Backward compatibility launcher redirecting to nekocat.py"""
import os
import sys
import runpy

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "nekocat.py")
    if os.path.exists(target):
        runpy.run_path(target, run_name="__main__")
    else:
        runpy.run_module("nekocat", run_name="__main__")
