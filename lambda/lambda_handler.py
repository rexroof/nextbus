#!/usr/bin/env python
from __future__ import print_function
import requests
import xml.etree.ElementTree as ET
import simplejson as json
import os
from dateutil import parser

api_key = os.environ.get('API_KEY')
api_host = os.environ.get('API_HOST')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def next_bus(route, stop):
    pred_url = "http://{}/bustime/api/v1/getpredictions".format(api_host)
    params = {
            'key': api_key,
            'rt': route,
            'top': 1,
            'stpid': stop,
            }
    r = requests.get(pred_url, params=params)
    root = ET.fromstring(r.text)
    next_bus = ''
    for prd in ET.fromstring(r.text).iter('prd'):
        preds = {}
        for child in prd.getchildren():
            preds[child.tag] = child.text
        now     = parser.parse(preds["tmstmp"])
        predict = parser.parse(preds["prdtm"])
        coming = ( predict - now )
        next_bus = { 'time': str(coming), 'direction': preds["rtdir"] ,
                'route': preds["rt"]}
    return next_bus

def lambda_handler(event, context):
    # print("event: {}".format(event))
    # print("context: {}".format(context))
    if event['httpMethod'] == 'GET':
        payload = event['queryStringParameters'] 
    else:
        return respond(ValueError('Unsupported method "{}"'.format(event['httpMethod'])))
    return respond(None, next_bus(payload["bus"],payload["stop"]))
