"""
Useful command line inferface for the shortcut methods. Can not be
imported by the module.
"""
import click
from pprint import pprint
from .navigate import core as nav

from .create import load
from .create import check
from .create import core

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def main():
    """AGR Shortcut"""
    pass


@main.command(help='Open manufacture drawing in Dropbox.')
@click.argument('partcode')
@click.option('-p', '--path', is_flag=True, help='Print path location.')
@click.option('-f', '--folder', is_flag=True, help='Open/find folder.')
def drawing(partcode, path, folder):
    """command for drawing shortcut"""
    shortcut = nav.Drawing(partcode)
    parse_options(shortcut, path, folder)


@main.command(help='Open manufacture jobcard in Balmoral.')
@click.argument('partcode')
@click.option('-p', '--path', is_flag=True, help='Print path location.')
@click.option('-f', '--folder', is_flag=True, help='Open/find folder.')
def jobcard(partcode, path, folder):
    """command for jobcard shortcut"""
    shortcut = nav.Jobcard(partcode)
    parse_options(shortcut, path, folder)


@main.command(help='Open purchase order in Balmoral.')
@click.option('-p', '--path', is_flag=True, help='Print path location.')
@click.option('-f', '--folder', is_flag=True, help='Open/find folder.')
@click.argument('po_number')
def po(po_number, path, folder):
    """command for purchase order shortcut"""
    shortcut = nav.PO(po_number)
    parse_options(shortcut, path, folder)


@main.command(help='Open sticker template.')
@click.option('-p', '--path', is_flag=True, help='Print path location.')
@click.option('-f', '--folder', is_flag=True, help='Open/find folder.')
def sticker(path, folder):
    """command for sticker shortcut"""
    shortcut = nav.Sticker()
    parse_options(shortcut, path, folder)


@main.command(help='Create manufacture jobcard')
@click.argument('args', nargs=-1)
def new_jobcard(args):
    """command for drawing shortcut"""
    core.jobcard(*args)


@main.command(help='Find duplication on the bom')
@click.argument('args', nargs=-1)
def dubs(args):
    """command for finding duplication on the bom"""
    coop_data = load.coop_bom_directly(args[0])
    check.bom_for_duplication(coop_data, args[1], show=True)


def parse_options(shortcut, path, folder):
    """helper function for shortcut objects"""
    if not path and not folder:
        shortcut.open_file()
    elif not path and folder:
        shortcut.open_folder()
    elif path and not folder:
        pprint(shortcut.find_file())
    else:
        pprint(shortcut.find_folder())
