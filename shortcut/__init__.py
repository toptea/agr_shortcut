"""

The modules inside of this package are orgainize in the following way:

constant
    Contains global constants of various programs and folders paths.
    They are organize in dictionaries; PROGRAM_PATH & FOLDER_PATH.
    The constants are used to initialize shortcut objects in core file.

base
    Define the base class for shortcut objects in core.py file.
    Abstract class are used so that every child class have the same and
    consistent names. Inheritance were use to follow the DRY principle.
    See UML diagram for the class structure.

core
    This modules contains full-fledged shortcut objects that can be
    instantiated and then asked to provide all sorts of information and
    functionalities.
    Properties such as the file or folder location,
    and they can even open these file or folder automaticaly.
    For useability and convenience, 'Drawing','Jobcard', 'PO' and 'Sticker'
    objects are imported to the package namespace.
    (eg can call via shortcut.Drawing)

interface
    Useful command line inferface for the shortcut methods. Can not be
    imported by the module. TODO

"""

__title__ = 'shortcut'
__version__ = '1.0'
__author__ = 'Gary Ip'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Gary Ip'


__all__ = ['constant', 'base', 'core']
from .core import Drawing, Jobcard, PO, Sticker
