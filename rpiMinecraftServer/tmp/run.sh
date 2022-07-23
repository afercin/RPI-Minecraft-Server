#!/bin/bash

source /etc/productConf/mc.conf 2> /dev/null

forgeFile="forge-${ForgeVersion}.jar"
java -Xmx${MaxRAM} -Xms${MinRAM} ${AditionalArgs} -jar ${forgeFile} "$@"