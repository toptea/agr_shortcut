"""
Run this script if called via the command line.
python -m shortcut --help
"""

import logging
import sys

from . import interface


def logging_setup():
    logging.getLogger()
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S')


logging_setup()
interface.main()
