# -*- coding: utf-8 -*-
"""
Created on Thu May 12 11:32:49 2016

@author: Gary
"""

from subprocess import call


def test():
    call('python -m unittest')


def uml_diagram():
    call('pyreverse -Amy -o png -p shortcut shortcut\core.py')


def main():
    test()
    uml_diagram()


if __name__ == '__main__':
    main()
