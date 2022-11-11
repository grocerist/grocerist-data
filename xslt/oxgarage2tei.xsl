<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output indent="yes"></xsl:output>
    <!-- Identity template : copy all text nodes, elements and attributes -->   
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="tei:anchor" />
    <xsl:template match="tei:front"/>
    <xsl:template match="tei:teiHeader">
        <teiHeader xmlns="http://www.tei-c.org/ns/1.0">
            <fileDesc>
                <titleStmt>
                    <title type="main">Galata Sharia Court Records 18th Century</title>
                    <title type="sub">Grocers of Istanbul: Tracing Food Consumption (GrocerIST)</title>
                    <principal><persName role="acdh:hasPrincipialInvestigator" key="https://orcid.org/0000-0002-8740-5275">Yavuz Köse</persName></principal>
                    <funder>
                        <name>FWF - Der Wissenschaftsfonds</name>
                        <address>
                            <street>Sensengasse 1</street>
                            <postCode>1090 Wien</postCode>
                            <placeName>
                                <country>A</country>
                                <settlement>Wien</settlement>
                            </placeName>
                        </address>
                    </funder>
                    <respStmt>
                        <resp>Transcription and Annotation</resp>
                        <persName role="acdh:hasCreator">Suemeyye Hosgoer Bueke</persName>
                    </respStmt>
                    <respStmt>
                        <resp>XML/TEI creation</resp>
                        <persName role="acdh:hasContributor" key="https://orcid.org/0000-0002-9575-9372">Peter Andorfer</persName>
                    </respStmt>
                </titleStmt>
                <publicationStmt>
                    <p>Publication Information</p>
                </publicationStmt>
                <sourceDesc>
                    <msDesc type="invetory">
                        <msIdentifier>
                            <institution>Name of the Archiv</institution>
                            <repository>Name of the Repository</repository>
                            <idno type="archive">Signature of Document</idno>
                        </msIdentifier>
                        
                        <history>
                            <origin notBefore="1700-01-01" notAfter="1799-12-31"/>
                        </history>
                    </msDesc>
                </sourceDesc>
            </fileDesc>
        </teiHeader>
    </xsl:template>
    
</xsl:stylesheet>