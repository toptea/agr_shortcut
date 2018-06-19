"""
This modules contains full-fledged shortcut objects that can be
instantiated and then can be asked to provide information such the
file/folder location. They also have can even be used to open file/folder
directly.

See Also
--------
shortcut.base.GlobMatch
shortcut.base.Match
"""

import os
from .base import GlobMatch, ExactMatch
from .constant import PROGRAM_PATH, FOLDER_PATH


class Drawing(GlobMatch):
    """
    Using the part and project number, find/open the manufacture
    drawings in Dropbox. If the project number is not specified, the
    project number within the partcode string is used.

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
    >>> from shortcut.core import Drawing
    >>> pdf = Drawing('AGR1288-010-00')
    >>> pdf.find_file()
    >>> pdf.open_file()
    """

    def __init__(self, partcode, project='default'):
        self.program = str(PROGRAM_PATH['pdf_reader'])
        self.folder = str(FOLDER_PATH['pdf_drawings'])
        self.partcode = str(partcode)
        self.project = str(project)

    def _folder_expression(self):
        """return a glob expression used in the find_folder method"""
        if self.project == 'default':
            project = self.partcode[3:7]
        return os.path.join(self.folder, '*' + project + '*')

    def _file_expression(self, folder):
        """return a glob expression used in the find_file method"""
        return os.path.join(folder, self.partcode + '.pdf')


class Jobcard(GlobMatch):
    """
    Using the part and project number, find/open the manufacture job card
    in the 'project files' folder located in the Balmoral drive.
    If project number is not specified, the project number within
    the partcode string is used.

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
    >>> from shortcut.core import Jobcard
    >>> xls = Jobcard('AGR1288-010-00')
    >>> xls.find_file()
    >>> xls.open_file()
    """
    def __init__(self, partcode, project='default'):
        self.program = str(PROGRAM_PATH['excel'])
        self.folder = str(FOLDER_PATH['jobcard'])
        self.partcode = str(partcode)
        self.project = str(project)

    def _folder_expression(self):
        """return a glob expression used in the find_folder method"""
        if self.project == 'default':
            project = self.partcode[3:7]
        return os.path.join(r'Z:\*' + project + '*', 'Job Card*')

    def _file_expression(self, folder):
        """return a glob expression used in the find_file method"""
        return os.path.join(folder, '*' + self.partcode + '*.xls')


class PO(ExactMatch):
    """
    Using the purchase order number, find the corresponding pdf paperwork
    in 'Pegasus' folder located on the Balmoral drive

    Parameters
    ----------
    po : str
        AGR part number (eg. 61234)

    Raises
    ------
    NotADirectoryError
    FileNotFoundError

    Example
    -------
    >>> from shortcut.core import PO
    >>> pdf = PO(61234)
    >>> pdf.find_file()
    >>> pdf.open_file()
    """
    def __init__(self, number):
        self.program = str(PROGRAM_PATH['pdf_reader'])
        self.folder = str(FOLDER_PATH['purchase_order'])
        self.number = str(number)

    def _folder_expression(self):
        """return a glob expression used in the find_folder method"""
        return self.folder

    def _file_expression(self):
        """return a glob expression used in the find_file method"""
        return os.path.join(self.folder, 'PO_00' + self.number + '.PDF')


class Sticker(ExactMatch):
    """
    Open the manufacture drawing labels template in 'My Document'

    Raises
    ------
    NotADirectoryError
    FileNotFoundError

    Example
    -------
    >>> from shortcut.core import Sticker
    >>> xls = Sticker()
    >>> xls.find_file()
    >>> xls.open_file()
    """
    def __init__(self):
        """
        initialize path strings for MS Excel and main template folder
        store sticker template name
        """
        self.program = str(PROGRAM_PATH['excel'])
        self.folder = str(FOLDER_PATH['stickers'])
        self.file = 'drawing labels - normal 7x2.xls'

    def _folder_expression(self):
        """return a glob expression used in the find_folder method"""
        return self.folder

    def _file_expression(self):
        """return a glob expression used in the find_file method"""
        return os.path.join(self.folder, self.file)
