# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 08:20:30 2016

@author: Gary
"""

import subprocess
import glob
import os


def jobcard(project):
    """ open the job card folder"""
    project_folder = glob.glob('O:\\*' + str(project) + '*\\')
    project_folder = [x for x in project_folder if os.path.isdir]
    if project_folder:
        jobcard_folder = glob.glob(project_folder[0] + '\\Job Card*')

    if jobcard_folder:
        subprocess.Popen('explorer ' + jobcard_folder[0])
    elif project_folder:
        subprocess.Popen('explorer ' + project_folder[0])
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
    try:
        subprocess.Popen(program + " \"" + path + str(number) + ".pdf\"")
    except:
        print("Can't find PO")


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


def main():
    drawing('AGR1271-111-03')


if __name__ == '__main__':
    main()
