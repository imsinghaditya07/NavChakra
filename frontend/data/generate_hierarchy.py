#!/usr/bin/env python3
"""
Generate comprehensive all-India Administrative Hierarchy JSON
for AryaSaarthi Multi-mode search cascading dropdowns.
Contains all 28 States + 8 Union Territories = 36 States & UTs,
all 786 official Districts, Blocks/Tehsils, and Gram Panchayats (GPs).
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from build_complete_india_hierarchy import main

if __name__ == "__main__":
    main()
