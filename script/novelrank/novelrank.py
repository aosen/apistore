# -*- coding: utf-8 -*-
#!/usr/bin/python

import pandas as pd
import MySQLdb
import datetime
import sys
sys.path.append("../../")

from script.settings import DATABASES, logger

if __name__ == "__main__":
    mysql_cn= MySQLdb.connect(
            host=DATABASES['HOST'], 
            user=DATABASES['USER'], 
            passwd=DATABASES['PASSWORD'], 
            db=DATABASES['NAME'],
            charset="utf8")
    sql = "SELECT id, title, first, second, author, picture, novelpv FROM novel"
    df = pd.read_sql(sql, con=mysql_cn)
    df = df.sort_values(by='novelpv', ascending=False)
    df.rename(columns={'id': 'novelid'}, inplace=True)
    df['createtime'] = datetime.date.today()
    """
    df['id'] = 0
    l = df['novelid'].count()
    for i in range(l):
        df['id'][i] = l - i
    """
    pd.io.sql.to_sql(df, 'novelrank', mysql_cn, flavor='mysql', if_exists='replace')
    mysql_cn.close()
    logger.info("[%s] sort success" % datetime.date.today())
