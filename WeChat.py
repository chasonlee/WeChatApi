#!/usr/bin/python
# coding: utf-8
__author__ = 'Chason'

import urllib2
import json
import sys

class WeChat:
    def __init__(self,
                 user = '', # User Name
                 corpid='',   # CorpID
                 corpsecret=''  # CorpSecret
                ):
        self.user = user
        self.corpid = corpid
        self.corpsecret = corpsecret

        # if you wanna send Chinese messages, keep it.
        reload(sys)
        sys.setdefaultencoding("utf-8")

    def gettoken(self, corpid, corpsecret):
        gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
        try:
            token_file = urllib2.urlopen(gettoken_url)
        except urllib2.HTTPError as e:
            print e.code
            print e.read().decode("utf8")
            sys.exit()

        token_data = token_file.read().decode('utf-8')
        token_json = json.loads(token_data)

        try:
            token = token_json['access_token']
        except:
            # traceback.print_exc()
            print token_json
            print 'Get Token Error.'
            token = None
        return token


    def senddata(self, access_token, user, content):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        send_values = {
            "touser": user,
            "toparty": "1",
            "msgtype": "text",
            "agentid": "1",
            "text": {
                "content": content
            },
            "safe": "0"
        }
        send_data = json.dumps(send_values, ensure_ascii=False)
        send_request = urllib2.Request(send_url, send_data)
        response = json.loads(urllib2.urlopen(send_request).read())
        print 'response: ' + str(response)

    def SendMessage(self, message):
        accesstoken = self.gettoken(self.corpid, self.corpsecret)
        if accesstoken != None:
            self.senddata(accesstoken, self.user, message.encode('utf-8'))
            print 'Message Send Successful!'
