#!/bin/bash
SED=`which sed`
DJANGO=`which django-admin.py`
MV=`which mv`

cd /home/kitdata/www/production/tvet/tvet
workon tvet-production
$DJANGO build_solr_schema > schema.xml
$SED -i 's/stopwords_en.txt/lang\/stopwords_en.txt/' schema.xml 
$MV schema.xml /opt/solr/solr/collection1/conf/
sudo service solr restart
$DJANGO rebuild_schema
