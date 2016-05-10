# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 08:20:30 2016

@author: Gary
"""

import subprocess
import glob
import os


app = {
    'pdf': r'C:\Program Files\Adobe\Reader 11.0\Reader\AcroRd32.exe',
    'autohotkey': r'C:\Program Files\AutoHotkey\AutoHotkey.exe',
    'excel': r'C:\Program Files\Microsoft Office\Office12\EXCEL.EXE',
    'email': r'C:\Program Files\Microsoft Office\Office12\OUTLOOK.EXE',
    'word': r'C:\Program Files\Microsoft Office\Office12\WINWORD.EXE',
    'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
    'notepad': r'C:\Program Files\Notepad++\notepad++.exe',
    'paint': r'C:\Program Files\Paint.NET\PaintDotNet.exe',
    'r': r'C:\Program Files\RStudio\bin\rstudio.exe',
    'tabula': r'C:\Program Files\tabula\tabula.exe',
    'cmd': r'C:\Program Files\ConEmu\ConEmu.exe',
    'operation': r'C:\Program Files\Pegasus\Operations II\Operations.exe'
    }


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
    jobcard('AGR1288-800-01')


if __name__ == '__main__':
    main()
