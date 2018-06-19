"""
This module contains function that loads data from:
- Foxpro Operation database
- MS Access Cooperation database
And return a Panda dataframe
"""


import datetime as dt
import pandas as pd
from contextlib import closing
from .. import secret


def ref_plan():
    """return a dictionary of useful infomation about the project"""

    sql = (
        """
        SELECT
            scust.comp_name,
            sitem.desc1,
            sitem.son,
            sitem.pstk,
            sitem.ijn,
            sitem.ord_qty,
            shead.order_date,
            shead.duedate,
            sitem.items_net


        FROM sitem
            LEFT JOIN shead
                ON sitem.son = shead.son
            LEFT JOIN scust
                ON shead.comp_no = scust.comp_no

        """)

    with closing(secret.get_connection('foxpro')) as connection:
        df = pd.read_sql(sql, con=connection)

        df = df.rename(columns={
                'comp_name': 'customer',
                'desc1': 'description',
                'duedate': 'delivery_date',
                'items_net': 'net_cost',
                'pstk': 'project'
            })

    df['project'] = df.project.str.strip()
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['delivery_date'] = pd.to_datetime(df['delivery_date'])
    df = df[(df.order_date >= pd.to_datetime('2016-01-01')) | (df.delivery_date >= pd.to_datetime('2016-01-01'))]
    df['customer'] = df['customer'].str.strip()
    df['description'] = df['description'].str.strip()
    df['order_month'] = df.order_date.map(lambda x: x.strftime('%B-%Y'))
    df['delivery_month'] = df.delivery_date.map(lambda x: x.strftime('%B-%Y'))
    df = df[df.project.str[0:3] == 'AGR']

    b1 = (df.net_cost >= 10000)          # less
    b2 = (df.project.str[-3:] == '-00')  # whole project
    b3 = (df.project.str[0:4] == 'AGR1')       # new project
    df = df[ b1 | b2]
    df = df[ b1 | b3]
    return df


if __name__ == '__main__':
    df = ref_plan()
    df.to_csv(r'C:\code\python\shortcut\test.csv')

