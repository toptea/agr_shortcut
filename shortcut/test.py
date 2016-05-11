# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:08:07 2016

@author: Gary
"""

import unittest
import shortcut


class TestDrawing(unittest.TestCase):

    def setUp(self):
        self.drawing = shortcut.Drawing('AGR1288-010-00')

    def test_find_folder_path(self):
        expect = [
            r'C:\Documents and Settings\GARY\My Documents\Dropbox' +
            r'\0001-AGR Project-Files\AGR1288-HTL Pen Needle Line-2']
        actual = self.drawing.find_folder_path()
        self.assertEqual(expect, actual)

    def test_find_file_path(self):
        expect = [
            r'C:\Documents and Settings\GARY\My Documents\Dropbox' +
            r'\0001-AGR Project-Files\AGR1288-HTL Pen Needle Line-2' +
            r'\AGR1288-010-00.pdf']
        actual = self.drawing.find_file_path()
        self.assertEqual(expect, actual)


class TestJobcard(unittest.TestCase):

    def setUp(self):
        self.jc = shortcut.Jobcard('AGR1288-010-00')

    def test_find_folder_path(self):
        expect = [r'O:\AGR-1288 HTL Pen Needle-2\Job Cards']
        actual = self.jc.find_folder_path()
        self.assertEqual(expect, actual)

    def test_find_file_path(self):
        expect = [
            r'O:\AGR-1288 HTL Pen Needle-2\Job Cards' +
            r'\AGR1288-010-00 Needle Hub Feeder.xls']
        actual = self.jc.find_file_path()
        self.assertEqual(expect, actual)


class TestPO(unittest.TestCase):

    def setUp(self):
        self.po = shortcut.PO(60000)

    def test_find_folder_path(self):
        expect = r'\\Balmoral\Pegasus\Operations II\data\A_PDF'
        actual = self.po.find_folder_path()
        self.assertEqual(expect, actual)

    def test_find_file_path(self):
        expect = (
            r'\\Balmoral\Pegasus\Operations II\data\A_PDF' +
            r'\PO_0060000.PDF')
        actual = self.po.find_file_path()
        self.assertEqual(expect, actual)


class TestSticker(unittest.TestCase):

    def setUp(self):
        self.sticker = shortcut.Sticker()

    def test_find_folder_path(self):
        expect = (
            r'C:\Documents and Settings\GARY\My Documents' +
            r'\work\templates\labels')
        actual = self.sticker.find_folder_path()
        self.assertEqual(expect, actual)

    def test_find_file_path(self):
        expect = (
            r'C:\Documents and Settings\GARY\My Documents' +
            r'\work\templates\labels\drawing labels - normal 7x2.xls')
        actual = self.sticker.find_file_path()
        self.assertEqual(expect, actual)

if __name__ == '__main__':
    unittest.main()
