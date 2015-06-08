<?xml version="1.0" encoding="utf8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- set encode of output -->
    <xsl:output encoding="utf8" method="html" indent="yes"/>

    <xsl:template match="/div">
        <xsl:variable name="dish_pre" select="'http://example.com/localdish/'" />
        <xsl:variable name="dealer_pre" select="'http://example.com/dealer/'" />
        <html xmlns="http://www.w3.org/1999/xhtml"  prefix="lcdsh:http://example.com/localdish/
            lcdl:http://example.com/localdealer/
            gr:http://purl.org/goodrelations/v1# 
            food:http://data.lirmm.fr/ontologies/food# 
            xsd:http://www.w3.org/2001/XMLSchema#">
            <head></head>
            <body>
                <div id="dishs">
                    <!--xsl:for-each select="descendant::div[@property='dists']/ul/li"-->
                        <xsl:for-each select="descendant::div[@property='foods']/descendant::ul/li/div">
                            <div typeof="gr:ProductOrService http://data.lirmm.fr/ontologies/food#Dish">
                                <xsl:attribute name="about">
                                    <xsl:value-of select="concat($dish_pre,div[@property='id']/text())"/>
                                </xsl:attribute>
                                <div property="gr:name"><xsl:value-of select="div[@property='name']/text()"/></div>
                                <xsl:if test="div[@property='image']">
                                    <a property="gr:logo">
                                        <xsl:attribute name="href">
                                            <xsl:value-of select="div[@property='image']/@src"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="div[@property='image']/@src"/>
                                    </a>
                                </xsl:if>
                                <div property="http://data.lirmm.fr/ontologies/food#ingredientListAsText" lang="zh-cn"><xsl:value-of select="h5"/></div> </div>
                        </xsl:for-each>
                    <!--/xsl:for-each-->
                </div>

                <!-- dealer -->
                <div typeof="gr:BusinessEntity">
                    <xsl:attribute name="about">
                        <xsl:value-of select="concat($dealer_pre,div[@property='name_for_url']/text())"/>
                    </xsl:attribute>
                    <div property="gr:name" lang="zh-cn"><xsl:value-of select="div[@property='name']/text()"/></div>

                    <!-- offder dists -->
                    <div property="gr:offers" typeof="gr:Offers">
                        <ul>
                            <xsl:for-each select="descendant::div[@property='foods']/descendant::ul/li/div">
                                <li property="gr:includes">
                                    <xsl:attribute name="resource">
                                        <xsl:value-of select="concat($dish_pre,div[@property='id']/text())"/>
                                    </xsl:attribute>
                                </li>
                            </xsl:for-each>
                        </ul>
                    </div>

                    <!-- location of dealer -->
                    <div property="gr:hasPos" typeof="gr:Location">
                        <div property="schema:address" typeof="schema:PostalAddress">
                            <div property="schema:streetAddress">
                                    <xsl:value-of select="div[@property='address']/text()"/>
                            </div>
                            <div property="schema:postalCode">
                                    <xsl:value-of select="div[@property='postalcode']/text()"/>
                            </div>
                            <div property="schema:addressLocality">
                                    <xsl:value-of select="div[@property='city']/text()"/>
                            </div>
                        </div>
                        <div property="schema:latitude">
                                <xsl:value-of select="div[@property='latitude']/text()"/>
                        </div>
                        <div property="schema:longitude">
                                <xsl:value-of select="div[@property='longitude']/text()"/>
                        </div>
                        <xsl:for-each select="div[@property='opening_hours']/ul/li">
                            <div property="gr:hasOpeningHoursSpecificaton" typeof="gr:OpeningHoursSpecification">
                                <div property="gr:opens" datatype="xsd:time">
                                    <xsl:variable name="optime" select="substring-before(text(),'/')"/>
                                    <xsl:choose>
                                        <xsl:when test="contains($optime,'-:-:-')">
                                            <xsl:value-of select="$optime"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select="concat($optime,':00')"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </div>
                                <div property="gr:closed" datatype="xsd:time">
                                    <xsl:variable name="cltime" select="substring-before(text(),'/')"/>
                                    <xsl:choose>
                                        <xsl:when test="contains($cltime,'-:-:-')">
                                            <xsl:value-of select="$cltime"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select="concat($cltime,':00')"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </div>
                            </div>
                        </xsl:for-each>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
