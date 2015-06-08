#!/usr/bin/env python
#-*- encoding:utf8 -*-

"""
机器查询基本接口
"""

from sqlalchemy import create_engine, MetaData

engine = create_engine("postgresql://zzpwelkin:2191307@localhost:5432/o2o")
metadata = MetaData()
metadata.reflect(engine, views=True)

deal_tb = metadata.tables['dealer']
prod_tb = metadata.tables['products']

def select(obj, number=1, com_cond=None, extra_cond=None):
    """
    @param extra_con: 其他的条件. 格式为{cond:1 or 0}.其中1表示必须
        要存在的，0表示必须不存在的
    """
    pass

def filter(dealer=None, time_cond=60):
    pass

def resort(strategy='seam_dealer'):
    pass
