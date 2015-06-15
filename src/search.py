#!/usr/bin/env python
#-*- encoding:utf8 -*-

"""
后台服务主要接口
"""
from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.sail.allegrographserver import AllegroGraphServer

namespaces = {
        'gr':'http://purl.org/goodrelations/v1#',
        }

def products(conn, dataset):
    """
    Get quality products of this dataset and return data only that have 
        products or service more than one 
    """
    resDts = {}
    askForm = u"""ask {{ ?dsh gr:name "{0}".}}"""
    queryForm = u"""select distinct ?dsh ?dshname where {{ ?dsh gr:name ?dshname. 
            FILTER  regex(?dshname, "{0}") .}}"""
    for k, v in dataset.iteritems():
        res = []
        if  not conn.prepareBooleanQuery(QueryLanguage.SPARQL, askForm.format(k)).evaluate():
            tupleQuery = conn.prepareTupleQuery(QueryLanguage.SPARQL, queryForm.format(k))
            result = tupleQuery.evaluate()
            if result.rowCount()>1:
                for r in result:
                    bnames = r.getBindingNames()
                    res.append([r.getValue(bnm).getValue() for bnm in bnames])
            if len(res)>1:
                resDts[k] = res

            result.close()

    return resDts

def dealers(conn, dataset):
    """
    Get the dealers
    """
    ret = []
    wraperForm = u"select distinct ?s ?dlname where {{ {0} }}"
    innerForm = u"""select ?s ?dlname where {{?s a gr:BusinessEntity;gr:name ?dlname;
            gr:offers[gr:includes ?dsh]. ?dsh gr:name "{0}".}}"""
    queryStr = u""
    for k, v in dataset.iteritems():
        queryStr += u"{{ {0} }}".format(innerForm.format(k))

    queryStr = wraperForm.format(queryStr)
    result = conn.prepareTupleQuery(QueryLanguage.SPARQL, queryStr).evaluate()
    for r in result:
        bnames = r.getBindingNames()
        ret.append([r.getValue(bnm).getValue() for bnm in bnames])
    result.close()
    return ret
    
def main(data):
    """
    Repositories: o2o
        Subrepositories: ele, ...

    @return: (FLAG, DATA). 
        (0, dealers) | (1, quality_products)
    """
    # connect to repostry and initial
    server = AllegroGraphServer(host='localhost', port=10035, user='zzpwelkin', password='2191307')
    repos = server.openCatalog().getRepository('o2o', Repository.OPEN)
    conn = repos.getConnection()

    # set default namespace 
    for ns,uri in namespaces.iteritems():
        conn.setNamespace(ns, uri)

    try:
        prds = products(conn, data)
        if prds:
            return (0, prds)
        else:
            dl = dealers(conn, data)
            return (1, dl)
    finally:
        conn.close()

if __name__ == "__main__":
    import json
    import optparse
    USAGE = "%progs [OPTIONS]"
    desc = u"根据文件定义查询相关内容"
    parser = optparse.OptionParser()
    parser.add_option('-f', '--rfile', action='store', help=u'查询的规则文件')

    args, _ = parser.parse_args()
    if not args.rfile:
        parser.print_help()
        exit(-1)

    with open(args.rfile) as f:
        dataset = json.load(f)

    flag, d = main(dataset)

    if flag==1:
        print "Result is dealer"
    elif flag==0:
        print "Result is quality products"

    for _d in d:
        print d
