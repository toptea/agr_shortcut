"""
Dublication in the BOM can cause problems when printing out change notice.
This module contain a function that roughly scan the bom for duplications.
"""
import logging


def bom_for_duplication(df, assy=None, electric_only=False, show=False):
    """check if there are duplicated parts on the bom"""
    if assy is not None:
        df = df[df.assy == assy]

    if electric_only is True:
        df = df[df.assy.str[0:3] == 'AGR']
        df = df[df.assy.str[8] == '8']

    df = df[df.duplicated(subset=['projcode', 'assy', 'partcode'],
                          keep=False)]
    df = df[~df.duplicated(subset=['projcode', 'assy', 'item', 'partcode'],
                           keep=False)]
    df = df.sort_values(['projcode', 'assy', 'partcode'])
    df = df.reset_index()
    df = df[['projcode', 'assy', 'item',
             'partcode', 'desc', 'qty', 'std_cost']]

    if len(df) == 0:
        logging.info("No dublicated parts found on the '" + assy + "' BOM")

    if len(df) != 0:
        logging.warning("Dublicated parts found on the '" + assy + "' BOM!!!")

    if len(df) != 0 and show:
        print(df[['item', 'partcode', 'desc']])
