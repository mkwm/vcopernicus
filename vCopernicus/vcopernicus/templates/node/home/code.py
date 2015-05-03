#!/usr/bin/env python
import os
from serial import Serial

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SERIAL_PATH = os.path.join(BASE_DIR, 'dev', 'ttyS0')

serial = Serial(SERIAL_PATH, 38400)