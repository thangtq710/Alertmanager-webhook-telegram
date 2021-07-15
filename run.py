#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Thangtq710

from flask import Flask, request
from urllib.parse import unquote_plus
import json
import os
import logging
import re
import urllib
import sys
import argparse
from urllib.request import urlopen


app = Flask(__name__)
telegram_bot_token = "123456:BB1231rGZy29ILxfHrT5fyvsM5U9696"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_telegram_message(token, chat_id, text):
    url = 'https://api.telegram.org/bot%s/sendMessage' % (token)
    data = urllib.parse.urlencode({'chat_id':chat_id, 'text':text, 'parse_mode':'Markdown'}).encode("utf-8")
    try:
        urlopen(url, data, timeout=30).read()
    except Exception as e:
        sys.stdout.write('Cannot send Telegram message: HTTP-Error: %s\n' % (e))


@app.route('/', methods=['GET'])
def index():
    """
    Go to localhost:5000 to see a message
    """
    return ('OK.', 200, None)


@app.route('/notify/<user>', methods=['POST'])
def notifier(user):

### Send data on prometheus to webhook
    """
    Send a POST request to localhost:5000/notify/<user> with a JSON body with a "p" key
    to print that message in the server console.
    """
    data = request.get_json()
    print(data)
    if "Webhook setting validated" in json.dumps(data):
        return ("", 200, None)
    for alerts in data['alerts']:
        tmp = list()
        for k,v in alerts['labels'].items():
            if k in ["alertname", "alert_type", "expression", "rule_id", "prometheus", "prometheus_from", "group_id"]:
                continue
            tmp.append("%s:	%s" % (k.capitalize(),v))
        for k,v in alerts['annotations'].items():
            tmp.append("%s:	%s" % (k.capitalize(),v))
        msg = """*ADT-PROMETHEUS ALERT*: `%s`
```
%s
StartsAt:	%s
```
        """ % (alerts['status'].upper(), "\n".join(tmp), alerts['startsAt'])
        print(msg)

### Alert to telegram
    
    if not os.path.isfile('/app/user.json'):
        logger.info("File /app/user.json is not found.Check again!")
        sys.exit(2)
    else:
        with open('/app/user.json') as fh:
            list_user = json.load(fh)
    
    key_to_lookup = user
    if key_to_lookup not in list_user:
        logger.info("User not exists.")
        sys.exit(2)
    else:
        telegram_user_id = list_user[key_to_lookup]
        send_telegram_message(telegram_bot_token, telegram_user_id, msg)
    return ("", 200, None)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, use_reloader=True)
