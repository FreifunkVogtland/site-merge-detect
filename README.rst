=================
Site Merge Detect
=================

Gluon nodes using different sites (and domains) are usually expected to have no
direct links between each other. Also only a limited number of sites (and
domains) are expected to be managed in by the same servers.

site-merge-detect will now search the yanic meshviewer json for unexpected
site codes and warn about links between nodes with different site codes.

The allowed site codes have to be written to whitelisted_sites.json. It must
contain an array list of strings. An empty error automatically allows all site
codes. An example can be found in ``whitelisted_sites.example.json``

The meshviewer.json has to be downloaded manually and given to the script::

  curl -s https://mapdata.freifunk-vogtland.net/meshviewer.json -o meshviewer.json
  ./site-merge-detect.py meshviewer.json

Both commands will be started automaticall when calling::

  ./check.sh

The error log is shown as human readable text::

  Nodes with invalid domain found
  ===============================
  
   * ac86740037e0 (ffv_foobar)
  
  Links with different domain found
  =================================
  
   * ac867400ec00 (ffv) <--(wifi)--> f4f26dc1faea (ffv_pl)
  
To check the meshviewer.json for that node grep in the output of jq, for example

  jq . <meshviewer.json |grep ac86740037e0 -B16 -A27
