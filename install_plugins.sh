#!/bin/bash
File="plugins.txt"
Lines=$(cat $File)
for Line in $Lines
do
    arrIN=($(echo $Line | sed 's/==/\n/g' ))
    url=https://plugins.qgis.org/plugins/${arrIN[0]}/version/${arrIN[1]}/download/
    curl $url --output ${arrIN[0]}.zip
    unzip ${arrIN[0]}.zip -d /usr/share/qgis/python/plugins
    rm ${arrIN[0]}.zip
done