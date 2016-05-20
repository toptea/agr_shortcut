import logging


def bom_for_duplication(df, assy=None, electric_only=False):
    """
    return a dataframe with parts that are duplicated
    on the bom
    """
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
    df = df[['projcode', 'assy', 'item',
             'partcode', 'desc', 'qty', 'std_cost']]
    if len(df) == 0:
        logging.info("No dublicated parts found on the '" + assy + "' BOM")
    else:
        logging.warning("Dublicated parts found on the '" + assy + "' BOM...")
        # return df
