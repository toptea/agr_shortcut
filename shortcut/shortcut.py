# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 08:20:30 2016

@author: Gary


>>> import os
>>> os.path.join(r"C:\mypath", "subfolder")
'C:\\mypath\\subfolder'

"""
import subprocess
import os

from shortcut_base import GlobMatch, ExactMatch
from constants import PROGRAM_PATH, FOLDER_PATH,


class Drawing(GlobMatch):

    def __init__(self, partcode, project=None):
        self.program = PROGRAM_PATH['pdf_reader']
        self.folder = FOLDER_PATH['pdf_drawings']
        self.partcode = partcode
        self.project = project

    def _folder_expression(self):
        if self.project is None:
            project = self.partcode[3:7]
        return os.path.join(self.folder, '*' + project + '*')

    def _file_expression(self, folder):
        return os.path.join(folder, self.partcode + '.pdf')


class Jobcard(GlobMatch):

    def __init__(self, partcode, project=None):
        self.program = PROGRAM_PATH['excel']
        self.folder = FOLDER_PATH['jobcard']
        self.partcode = partcode
        self.project = project

    def _folder_expression(self):
        if self.project is None:
            project = self.partcode[3:7]
        return os.path.join(r'O:\*' + project + '*', 'Job Card*')

    def _file_expression(self, folder):
        return os.path.join(folder, '*' + self.partcode + '*.xls')


class PO(ExactMatch):

    def __init__(self, number):
        self.program = PROGRAM_PATH['pdf_reader']
        self.folder = FOLDER_PATH['purchase_order']
        self.number = str(number)

    def _folder_expression(self):
        return self.folder

    def _file_expression(self):
        return os.path.join(self.folder, 'PO_00' + self.number + '.PDF')


class Sticker(ExactMatch):

    def __init__(self):
        self.program = PROGRAM_PATH['excel']
        self.folder = FOLDER_PATH['stickers']
        self.file = 'drawing labels - normal 7x2.xls'

    def _folder_expression(self):
        return self.folder

    def _file_expression(self):
        return os.path.join(self.folder, self.file)


def run(program):
        subprocess.Popen(PROGRAM_PATH[program])


def main():
    d = Sticker()
    print('folder:')
    print(d.find_folder_path())
    print('\nfile:')
    print(d.find_file_path())
    d.open_folder()
    d.open_file()
    print('finish')


if __name__ == '__main__':
    main()
