#!/usr/bin/env python3

docstring=''' A basic example reading from influxdb in this case show all databases'''



import hug
import logging


FORMAT = 'write-influx-example log %(levelname)s: %(message)s'
logging.basicConfig(level=0, format=FORMAT)
logging.info(docstring)