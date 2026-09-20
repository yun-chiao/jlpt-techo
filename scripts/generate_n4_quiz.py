# -*- coding: utf-8 -*-
"""
Main entry point for generating N4 Quiz data.
Delegates to scripts/n4_generator/build_all.py
"""
import sys
from pathlib import Path

# Add n4_generator to sys.path
sys.path.insert(0, str(Path(__file__).parent / "n4_generator"))

import build_all

if __name__ == "__main__":
    build_all.main()
