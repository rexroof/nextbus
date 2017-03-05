#!/usr/bin/env python

import requests, yaml
import xml.etree.ElementTree as ET


def read_config():
    with open("config.yml", 'r') as stream:
        try:
            junk = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return junk

cfg = read_config()


params = {
        'key': cfg["api_key"],
        'rt' : 31,
        'dir':'LOOP',
        'stpid' : '2091',
        }

# 'key': cfg["api_key"],
# 'rt' : 31,
# 'dir':'LOOP',

# <stpid>2091</stpid>
# <stpnm>Dexter + Glenwood</stpnm>
# <lat>42.288219280658</lat>
# <lon>-83.788167084656</lon>

# http://[host:port]/bustime/api/[version]/gettime
# http://[host:port]/bustime/api/[version]/getvehicles
# http://[host:port]/bustime/api/[version]/getroutes
# http://[host:port]/bustime/api/[version]/getpatterns
# http://[host:port]/bustime/api/[version]/getpredictions
# http://[host:port]/bustime/api/[version]/getservicebulletins
# http://[host:port]/bustime/api/[version]/getlocalelist
# http://[host:port]/bustime/api/[version]/getstops
# http://[host:port]/bustime/api/[version]/getdirections


# r = requests.get("http://{}/bustime/api/v1/getvehicles".format(cfg["hostname"]), 
r = requests.get("http://{}/bustime/api/v1/getpredictions".format(cfg["hostname"]), 
        params=params)

print r.text
root = ET.fromstring(r.text)

for child in root:
    print child.tag, child.attrib
