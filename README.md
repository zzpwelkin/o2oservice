# o2o语义服务实现
蝇虫小智，藏之如宝。人如透竹，清风冽泉,无碍无得。

当前生活中各各行业互联网服务林起，每一领域都是杀声一片，竞争云起，妄自称霸，造成资源极度浪费。我欲用
语义网络之技术扫除各家门前血，拯江湖于宁静，各得所乐，虽有如下之工作。

当前虽说已是信息爆炸时代，大数据概念深入人心，但传统公司数据，国家数据，以及所谓的互联网公司(无有而说有着太多)等都还是以自己的一套方式和结构(或接口)
向外发布数据，信息孤岛状况仍然很严重。虽然互联网之父早于多年前就提出语义网络的概念，但由于缺乏实践的证明(中国人喜欢吃别人咀嚼后的饭食)，
迄今在中国还没见到向这方面深入研究和应用的公司或组织(也可能是个人圈子之狭小，没接触到)。现在每日隐约感到时不待我，潜心学习和应用他人之结晶，
只望建孤岛之桥梁，通衢大道。

## 系统概要描述

主要的工作重点:

    1. 数据转换和存储 

    2. 语义分析及推理

    3. 第三方下订单或支付接口使用

### 数据获取、转换及存储

经过前期的分析后，决定还是直接用RDF方式保存商品信息并通过语义网络的知识架构管理和查询比较合理。
这样决定的主要原因是考虑到所属不同类别的商品本身存在属性上的差异(如菜和饮料包含的信息内容不同，
而如果用结构化方法存储，会比较麻烦)

要实现的系统中，每一个类商品都有两大类属性，一是每类商品特有的属性，一类是与服务质量相关的属性。
与服务质量相关的属性相对比较统一。

#### 相关商品本体(ontology)定义参考

* 基本本体定义列表 

    [rdfs](http://www.w3.org/2000/01/rdf-schema#) A vocabulary for structuring RDF resources. 

    [rdf](http://www.w3.org/1999/02/22-rdf-syntax-ns#)  

    [owl](http://www.w3.org/2002/07/owl#) 

    [xsd](http://www.w3.org/2001/XMLSchema#) 

    [foaf](http://xmlns.com/foaf/0.1/) A vocabulary for linking people and information about them. 

    [schema.org](http://schema.org/) 

    [skos](http://www.w3.org/2004/02/skos/) A vocabulary for organizing knowledge contained in thesauri, classification schemes, subject heading lists and taxonomies. 
    
    [sioc](http://rdfs.org/sioc/spec/) A vocabulary for linking online communities. 

    [geonames](http://www.geonames.org/) A vocabulary with the official geographical names for all countries and containing over eight million placenames. 

* 商业主要本体定义列表 

    [goodrelations](http://www.heppnetz.de/ontologies/goodrelations/v1) A vocabulary for describing products and services. 

    [Vcard](http://www.w3.org/TR/vcard-rdf/) A vocabulary for the type of information that might be found on a business card. 

* 与食物(foods)相关的本体定义和描述网站

    [food_ontology](http://data.lirmm.fr/ontologies/food) 

    [food-ontology](http://www.dataversity.net/tag/food-ontology/) 

    [Food Ontology simple](http://fruct.org/publications/abstract13/files/Kol.pdf) 

##### Exampled 
**食品类RDF定义例子**

1. Turtle

```
@prefix food:<http://data.lirmm.fr/ontologies/#>
@prefix gr:<http://purl.org/goodrelations/v1#>
@prefix s:<http://http://schema.org/address>
foo:xcr a gr:ProductOrService, food:Dist;
    gr:name "小炒肉"@zh-cn;
    gr:category "中餐/炒菜/农家菜"^^xsd:string;
    gr:logo "http://example.com/1.png",
    food:ingredientListAsText "猪肉,青椒"@zh-cn.

foo:jyjr a gr:BusinessEntity
    gr:name "聚缘家人"@zh-cn;
    gr:hasPos [a gr:Location;
                 s:address [ a s:PostalAddress;
                             s:streetAddress "定淮门2号";
                             s:postalCode "210012";
                             s:addressLocality "南京, 江苏"];
                 s:latitude 37.2342;
                 s:longitude 138.349840;
                 gr:hasOpeningHoursSpecification [
                    a gr:OpeningHoursSpecification;
                    gr:opens "08:00:00"^^xsd:time;
                    gr:closes "20:00:00"^^xsd:time;
                    gr:hasOpeningHoursDayOfWeek gr:Monday, gr:Tuesday, gr:Wednesday, gr:Thursday, gr:Friday].
                 ];
    gr:offers [ a gr:Offers;
                gr:includes foo:xcr].
    
```

2. RDFa 

```
<html xmlns="http://www.w3.org/1999/xhtml" prefix="s:http://http://schema.org/ gr:http://purl.org/goodrelations/v1# food:http://data.lirmm.fr/ontologies/# xsd:http://www.w3.org/2001/XMLSchema#">
<head></head>
<body>
    <!-- dists -->
    <div id="dists">
        <div typeof="gr:ProductOrService food:Dist" about="#xcr">
            <div property="gr:name">小炒肉</div>
            <a property="gr:logo" @href="http::/example.com/1.png">logo</a>
            <div property="food:imgredientListAsText" lang="zh-cn">猪肉,青椒</div>
        </div>
        <div typeof="gr:ProductOrService food:Dist" about="#fqjd">
            <div property="gr:name">番茄鸡蛋</div>
            <a property="gr:logo" @href="http::/example.com/2.png">logo</a>
            <div property="food:imgredientListAsText" lang="zh-cn">鸡蛋, 西红柿</div>
        </div>
    </div>

    <!-- dealer -->
    <div typeof="gr:BusinessEntity" about="#jyjr">
        <div property="gr:name" lang="zh-cn">聚缘家人</div>

        <!-- offder dists -->
        <div property="gr:offers" typeof="gr:Offers">
            <ul property="gr:includes"><li rel="#xcr #fqjd"></li></ul>
        </div>

        <!-- location of dealer -->
        <div property="gr:hasPos" typeof="gr:Location">
            <div property="s:address" typeof="s:PostalAddress">
                <div property="s:streetAddress">定淮门2号</div>
                <div property="s:postalCode">210012</div>
                <div property="s:addressLocality">南京, 江苏</div>
            </div>
            <div property="s:latitude">37.2342</div>
            <div property="s:longitude">138.2342</div>
            <div property="gr:hasOpeningHoursSpecificaton" typeof="gr:OpeningHoursSpecification">
                <div property="gr:opens" datatype="xsd:time">08:00:00</div>
                <div property="gr:closed" datatype="xsd:time">20:00:00</div>
                <div property="gr:hasOpeningHoursDayOfWeek">
                    <ul><li rel="gr:Monday">Monday</li><li rel="gr:Tuesday">Tuesday</li></ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

#####  服务质量属性本体定义参考

#### ETL过程描述

1. 信息获取(E)

通过爬虫从各类相关网站上爬取下来商家和商品的信息并暂村到mongodb数据库中。 
```
商家信息: 名称，地理位置，logo， 营业时间，商家类型，联系电话，配送费用，最低消费等
菜系(商品)信息: 名称，图片，价格，材料，口味等
饮料(商品)信息: 名称，图片，价格等
```
2. 信息处理并入库(TL)

处理保存在monbodb中的商家和商品信息转换成对应本体的RDF格式并保存到RDF数据库(e.g.Callimachus)中(或者也可以保存到本地的文本文件中).

#### 原始数据向rdf数据转换策略

1. rule方式
    * 流程: doc -> [[rule]] -> ttl.
    * 制定具有灵活性且比较简便的转换规则很重要. 

2. pythonic方式
    * 流程: owl shcema -> [[pythonic]] -> 编程转换
    * 对所有OWL模式产生对应的python类或数据类型。这样用python方式处理起来很灵活，但需要实现可用的shcema到pythoc语言的转换框架。
    * 调研后发现一下两个工具可以使用: [OntoSPy](https://github.com/lambdamusic/OntoSPy), [generageDS](http://pythonhosted.org/generateDS/) .

3. html方式
    * 流程: raw data -> simple html -> [[xslt]] -> [rdfa](http://www.w3.org/TR/rdfa-primer/#bib-rdfa-core)(rdf/xml) -> turtle
    * 方法比较简单, xslt也提供了丰富的功能但需要认真学习

#### HTML方式数据转换说明

### 语义数据分析和应用

#### 请求文本分析

自然语言方式服务的请求中一般包括三类语义信息:

    1. 具体购买的商品或服务(如: 来2份盖浇饭和一瓶可乐) 
    
    2. 对商品或服务的额外要求(如: 盖浇饭放点辣椒) 

    3. 服务质量要求(如: 要求12点以前送到) 

也即用户自然分析后的基本结构形式为: 

```
requests := products [services_QA]

products := (prodmain [prodextra]|products)
prodmain := name [category] number [dealer]
prodetra := list<text>

services_QA := [time_cond|price_cond|service_QA]
time_cond := 送货上门时间
price_cond := 商品价格
```

对应一个简单json实例:
```
{
    products:{
        '盖浇饭':
            {
                'number': 2
                'extra': ['多放点辣椒','多加点米']
            },
        '可乐':
            {
                'number': 1,
                'extra': ['冰的'],
                'unit': '听'
            }
    },
    serviceQA:{
        'time_cond':"12:00:00"
    }
}
```

*Note:* w3c语音小组已定义了一些列标准方便web上语音的使用。其中[SISR(Sematic interpretion for speech recognition)标准](http://www.w3.org/TR/semantic-interpretation/)定义了解析规则，并参考其[例子](http://www.w3.org/TR/semantic-interpretation/#SI8)已大有可用之出。

#### 文本分析结果处理
有用户请求后的文本分析结果后，既可以从数据库中查询商品/服务和其他信息。从生活和查询结果来看，用户的请求有准确请求(quality data)和模糊请求(confuse data)两类。准确请求即用户详细的指定了购买的商品(如西红柿鸡蛋盖浇饭， 一听可乐)，模糊的请求即用户只指定了某一类商品/服务(如盖浇饭). 

如果数据库中组织和录入细度合理，对于quality data, 算法可以准确的确定用户想购买的商品/服务。 

基于简单原则，当前确定如下基于data的查询原则.

**查询的基本原则:**

    1. quality data请求的商品/服务尽可能由一个商家提供;

    2. confuse data请求则返回包括的具体的商品/服务.

graph图数据库sparql查询示例:
```
1. 查询同时提供鸡蛋炒饭和可乐的商家

prefix gr:<http://purl.org/goodrelations/v1#>
select distinck ?s
where
{
{
select ?s ?dlname where {?s a gr:BusinessEntity;gr:name ?dlname; gr:offers[gr:includes ?dsh]. ?dsh gr:name ?dshname. 
FILTER  regex(?dshname, "鸡蛋炒饭") .}
}
{
select ?s ?dlname where {?s a gr:BusinessEntity;gr:name ?dlname; gr:offers[gr:includes ?dsh]. ?dsh gr:name ?dshname.
FILTER  regex(?dshname, "可乐") .}
}
}

2. confuse data 查询具体的商品(如confuse data中只有 "盖浇饭" 关键字)
select distinct ?dsh ?dshname where { ?dsh gr:name ?dshname. FILTER  regex(?dshname, "盖浇饭") .}

```

### APPENDIX

#### 标准
[rdf 中文](http://zh.transwiki.org/cn/rdfprimer.htm) 

[rdfa primer](http://www.w3.org/TR/rdfa-primer/) 

[rdfa core](http://www.w3.org/TR/rdfa-core/) 

[xPath and xQuery](http://www.w3.org/TR/xpath-functions-30/) 

[rdfa 预定义的URI前缀列表](http://www.w3.org/2011/rdfa-context/rdfa-1.1) 

#### 标准学习辅助材料
[w3school xslt](http://www.w3school.com.cn/xsl/index.asp) 

#### 其他工具
[json 在线格式化工具](http://www.bejson.com/) 

[rdflib 与rdf相关的python库](https://github.com/RDFLib/rdflib) 

[callimachus](http://callimachusproject.org/) 

[allegrograph rdf图数据库](http://franz.com/agraph/allegrograph/) 

[基于allegrograph数据库的triple-data可视化工具Gruff](http://franz.com/agraph/gruff/) 

#### 相关工作人员网站
[Michele Pasin](http://www.michelepasin.org/) 
