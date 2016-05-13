
import os
from subprocess import call
from .base import GlobMatch, ExactMatch
from .constant import PROGRAM_PATH, FOLDER_PATH


class Drawing(GlobMatch):
    """
    Using the [partcode] and [project] number, find the manufacture pdf
    drawings in Dropbox.If project number is not specified, use the
    original project number in the partcode.
    """
    def __init__(self, partcode, project='default'):
        """
        initialize path strings for adobe reader and main drawing folder
        store partcode and project parameters
        """
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
    Using the [partcode] and [project] number, find the manufacture
    job card in the 'project files' folder located on the Balmoral drive.
    If project number is not specified, use the original project number in
    the partcode.
    """
    def __init__(self, partcode, project='default'):
        """
        initialize path strings for MS Excel and main project folders
        store partcode and project parameters
        """
        self.program = str(PROGRAM_PATH['excel'])
        self.folder = str(FOLDER_PATH['jobcard'])
        self.partcode = str(partcode)
        self.project = str(project)

    def _folder_expression(self):
        """return a glob expression used in the find_folder method"""
        if self.project == 'default':
            project = self.partcode[3:7]
        return os.path.join(r'O:\*' + project + '*', 'Job Card*')

    def _file_expression(self, folder):
        """return a glob expression used in the find_file method"""
        return os.path.join(folder, '*' + self.partcode + '*.xls')


class PO(ExactMatch):
    """
    Using the purchase order [number], find the corresonding pdf paperwork
    in 'Pegasus' folder located on the Balmoral drive
    """
    def __init__(self, number):
        """
        initialize path strings for MS Excel and main project folders
        store partcode and project parameters
        """
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
    Open the manufacture drawing labels in 'My Document'
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


def run(program):
    call(PROGRAM_PATH[program])
