# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:24:28 2016

@author: Gary
"""

import subprocess
from abc import ABCMeta, abstractmethod


class Shortcut(metaclass=ABCMeta):

    def __init__(self):
        self.program = None
        self.folder = None

    @abstractmethod
    def find_folder_paths(self):
        pass

    @abstractmethod
    def find_file_paths(self):
        pass

    def open_folder(self):
        folder = self.find_folder_paths()
        if type(folder) == list:
            folder = folder[0]
        folder = '"' + folder + '"'
        subprocess.Popen('explorer ' + folder)

    def open_file(self):
        file = self.find_file_paths()
        if type(file) == list:
            file = file[0]
        file = '"' + file + '"'
        program = '"' + self.program + '"'
        subprocess.Popen(program + ' ' + file)