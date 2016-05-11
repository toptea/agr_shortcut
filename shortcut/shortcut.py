# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 08:20:30 2016

@author: Gary


>>> import os
>>> os.path.join(r"C:\mypath", "subfolder")
'C:\\mypath\\subfolder'

"""
import subprocess
import glob
import os

from shortcut_base import Shortcut
from constants import PROGRAM_PATH, FOLDER_PATH


class Drawing(Shortcut):

    def __init__(self, partcode, project=None):
        self.program = PROGRAM_PATH['pdf_reader']
        self.folder = FOLDER_PATH['pdf_drawings']
        self.partcode = partcode
        if project is None:
            self.project = partcode[3:7]
        else:
            self.project = project

    def find_folder_paths(self):
        globber = os.path.join(self.folder, '*' + self.project + '*')
        folders = glob.glob(globber)
        if len(folders) == 0:
            message = 'Invalid glob expression: ' + globber
            raise NotADirectoryError(message)
        return folders

    def find_file_paths(self):
        files = []
        for folder in self.find_folder_paths():
            globber = os.path.join(folder, self.partcode + '.pdf')
            file = glob.glob(globber)
            files.extend(file)
        if len(files) == 0:
            message = self.partcode + '.pdf in ' + self.project + ' folder'
            raise FileNotFoundError(message)
        return files


class PO(Shortcut):

    def __init__(self, number):
        self.program = PROGRAM_PATH['pdf_reader']
        self.folder = FOLDER_PATH['purchase_order']
        self.number = str(number)

    def find_folder_paths(self):
        if not os.path.isdir(self.folder):
            message = 'Invalid path: ' + self.folder
            raise NotADirectoryError(message)
        return self.folder

    def find_file_paths(self):
        file = os.path.join(self.folder, 'PO_00' + self.number + '.PDF')
        if not os.path.exists(file):
            message = 'Invalid path: ' + file
            raise FileNotFoundError(message)
        return file


class Jobcard(Shortcut):

    def __init__(self, partcode, project=None):
        self.program = PROGRAM_PATH['excel']
        self.folder = FOLDER_PATH['jobcard']
        self.partcode = partcode
        if project is None:
            self.project = partcode[3:7]
        else:
            self.project = project

    def find_folder_paths(self):
        globber = os.path.join(r'O:\*' + self.project + '*', 'Job Card*')
        folders = glob.glob(globber)
        if len(folders) == 0:
            message = 'Invalid glob expression: ' + globber
            raise NotADirectoryError(message)
        return folders

    def find_file_paths(self):
        files = []
        for folder in self.find_folder_paths():
            globber = os.path.join(folder, '*' + self.partcode + '*.xls')
            file = glob.glob(globber)
            files.extend(file)
        if len(files) == 0:
            message = 'Jobcard: ' + self.partcode
            raise FileNotFoundError(message)
        return files


def run(program):
        subprocess.Popen(PROGRAM_PATH[program])


def main():
    d = Jobcard('AGR1288-010-00')
    print('folder:')
    print(d.find_folder_paths())
    print('\nfile:')
    print(d.find_file_paths())
    d.open_folder()
    d.open_file()
    print('finish')


if __name__ == '__main__':
    main()
