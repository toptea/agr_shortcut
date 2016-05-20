"""
This module define base classes for the shortcut objects found in
core.py file.
"""

import glob
import os
from subprocess import Popen
from abc import ABCMeta, abstractmethod


class Match(metaclass=ABCMeta):
    """Base Class"""

    def __init__(self):
        self.program = None
        self.folder = None

    @abstractmethod
    def find_folder(self):
        """abstract method - defined in the GlobMatch/ExactMatch classes"""
        pass

    @abstractmethod
    def find_file(self):
        """abstract method - defined in the GlobMatch/ExactMatch classes"""
        pass

    def open_folder(self):
        """
        take the path string (or take the first element if its a list) and
        open the folder using subprocess Popen
        """
        folder = self.find_folder()
        if isinstance(folder, list):
            folder = folder[0]
        folder = _add_commas(folder)
        Popen('explorer ' + folder)

    def open_file(self):
        """
        take the path string (or take the first element if its a list) and
        open the file using subprocess Popen
        """
        file = self.find_file()
        if isinstance(file, list):
            file = file[0]
        file = _add_commas(file)
        program = _add_commas(self.program)
        Popen(program + ' ' + file)

    def open(self):
        """open file and if its not possible, open folder"""
        try:
            self.open_file()
        except:
            self.open_folder()


class GlobMatch(Match):
    """Base Class - search multiple of folders/files"""

    @abstractmethod
    def _folder_expression(self):
        """abstract method - defined in the core shortcut classes"""
        return None

    @abstractmethod
    def _file_expression(self, folder):
        """abstract method - defined in the core shortcut classes"""
        return None

    def find_folder(self):
        """return folder path list"""
        folders = glob.glob(self._folder_expression())
        if len(folders) == 0:
            raise NotADirectoryError(self._folder_expression())
        return folders

    def find_file(self, folders=None):
        """return file path list"""
        if folders is None:
            folders = self.find_folder()
        files = []
        for folder in folders:
            file = glob.glob(self._file_expression(folder))
            files.extend(file)
        if len(files) == 0:
            raise FileNotFoundError(self._file_expression())
        return files


class ExactMatch(Match):
    """Base Class - search one folder/file"""

    @abstractmethod
    def _folder_expression(self):
        """abstract method - defined in the core shortcut classes"""
        return None

    @abstractmethod
    def _file_expression(self):
        """abstract method - defined in the core shortcut classes"""
        return None

    def find_folder(self):
        """return folder path string"""
        folder = self._folder_expression()
        if not os.path.isdir(folder):
            raise NotADirectoryError(folder)
        return folder

    def find_file(self):
        """return file path string"""
        file = self._file_expression()
        if not os.path.exists(file):
            raise FileNotFoundError(file)
        return file


def _add_commas(string):
    return '"' + string + '"'
