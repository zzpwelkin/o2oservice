#!/usr/bin/env python
#-*- encoding:utf8 -*-

import json
import re
import requests
import pymongo

def extract(url):
    """
    extract dealer infomations from application/json content
    """
    limit, offset = 100, 0
    f = True
    while(f):
        url += "&offset={0}&limit={1}".format(offset, limit)
        req = requests.get(url)
        docs = json.loads(req.text)
        for d in docs:
            d['_id'] = d['name_for_url']
            d['dists'] = []
            dists_url = u'http://r.ele.me/{0}'.format(d['name_for_url'])
            req = requests.get(dists_url)
            dists = re.findall('var menu = (.*);\n', req.text)
            if dists:
                d['dists'] = json.loads(dists[0], encoding='utf8')
            yield d
        if len(docs)<limit:
            f = False
        else:
            offset += limit


if __name__ == "__main__":
    url_form="http://restapi.ele.me/v1/restaurants?type=geohash&geohash={0}"
    start_urls = ['wtsqqnp9ecs7']
    mgclt = pymongo.connection.MongoClient()
    col = mgclt['o2o']['ele_dealer']
    for url in start_urls:
        for doc in extract(url_form.format(url)):
            col.insert(doc)
        
