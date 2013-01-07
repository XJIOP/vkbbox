# -*- coding: utf-8 -*-

import urllib2, mc

try:
    import json
except ImportError:
    import simplejson as json

from vkauth import VKAppAuth
vkaa = VKAppAuth()

# config vk auth
app_id = 3341857
scope = ['video', 'audio', 'offline']

# link for authorize app on vk.com
# https://oauth.vk.com/oauth/authorize?client_id=3341857&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&scope=65560&dif=0
# http://goo.gl/cVlp0

# get search result
def getSearch(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link = response.read()
    return link

# get access token
def getAccess():

    config = mc.GetApp().GetLocalConfig()
    uEmail = config.GetValue("uEmail")
    uPassword = config.GetValue("uPassword")    
    uToken = config.GetValue("VKaceess")

    if uToken:
        current = json.loads(uToken)
    elif len(uEmail) and len(uPassword):
        current = vkaa.auth(uEmail, uPassword, app_id, scope)
        if current != "authorize":
            config.SetValue("VKaceess", json.dumps(current))
            mc.LogInfo("VKaceess:"+str(current))
    else:
        current = "config"
  
    return current
