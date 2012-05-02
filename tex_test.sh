#!/bin/bash

awk -F '"( ")?' \
 '{ if($2=="plane") pln=$3; if($2=="uaxis") system("./tex_test.py \"" pln "\""); else if($2!="vaxis") print $0 }' \
  mapsrc/superjer-card.vmf \
 >mapsrc/superjer-card-fixed.vmf
