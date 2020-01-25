#! /bin/sh
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2018-2020, Sven Eckelmann <sven@narfation.org>

set -e

curl -s https://mapdata.freifunk-vogtland.net/meshviewer.json -o meshviewer.json
./site-merge-detect.py meshviewer.json || {
    cp meshviewer.json "meshviewer_$(date '+%s').json"
}
