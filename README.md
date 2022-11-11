# grocerist-data
repo to store/publish data gathered in the [FWF-Project GroecrIST (P 35546)](https://pf.fwf.ac.at/en/research-in-practice/project-finder/56399)

## structured data

* structured data is gathered via dedicated [baserow-project](https://baserow.acdh-dev.oeaw.ac.at/database/275/table/1488)
* and frequently dumped via GitHub-Action into `./json_dumps`

## transcriptions

* transcriptions of source materials are done in [gdocs](https://docs.google.com/document/d/1ioQYuvjkT9sLVvLEan67mBEBWW2f_Iq0yNmvcDkGwJo/edit#) and until a better workflow (i.e. scriptable) is set up,
* exported as MS-Docs,
* converted with https://teigarage.tei-c.org/# into XML/TEI and
* stored into `./data/from_oxgarage`,
* and with `./xsl/oxgarage2tei.xsl` converted into a semantically richer XML/TEI stored at `./data/editions`
