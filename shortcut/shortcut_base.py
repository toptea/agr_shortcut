# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:24:28 2016

@author: Gary
"""

import subprocess
import glob
import os
from abc import ABCMeta, abstractmethod


class Shortcut(metaclass=ABCMeta):

    @abstractmethod
    def find_folder_path(self):
        pass

    @abstractmethod
    def find_file_path(self):
        pass

    def open_folder(self):
        folder = self.find_folder_path()
        if type(folder) == list:
            folder = folder[0]
        folder = '"' + folder + '"'
        subprocess.Popen('explorer ' + folder)

    def open_file(self):
        file = self.find_file_path()
        if type(file) == list:
            file = file[0]
        file = '"' + file + '"'
        program = '"' + self.program + '"'
        subprocess.Popen(program + ' ' + file)


class GlobMatch(Shortcut):

    @abstractmethod
    def _folder_expression(self):
        return None

    @abstractmethod
    def _file_expression(self):
        return None

    def find_folder_path(self):
        folders = glob.glob(self._folder_expression())
        if len(folders) == 0:
            message = 'Invalid glob expression: ' + self._folder_expression()
            raise NotADirectoryError(message)
        return folders

    def find_file_path(self):
        files = []
        for folder in self.find_folder_path():
            file = glob.glob(self._file_expression(folder))
            files.extend(file)
        if len(files) == 0:
            message = 'Invalid glob expression: ' + self._file_expression()
            raise FileNotFoundError(message)
        return files


class ExactMatch(Shortcut):

    @abstractmethod
    def _folder_expression(self):
        return None

    @abstractmethod
    def _file_expression(self):
        return None

    def find_folder_path(self):
        folder = self._folder_expression()
        if not os.path.isdir(folder):
            message = 'Invalid path: ' + folder
            raise NotADirectoryError(message)
        return folder

    def find_file_path(self):
        file = self._file_expression()
        if not os.path.exists(file):
            message = 'Invalid path: ' + file
            raise FileNotFoundError(message)
        return file
