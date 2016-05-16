"""
Useful command line inferface for the shortcut methods. Can not be
imported by the module. TODO
"""

from . import core
from pprint import pprint
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def main():
    pass


@main.command(help='Open manufacture drawing in Dropbox.')
@click.argument('partcode')
@click.option('-p', '--path', is_flag=True, help='Print path location.')
@click.option('-f', '--folder', is_flag=True, help='Open/find folder.')
def drawing(partcode, path, folder):
    shortcut = core.Drawing(partcode)
    parse_options(shortcut, path, folder)


@main.command(help='Open manufacture jobcard in Balmoral.')
@click.argument('partcode')
@click.option('-p', '--path', is_flag=True, help='Print path location.')
@click.option('-f', '--folder', is_flag=True, help='Open/find folder.')
def jobcard(partcode, path, folder):
    shortcut = core.Jobcard(partcode)
    parse_options(shortcut, path, folder)


@main.command(help='Open purchase order in Balmoral.')
@click.option('-p', '--path', is_flag=True, help='Print path location.')
@click.option('-f', '--folder', is_flag=True, help='Open/find folder.')
@click.argument('po_number')
def po(po_number, path, folder):
    shortcut = core.PO(po_number)
    parse_options(shortcut, path, folder)


@main.command(help='Open sticker template.')
@click.option('-p', '--path', is_flag=True, help='Print path location.')
@click.option('-f', '--folder', is_flag=True, help='Open/find folder.')
def sticker(path, folder):
    shortcut = core.Sticker()
    parse_options(shortcut, path, folder)


def parse_options(shortcut, path, folder):
    if not path and not folder:
        shortcut.open_file()
    elif not path and folder:
        shortcut.open_folder()
    elif path and not folder:
        pprint(shortcut.find_file())
    else:
        pprint(shortcut.find_folder())
