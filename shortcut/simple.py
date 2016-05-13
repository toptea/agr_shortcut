"""
This module contains useful shortcut functions for the end user.
Most of the function are wrappers around the core shortcut objects.
Every function in this module are imported to the package namespace for
convenience (eg. shortcut.sticker and shortcut.simple.stickers works!)

See Also
--------
shortcut.core.Drawing
shortcut.core.Jobcard
shortcut.core.PO
shortcut.core.Sticker
"""

from subprocess import Popen
from .core import Sticker, PO, Jobcard, Drawing
from .constant import PROGRAM_PATH


def drawing(partcode, project='default'):
    """open drawing and if its not possible, open folder

    Parameters
    ----------
    partcode : str
        AGR part number (eg. 'AGR1288-010-00')
    project : Optional[str]
        AGR project number (eg. 'AGR1288')

    Raises
    ------
    NotADirectoryError
    FileNotFoundError

    Example
    -------
    >>> import shortcut
    >>> drawing('AGR1288-010-00')
    """
    dw = Drawing(partcode, project)
    dw.open()


def jobcard(partcode, project='default'):
    """open jobcard and if its not possible, open folder

    Parameters
    ----------
    partcode : str
        AGR part number (eg. 'AGR1288-010-00')
    project : Optional[str]
        AGR project number (eg. 'AGR1288')

    Raises
    ------
    NotADirectoryError
    FileNotFoundError

    Example
    -------
    >>> import shortcut
    >>> jobcard('AGR1288-010-00')
    """
    jc = Jobcard(partcode, project)
    jc.open()


def po(number):
    """open purchase order and if its not possible, open folder

    Parameters
    ----------
    number : str
         AGR part number (eg. 61234)

    Raises
    ------
    NotADirectoryError
    FileNotFoundError

    Example
    -------
    >>> import shortcut
    >>> po(61234)
    """
    po = PO(number)
    po.open()


def sticker():
    """open label template and if its not possible, open folder

    Raises
    ------
    NotADirectoryError
    FileNotFoundError

    Example
    -------
    >>> import shortcut
    >>> shortcut.sticker()
    """
    sk = Sticker()
    sk.open()



def run(program):
    Popen(PROGRAM_PATH[program])
