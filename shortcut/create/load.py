"""
This module contains function that loads data from:
- Foxpro Operation database
- MS Access Cooperation database
And return a Panda dataframe
"""

import logging
import pandas as pd
pd.set_option('display.expand_frame_repr', False)

from contextlib import closing
from .. import secret


def coop_bom_directly(proj):
    """
    Read Cooperation, a Microsoft Access database and
    return the project BOM. In an adjacency list format
    (parent assy -> child assy). Need to preprocess this
    since the quantity is only for one section, no matter
    if the level above specified for more
    """
    if len(proj) > 10:
        return None
    sql = (
        """
        SELECT
            Project,
            Parent_drawing,
            item,
            Drawing_no,
            units,
            description,
            material,
            COST_PR,
            L
        FROM local_boms

        WHERE
            Project = '{0}'

        ORDER BY
            Parent_drawing, item
        """).format(proj)

    with closing(secret.get_connection('access_bom')) as connection:
        df = pd.read_sql(sql, con=connection)
        df = df.rename(columns={
            'Project': 'projcode',
            'Parent_drawing': 'assy',
            'Drawing_no': 'partcode',
            'units': 'qty',
            'description': 'desc',
            'COST_PR': 'std_cost',
            'L': 'length'})
        df = df[df.partcode != '90015410']
    return df


def bom(proj, top_lvl_assy, assy):
    """Read Cooperation, a Microsoft Access database and
    return the section BOM with the part quantity corrected.

    (todo: this function is a bit messy, refactor this soon)
    """

    df = coop_bom_directly(proj)
    unique = _unique_partcode(df)
    df = _s1_create_tabulated_bom(top_lvl_assy, df)
    if top_lvl_assy != assy:
        df = _s2_filter_tabulated_bom(assy, df)
    df = _s3_flatten_tabulated_bom(df)
    df = pd.merge(left=df, right=unique, how='left', on='partcode')
    df = df.reset_index()
    df = df.rename(columns={'index': 'item'})
    df['assy'] = assy

    dfr_list = pd.read_excel('C:/cooptemp2/Teamworks.xls', None)
    dfr = pd.concat(dfr_list, ignore_index=True)
    dfr = dfr.rename(columns={'DWG_NO': 'partcode', 'Revision Number': 'rev', 'Name': 'name'})
    b1 = dfr.name.str.contains('idw')
    b2 = dfr.name.str.contains('dwg')
    dfr = dfr[b1 | b2]
    dfr = dfr[['partcode', 'rev']]
    df = pd.merge(left=df, right=dfr, how='left', on='partcode')
    df['rev'] = df['rev'].fillna("")
    agr_partcode = df['partcode'].str[:3] == 'AGR'
    gil_partcode = df['partcode'].str[:3] == 'GIL'
    df['is_manu'] = (agr_partcode) | (gil_partcode)
    df['material'] = df['material'].fillna(" ")
    df = df[['assy', 'item', 'lvl', 'partcode',
             'rev', 'qty', 'desc', 'material', 'is_manu']]
    return df


def _unique_partcode(df):
    """private function for bom()

    return an unique partcode dataframe. One small change
    in the bom row produce dublicate rows. use this dataframe
    to prevent this.
    """
    df = df.groupby('partcode')[['desc', 'material']].last()
    df = df.reset_index()
    return df


def _s1_create_tabulated_bom(top_level, df):
    """private function for bom()

    take the project bom and keep joining to itself 9 times.
    this will show the quantity required at each bom level.
    """
    df = df[['assy', 'partcode', 'qty', 'item']]
    bom = df[df.assy == top_level]
    bom = bom.drop('assy', axis=1)
    bom = bom.rename(columns={
                'partcode': 'lvl1',
                'qty': 'qty1',
                'item': 'item1'})
    i = 1
    while True:
        bom = pd.merge(
            left=bom,
            right=df,
            how='left',
            left_on='lvl' + str(i),
            right_on='assy')
        bom = bom.drop('assy', axis=1)
        bom = bom.rename(columns={
                'partcode': 'lvl' + str(i+1),
                'qty': 'qty' + str(i+1),
                'item': 'item' + str(i+1)})
        i = i + 1
        if i == 9:
            break
    item_col = [col for col in bom.columns if 'item' in col]
    qty_col = [col for col in bom.columns if 'qty' in col]
    bom[item_col] = bom[item_col].fillna(0)
    bom[qty_col] = bom[qty_col].fillna(1)
    bom = bom.reindex_axis(sorted(bom.columns), axis=1)
    return bom


def _s2_filter_tabulated_bom(assy, df):
    """private function for bom()

    filter the project bom by assembly
    """
    assy_bom = pd.DataFrame()
    lvl_col = [col for col in df.columns if 'lvl' in col]
    for col in lvl_col:
        temp_bom = df[df[col] == assy]
        assy_bom = assy_bom.append(temp_bom)
    return assy_bom


def _s3_flatten_tabulated_bom(df):
    """private function for bom()

    instead of having sub-assemblies in 9 different column,
    put them all under one
    """
    i = 1
    bom = pd.DataFrame()
    item_col = [col for col in df.columns if 'item' in col]
    qty_col = [col for col in df.columns if 'qty' in col]
    for i in range(1, 10):
        gb_key = list(item_col[:i])
        gb_key.insert(0, 'lvl'+str(i))
        gb_val = list(qty_col[:i])
        drop_col = list(item_col[:i])
        drop_col.extend(qty_col[:i])
        assy_bom = df.groupby(gb_key)[gb_val].median().reset_index()
        assy_bom = assy_bom.rename(columns={'lvl'+str(i): 'partcode'})
        if 'item1' in assy_bom.columns:
            assy_bom['item1'] = assy_bom['item1']*10**24
        if 'item2' in assy_bom.columns:
            assy_bom['item2'] = assy_bom['item2']*10**21
        if 'item3' in assy_bom.columns:
            assy_bom['item3'] = assy_bom['item3']*10**18
        if 'item4' in assy_bom.columns:
            assy_bom['item4'] = assy_bom['item4']*10**15
        if 'item5' in assy_bom.columns:
            assy_bom['item5'] = assy_bom['item5']*10**12
        if 'item6' in assy_bom.columns:
            assy_bom['item6'] = assy_bom['item6']*10**9
        if 'item7' in assy_bom.columns:
            assy_bom['item7'] = assy_bom['item7']*10**6
        if 'item8' in assy_bom.columns:
            assy_bom['item8'] = assy_bom['item8']*10**3
        if 'item9' in assy_bom.columns:
            assy_bom['item9'] = assy_bom['item9']
        assy_bom['idn'] = assy_bom[item_col[:i]].sum(axis=1)
        assy_bom['qty'] = assy_bom[qty_col[:i]].product(axis=1)
        assy_bom['lvl'] = i
        assy_bom = assy_bom.drop(drop_col, axis=1)
        bom = bom.append(assy_bom)
    bom = bom.sort_values(by='idn')
    bom = bom.reset_index().drop('index', axis=1)
    return bom


def cost():
    """Read the SQL database and return a cost DataFrame

    This table contain parts with it's own unique partcode, description
    and cost summary statistics. Useful for cost estimation.
    """

    po_sql = (
        """
        SELECT
            pstk,
            MIN(price_per) AS "min_cost",
            AVG(price_per) AS "avg_cost",
            MAX(price_per) AS "max_cost",
            COUNT(pstk) AS "po_count"
        FROM pitem
        GROUP BY pstk
        ORDER BY pstk
        """)

    std_sql = (
        """
        SELECT
            cst.pstk,
            cst.desc1,
            cst.cost_pr AS "std_cost"
        FROM cst
        ORDER BY pstk
        """)

    # can't join tables in sql becasue of whitespace?
    logging.info('get cost data for time estimation')
    with closing(secret.get_connection('foxpro')) as connection:
        po = pd.read_sql(po_sql, con=connection)
        df = pd.read_sql(std_sql, con=connection)
    po['pstk'] = po['pstk'].str.strip()
    df['pstk'] = df['pstk'].str.strip()
    df = pd.merge(left=df, right=po, how='left', on='pstk')
    df['std_cost'] = df['std_cost'].fillna(0).round(2)
    df['min_cost'] = df['min_cost'].fillna(0).round(2)
    df['avg_cost'] = df['avg_cost'].fillna(0).round(2)
    df['max_cost'] = df['max_cost'].fillna(0).round(2)
    df['po_count'] = df['po_count'].fillna(0)
    return df


def bom_time(proj, top_lvl_assy, assy, cost_data):
    """estimated machined time of a section

    merge bom and cost dataframe together. divide the cost
    by a cost factor of 36 (regression was used to calculate
    the cost factor. the supplier quoted price was compared to
    the inhouse machined time, and plot a best fit line in the middle,
    where the y origin is zero. The points varies a lot so any value
    between 30 to 40 is valid. Although many assumption was ignored,
    take this value as a very quick and easy estimate.
    """
    df = bom(proj, top_lvl_assy, assy)
    # df = df[df.is_manu == True]
    df = pd.merge(left=df, right=cost_data,
                  how='left', left_on='partcode', right_on='pstk')

    df['avg_time'] = df['avg_cost'] / 36 / 0.25
    df['avg_time'] = df['avg_time'].round(0) * 0.25

    def ignore_pur_for_avg_time(x):
        if not x['is_manu']:
            return ""
        elif x['avg_time'] == 0:
            return ""
        else:
            return x['avg_time']

    df['avg_time'] = df.apply(ignore_pur_for_avg_time, axis=1)
    df = df[['item', 'lvl', 'partcode', 'rev', 'qty',
             'desc', 'material', 'avg_cost', 'avg_time', 'is_manu']]
    return df


def proj_head(ijn):
    """return a dictionary of useful infomation about the project"""
    df = pd.read_csv('shortcut/project.csv')
    df = df[df.ijn == int(ijn)]
    if len(df) > 0:
        header = df.to_dict(orient='records')[0]
    else:
        if len(str(ijn)) > 6:
            raise(Exception)
        sql = (
            """
            SELECT
                sitem.pstk,
                sitem.desc1,
                sitem.ord_qty,
                sitem.ijn,
                sitem.items_net,
                sitem.son,
                shead.order_date,
                shead.duedate,
                scust.comp_name

            FROM sitem
                LEFT JOIN shead
                    ON sitem.son = shead.son
                LEFT JOIN scust
                    ON shead.comp_no = scust.comp_no

            WHERE
                sitem.ijn == {0}

            """).format(ijn)

        with closing(secret.get_connection('foxpro')) as connection:
            logging.info("get project header for '" + str(ijn) + "'")
            df = pd.read_sql(sql, con=connection)
            df = df.rename(columns={
                    'comp_name': 'client',
                    'desc1': 'name',
                    'duedate': 'delivery_date',
                    'items_net': 'net_cost',
                    'pstk': 'code',
                })
            header = df.to_dict(orient='records')[0]
            header['delivery_date'] = header['delivery_date'].strftime("%d/%m/%y")

            header['client'] = header['client'].strip()
            header['name'] = header['name'].strip()
            header['code'] = header['code'].strip()
            header['ijn'] = int(header['ijn'])
            header['ord_qty'] = int(header['ord_qty'])
            header['son'] = int(header['son'])
    return header


def assy_head(proj, top_lvl_assy, assy_head_dict):
    """return assembly header dataframe"""
    df = bom(proj, top_lvl_assy, top_lvl_assy)
    logging.info("get assembly headers for '" + str(top_lvl_assy) + "'")
    df = df[df.lvl == 1]
    df = df[df.partcode.str[:3] == 'AGR']

    def tab_name(x):
        if x[11:] == '-00':
            return x[7:12]  # assy [3:11] [7:12]
        else:
            return x[7:15]  # assy & part [3:15] [7:15]

    df['tab_name'] = df['partcode'].apply(tab_name)
    df['qty'] = df['qty'] * assy_head_dict['ord_qty']
    df = df.reset_index()
    df = df[['tab_name', 'partcode', 'rev', 'qty', 'desc']]
    df = df.drop_duplicates()
    return df


def assy_part(proj, top_lvl_assy, assy, cost_data, proj_head_dict, show_indent=False, only_manu=True):
    """return manufacture BOM dataframe"""
    logging.info("get BOM for '" + str(assy) + "'")
    df = bom_time(proj, top_lvl_assy, assy, cost_data)

    df['qty'] = df['qty'] * proj_head_dict['ord_qty']
    df = df[df.lvl != 1]

    if show_indent:
        df['partcode'] = df.apply(
            lambda x: (x['lvl']-2) * '_' + x['partcode'], axis=1)

    if only_manu:
        df = df[df.is_manu == True]

    df = df.reset_index()
    df = df[['partcode', 'rev', 'qty', 'desc', 'material', 'avg_cost', 'avg_time', 'lvl']]
    return df
