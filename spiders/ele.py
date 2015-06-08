#!/usr/bin/env python
#-*- encoding: utf8 -*-

import pymongo

from spiderflow import SpiderNode, AsyncSpiderProcess, MemoryQueue
from spiderflow.storage.stream import ConsoleStream
from spiderflow.storage.rdbstorage import  RDBStorage

class EleRDBStorage(RDBStorage):
    def save(self, doc):
        tb = self.metadata.tables[self.kwargs['table']]
        ins = tb.insert().values(**doc)
        self.engine.execute(ins)

dealstrg = EleRDBStorage(driver='postgresql', host='localhost', port='5432', \
        username='zzpwelkin', password='2191307', database='o2o',  table='dealer')

class ProductsSpider(SpiderNode):
    elems = {
        'base':'//li[contains(@id,"food_view")]',
        'logo':('a[contains(@class,"food_img")]/img/@srcset', None, None),
        'name':('descendant::a[contains(@class,"food_name")]/text()', None, None),
        'tag':('ancestor::section/h2/@title', None, None),
        'price':('descendant::span[contains(@class,"price")]/text()', None, None),
        'orders_per_month':('div/span[contains(@class,"sales")]/text()', None, '"re_str":"\d+"'),
        'dealer':('//a[@class="rst-logo"]/img/@alt', None, None),
        'describe':('descendant::p[@class="rst-d-desc"]/text()', None, None),
        }
    save = [{'driver':ConsoleStream}, 
            {'driver':EleRDBStorage, 
                'param':{
                    'driver':'postgresql',
                    'host':'localhost',
                    'port':'5432',
                    'username':'zzpwelkin',
                    'password':'2191307',
                    'database':'o2o',
                    'table':'products',
                    }
                }
            ]
#
#class DealersMoreSpider(SpiderNode):
#    """ 品牌餐厅"""
#    elems = {
#        'address':('//span[@itemprop="address"]/text()', None, None),
#        }
#    nextnodes = [(ProductsSpider, ('@ng-href', None, None), True),]
#
#    save = [{'dirver':ConsoleStream}, ]
#
#class DealersPremiumListSpider(SpiderNode):
#    elems = {
#            'base':'//a[@ng-href][@data-rst-id]',
#            'logo':('div[1]/img/@ng-src', None, None),
#            'name':('div[2]/div[contains(@class,"title")]/text()', None, None),
#            }
#    nextnodes = [(DealersMoreSpider, ('@ng-href', None, None), True),]

#class DealersListSpider(SpiderNode):
#    elems = {
#            'base':'//div[@class="clearfix"]/a',
#            'logo':('div[1]/img/@src', None, None),
#            'name':('div[2]/div[contains(@class,"title")]/text()', None, None),
#            }
#    nextnodes = [(DealersPremiumListSpider, ('//a[@class="viewmore"]', None, 'pre_str:"http://ele.me"'), False),
#            (DealersMoreSpider,('@href', None, None), True,)]

class DealersETL(object):
    """
    从mongo数据库中提取出商家信息并入库
    """
    _logo_url_prefix = "http://fuss10.elemecdn.com"
    _deal_url_prefix = "http://r.ele.me/"

    def __init__(self):
        con = pymongo.connection.MongoClient()
        self._col = con['o2o']['ele_dealer']

    def load2db(self):
        for d in self._col.find():
            v = {'name':d['name'], 
                    'address':d['address'],
                    'logo':self._logo_url_prefix+d['image_path'],
                    'min_price':d['minimum_order_amount'],
                    'service_price':d['delivery_fee'],
                    }

            dealstrg.save(v)
        
    def dealer_urls(self):
        return [self._deal_url_prefix+d['name_for_url'] for d in self._col.find()]

if __name__ == "__main__":
    #surls = [(ProductsSpider, 'http://r.ele.me/nylhct'), ]
    dp = DealersETL()
    #dp.load2db()

    asp = AsyncSpiderProcess(start_urls=[(ProductsSpider, x) for x in dp.dealer_urls()], queue=MemoryQueue())
    asp.start()
