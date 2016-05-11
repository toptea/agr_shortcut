# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 08:20:30 2016

@author: Gary
"""

import subprocess
import glob
import os
from constants import APP_LOCATION, FILE_LOCATION



def operation():
    subprocess.Popen(app['operation'])


def jobcard(project):
    jobcard = glob.glob('O:\\*\\Job Card*\\' + project + '*.xls*')
    folder = glob.glob('O:\\*' + project[3:7] + '*\\Job Card*')
    if jobcard:
        subprocess.Popen([app['excel'], jobcard[0]])
    elif folder:
        subprocess.Popen('explorer' + ' "' + folder[0] + '"')
    else:
        print("Can't find job card folder!")


def stickers(arg=None):
    """ open the sticker spreadsheet template"""
    program = 'C:\\Program Files\\Microsoft Office\\Office12\\EXCEL.EXE'
    path = (
        'C:\\Documents and Settings\\GARY\\My Documents\\' +
        'Templates\\Labels - Drawings\\')
    if arg == 'blank':
        filename = 'Stickers - Blanks.xls'
    elif arg == 'formulated':
        filename = 'Stickers - Formulated.xls'
    else:
        filename = 'Stickers.xls'
    subprocess.Popen(program + " \"" + path + filename + "\"")


def po(number):
    """ open the purchase order pdf"""
    program = 'C:\\Program Files\\Adobe\\Reader 11.0\\Reader\\AcroRd32.exe'
    path = '\\\\Balmoral\\Pegasus\\Operations II\\data\\A_PDF\\PO_00'
    print(program + " \"" + path + str(number) + ".pdf\"")
    """
    try:
        subprocess.Popen(program + " \"" + path + str(number) + ".pdf\"")
    except:
        print("Can't find PO")
    """


def drawing(partcode):
    """ open manufacture drawing pdf"""
    program = 'C:\\Program Files\\Adobe\\Reader 11.0\\Reader\\AcroRd32.exe'
    path = (
        'C:\\Documents and Settings\\GARY\\' +
        'My Documents\\Dropbox\\0001-AGR Project-Files\\')
    path = glob.glob(path + '*' + str(partcode[3:7]) + '*\\')[0]
    try:
        subprocess.Popen(program + " \"" + path + partcode + ".pdf\"")
    except:
        print("Can't find drawing in Dropbox")


class Drawing:
    def __init__(self, partcode):
        self.partcode = partcode
        self.program = APP_LOCATION['pdf_reader']
        self.initial_file_path = (
            'C:\\Documents and Settings\\GARY\\' +
            'My Documents\\Dropbox\\0001-AGR Project-Files\\')

    def find_folder_path(self):
        agr_project_number = str(self.partcode[3:7])
        initial_file_path = self.initial_file_path
        filepaths = glob.glob(
            initial_file_path + '*' + agr_project_number + '*\\')
        return filepaths[0]

    def find_file_path(self):
        pass

    def open_folder(self):
        pass

    def open_file(self):
        filepath = self.find_file()
        program = self.program
        try:
            subprocess.Popen(program + " \"" + filepath + ".pdf\"")
        except:
            print("Can't find drawing in Dropbox")


def main():
    d = Drawing('AGR1288-800-01')
    print(d.find_file())


if __name__ == '__main__':
    main()
