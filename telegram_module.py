# -*- coding: utf-8 -*-

import requests
import threading
import json


class Telegram:
    def __init__(self):
        with open('../config.json') as json_file:
            json_data = json.load(json_file)
            self.token = json_data['token']
            self.id = json_data['telegram_id']

    def post(self, con):
        requests.post(con)

    def sendTelegramPush(self, *msgs):
        if self.token == '' or self.id == '':
            return

        msg = ''
        for i in range(len(msgs)):
            msg += str(msgs[i]) + '\n'

        contents = 'https://api.telegram.org/bot%s/sendmessage?chat_id=%s&text=%s' % (self.token, self.id, msg)

        t = threading.Thread(target=self.post, args=(contents,))
        t.daemon = True
        t.start()

        return t
