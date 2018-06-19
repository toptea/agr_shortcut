"""
Dublication in the BOM can cause problems when printing out change notice.
This module contain a function that roughly scan the bom for duplications.
"""
import logging
import itertools
from fuzzywuzzy import fuzz
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.expand_frame_repr', False)

def bom_for_duplication(df, assy=None, electric_only=False, show=False):
    """check if there are duplicated parts on the bom"""
    if assy is not None:
        df = df[df.assy == assy]

    if electric_only is True:
        df = df[df.assy.str[0:3] == 'AGR']
        df = df[df.assy.str[8] == '8']

    df1 = df.copy()

    df1 = df1[df.duplicated(subset=['projcode', 'assy', 'partcode'],
                          keep=False)]
    df1 = df1[~df.duplicated(subset=['projcode', 'assy', 'item', 'partcode'],
                           keep=False)]
    df1 = df1.sort_values(['projcode', 'assy', 'partcode'])
    df1 = df1.reset_index()
    df1 = df1[['projcode', 'assy', 'item',
             'partcode', 'desc', 'qty', 'std_cost']]

    if len(df1) == 0:
        logging.info('')
        logging.info('Checking part number dublication:')
        logging.info("No dublicated parts found on the '" + assy + "' BOM")

    if len(df1) != 0:
        logging.warning("Dublicated parts found on the '" + assy + "' BOM!!!")

    if len(df1) != 0 and show:
        logging.info(df1[['item', 'partcode', 'desc']])

    df = df[(df.partcode.str[:3] != 'AGR')]

    list_a = []
    list_b = []
    list_fuzz = []
    for a, b in itertools.combinations(df.desc.values, 2):
        list_a.append(a.strip())
        list_b.append(b.strip())
        list_fuzz.append(fuzz.token_set_ratio(a, b))

    df2 = pd.DataFrame({
        'desc_a': list_a,
        'desc_b': list_b,
        'fuzz_ratio': list_fuzz})

    df2 = df2.sort_values('fuzz_ratio', ascending=False)
    df2 = df2[df2.fuzz_ratio >= 75]
    df2 = df2.reset_index()
    df2 = df2[['desc_a', 'desc_b', 'fuzz_ratio']]
    logging.info('')
    logging.info('Checking pur part description dublication:')
    logging.info(df2)
