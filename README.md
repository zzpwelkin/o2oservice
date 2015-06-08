### 

经过前期的分析后，决定还是直接用RDF方式保存商品信息并通过语义网络的知识架构管理和查询比较合理。
这样决定的主要原因是考虑到所属不同类别的商品本身存在属性上的差异(如菜和饮料包含的信息内容不同，
而如果用结构化方法存储，会比较麻烦)

要实现的系统中，每一个类商品都有两大类属性，一是每类商品特有的属性，一类是与服务质量相关的属性。
与服务质量相关的属性相对比较统一。

### 相关商品本体(ontology)定义参考

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

#### Exampled 
**食品类RDF定义例子**

1. Trutle

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

####  服务质量属性本体定义参考

### ETL过程描述

1. 信息获取(E)
通过爬虫从各类相关网站上爬取下来商家和商品的信息并暂村到mongodb数据库中。

商家信息: 名称，地理位置，logo， 营业时间，商家类型，联系电话，配送费用，最低消费等
菜系(商品)信息: 名称，图片，价格，材料，口味等
饮料(商品)信息: 名称，图片，价格等

2. 信息处理并入库(TL)
处理保存在monbodb中的商家和商品信息转换成对应本体的RDF格式并保存到RDF数据库(e.g.Callimachus)中(或者也可以保存到本地的文本文件中).

### 原始数据向rdf数据转换策略

1. rule方式
    * 流程: doc -> <<rule>> -> ttl.
    * 制定具有灵活性且比较简便的转换规则很重要. 

2. pythonic方式
    * 流程: owl shcema -> <<pythonic>> -> 编程转换
    * 对所有OWL模式产生对应的python类或数据类型。这样用python方式处理起来很灵活，但需要实现可用的shcema到pythoc语言的转换框架。
    * 调研后发现一下两个工具可以使用: [OntoSPy](https://github.com/lambdamusic/OntoSPy), [generageDS](http://pythonhosted.org/generateDS/) .

3. html方式
    * 流程: raw data -> simple html -> <<xslt>> -> [rdfa](http://www.w3.org/TR/rdfa-primer/#bib-rdfa-core)(rdf/xml) -> turtle
    * 方法比较简单, xslt也提供了丰富的功能但需要认真学习

#### HTML方式数据转换说明


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
