#!/usr/bin/env python
#-*- encoding:utf8 -*-

"""
后台服务主要接口
    1. QualityData 查询集合中的查询条件是否都为QualityData
    2. dealers Quality data商家查询
    3. detail 某一对象的详细信息
"""
from rdflib import Graph, plugin
from rdflib.serializer import Serializer

from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.sail.allegrographserver import AllegroGraphServer

namespaces = {
        'gr':'http://purl.org/goodrelations/v1#',
        }

def QualityData(conn, dataset):
    """
    Get quality products of this dataset and return data only that have 
        products or service more than one 

    @param conn: repository链接对象
    @param dataset: 查询的数据集.必须为Dict类型

    @return: 如果${dataset}中有Confuse data，则返回其包含的Quality data.
        返回Dict类型。
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

def Products(conn, dataset):
    """
    根据规则查询商品/服务

    @param conn: repository链接对象
    @param dataset: 查询的数据集.必须为Dict类型,且Dict中查询的数据为Quality data.

    @return: 商品列表. 其返回的格式为[D1:{P1,P2,PN}, DN:{PX,PM}].
        其中Dx表示商家, Px表示商品或服务.
    """
    resProds = []
    def _matchedDealers(pdmap):
        # 从商家集合中判断出最优的商家
        dlsSet = set()
        dlsList = []
        dlsCount = {}
        otherProdDealersSet = {}
        for v in pdmap.values():
            dlsSet = dlsSet.union(v)
            dlsList += v

        for  dl in dlsSet:
            dlsCount[dl] = dlsList.count(dl)

        maxNumDls = sorted(dlsCount.items(),cmp=lambda x,y: y-x, key=lambda x: x[1])
        dealer = maxNumDls[0][0]
        dealProd = []
        otherPDMap = {}

        for p, dls in pdmap.iteritems():
            if dealer in dls:
                dealProd.append(p)
            else:
                otherPDMap[p] = dls

        return (dealer, dealProd, otherPDMap)

    # 商家所包含的商品和商品所在的商家映射
    DealerProdsMap = {}
    ProdDealersMap = {}

    # 获取每一个组查询条件对应的商家集合
    query = u"""select distinct ?s where {{?s a gr:BusinessEntity;
                gr:offers[gr:includes ?dsh]. ?dsh gr:name "{0}".}}"""
    for k, v in dataset.iteritems():
        ds = []
        tupleQuery = conn.prepareTupleQuery(QueryLanguage.SPARQL, query.format(k))
        result = tupleQuery.evaluate()
        for r in result:
            ds.append(r.getValue('s').getValue())

        ProdDealersMap[k] = ds

    while(ProdDealersMap):
        d, prods, ProdDealersMap = _matchedDealers(ProdDealersMap)
        DealerProdsMap[d] = prods

    # 查找具体的商品/服务
    # TODO: 修改以更便捷的json格式输出, 调研JSON-LD是否可行
    dealerQuery = u"""select ?dname where {{<{0}> gr:name ?dname.}}"""
    productQuery = u"""select ?dsh ?p ?o where {{<{0}> gr:offers [gr:includes ?dsh].?dsh gr:name "{1}";?p ?o.}}"""
    dealerDesc = u"""describe <{0}> ?p ?o where {{<{0}> ?p ?o.}}"""
    prodDesc = u"""describe ?dsh ?p ?o where {{<{0}> gr:offers [gr:includes ?dsh].?dsh gr:name "{1}";?p ?o.}}"""
    g = Graph()
    tmpResStr = ""
    for d, prods in DealerProdsMap.iteritems():
        result = conn.prepareTupleQuery(QueryLanguage.SPARQL, dealerQuery.format(d)).evaluate_generic_query(accept='application/sparql-results+json')
        print result

        # describe query and get all triples of this dealer
        result = conn.prepareGraphQuery(QueryLanguage.SPARQL, dealerDesc.format(d)).evaluate()
        for r in result: print r
        result.close()

        for p in prods:
            print conn.prepareTupleQuery(QueryLanguage.SPARQL, productQuery.format(d, p)).evaluate_generic_query(accept='application/sparql-results+json')

            # describe query and get all triples of this dealer
            result = conn.prepareGraphQuery(QueryLanguage.SPARQL, prodDesc.format(d,p)).evaluate()
            for r in result: print r
            result.close()

    g.parse(data=tmpResStr, format='nt')
    return g.serialize(format='json-ld', indent=4)

    
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
        prds = QualityData(conn, data)
        if prds:
            return (0, prds)
        else:
            dl = Products(conn, data)
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
