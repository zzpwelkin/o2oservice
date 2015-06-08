#!/usr/bin/env python
#-*- encoding:utf8 -*-
from lxml import etree
import pymongo
con = pymongo.connection.MongoClient()

def docs(db, col, num=None):
    num_count = 0
    collec = con[db][col]
    for doc in collec.find({}, {'_id':0}):
        if num:
            if num_count<num:
                num_count += 1
            else:
                return
        
        yield doc


if __name__ == "__main__":
    import importlib
    import json
    import optparse
    import os
    import sys
    from rdflib.plugins.parsers import pyRdfa
    import tempfile
    usage = "%prog [OPTIONS]"
    describe = u" the parameters is data_source rawdata_to_html xsdt output repectively.\
            Example: ./convert.py -d o2o -c ele_dealer -m json2html.py  -t ele.xsl -n 2 -o test.ttl -v"
    parser = optparse.OptionParser(usage=usage, description=describe)

    parser.usage = usage
    parser.add_option("-d", "--database", dest='database',)
    parser.add_option("-c", "--collection", dest='collection',)

    parser.add_option("-m", "--convert", dest='convert', help=u"json数据向html文件转换程序")
    parser.add_option("-t", "--transform", dest="transform", help=u"xslt转换文件")
    parser.add_option("-o", "--outfile", help=u"turtle 最终存储文件")

    parser.add_option("-n", "--test_num", dest="testnumber", help=u"测试的文档数.如果不设置或值为0则默认表示全部执行")

    parser.add_option("-v", "--verbose", action='store_true', dest="verbose", help=u"打印详细信息")

    args,_v = parser.parse_args()
    def verbose(x):
        if args:
            print x

    if not (args.convert and args.database and args.collection):
        parser.print_help()
        exit(-1)

    # import process module
    sys.path.append(os.path.dirname(os.path.abspath(args.convert)))
    cmdl = os.path.split(args.convert)[1]
    cmdl = cmdl.rstrip('.py')

    cmdl = importlib.import_module(cmdl)

    xslt_transform = None
    limit = 0 if not args.testnumber else int(args.testnumber)

    fobj = open(args.outfile, 'w') if args.outfile else StringIO()

    try:
        for doc in docs(args.database, args.collection, limit):
            html_doc =  cmdl.main(doc)
            verbose(html_doc)

            if not (args.transform or args.verbose):
                print html_doc
            else:
                if not xslt_transform:
                    xslt_transform = etree.XSLT(etree.XML(open(args.transform).read()))
                etree.XML(html_doc)
                rdfa_doc = str(xslt_transform(etree.XML(html_doc)))
                verbose(rdfa_doc)
                _, tmpf = tempfile.mkstemp(suffix='.html')
                with open(tmpf, 'w') as _tf:
                    _tf.write(rdfa_doc)
                ttl_doc = pyRdfa.pyRdfa().rdf_from_source(tmpf, rdfOutput=True)
                #os.remove(tmpf)
                verbose(ttl_doc)

                fobj.write(ttl_doc)
    finally:
        fobj.close()


