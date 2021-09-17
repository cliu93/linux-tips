#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Chi Liu 
# Created Date: 17/09/2021
# Email: lichee93@gmail.com
# version ='1.0'
# ---------------------------------------------------------------------------
""" This script is used to check Windows Server physical memory usage.
    Usage: python check_memory.py warning_threshold critical_threshold
    e.g.: python check_memory.py 75 85
"""  
# ---------------------------------------------------------------------------
# Futures
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Generic/Built-in
import psutil
import sys
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

if len(sys.argv) != 3:
    raise Exception("Input invalid, usage: check_memory.py argv1 argv2")

memory = psutil.virtual_memory()

if memory[2] >= float(sys.argv[1]) and memory[2] <= float(sys.argv[2]):
    info = '''Warning, the currernt memory usage is up to %.2f''' %(float(memory[2])) + "%."
    print(info)
    sys.exit(1)
elif memory[2] > float(sys.argv[1]):
    info = '''Critical, the currernt memory usage is up to %.2f''' %(float(memory[2])) + "%."
    print(info)
    sys.exit(2)
elif memory[2] >= 0 and memory[2] < float(sys.argv[1]):
    info = '''OK, the currernt memory usage is up to %.2f''' %(float(memory[2])) + "%."
    print(info)
    sys.exit(0)
else:
    print("UNKNOWN")
    sys.exit(3)