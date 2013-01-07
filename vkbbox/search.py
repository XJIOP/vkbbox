# -*- coding: utf-8 -*-

import vkaccess, datetime, mc, urllib, re
from vklink import getURL

try:
    import json
except ImportError:
    import simplejson as json

config = mc.GetApp().GetLocalConfig()

# other settings
uSearchQ = 1 # 0 include youtube 
uSort = 0 # 0 date # 1 duration # 2 relevante
uCount = 200 # 200 max list

# clean text for title and description
def cleanText(text):
    result = re.sub("<br>", "\n", text)
    result = re.sub("&amp;", "\n", result)
    result = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ', result)
    return result.strip()
    
# set movie gui list
def getList(data):
    itemList = mc.ListItems()
    for result in data:
        item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_CLIP)
        item.SetLabel(str(cleanText(result[0]).encode("utf-8")))
        item.SetDescription(str(cleanText(result[1]).encode("utf-8")))
        item.SetPath(str(result[2]))
        item.SetThumbnail(str(result[3]))
        item.SetDuration(int(result[4]))
        item.SetProperty("vtime", str(datetime.timedelta(seconds=int(result[4]))))
        item.SetProperty("drect", "no")
        item.SetProperty("vq", "unknown")
        itemList.append(item)
    
    return itemList   

# search and get movie to json
def searchList(VKsearch):
    
    mc.ShowDialogWait()

    if not len(config.GetValue("uEmail")) or not len(config.GetValue("uPassword")):
        mc.HideDialogWait()
        return "config"

    # check and get access_token
    current_token = vkaccess.getAccess()

    if current_token == "config" or current_token == "authorize":
        mc.HideDialogWait()
        return current_token    
    
    quality = ["240p", "360p", "480p", "720p"]
    vkQuery = "https://api.vk.com/method/video.search?q=%s&access_token=%s&user_id=%s&count=%s&hd=%s&sort=%s" % (urllib.quote(str(VKsearch)), current_token["access_token"], current_token["user_id"], uCount, uSearchQ, uSort)
    
    getVKlist = vkaccess.getSearch(vkQuery)
    in_json = json.loads(getVKlist)

    try:
        error = json.loads(getVKlist)["error"]
        mc.HideDialogWait()
        return "authorize"
       
    except:
        getVideo = []
  
        for result in in_json["response"]:
            getVideo.append([result['title'].strip(), result['description'].strip(), result['player'], result['image_medium'], result["duration"]])
        
        mc.HideDialogWait()
        return getList(getVideo)

# get direct link to play
def getLink(url):
    mc.ShowDialogWait()
    
    this = getURL(url)
    goToPlay = max(0, min(int(config.GetValue("uMaxPlayQ")), len(this)-1))
    
    mc.HideDialogWait()
    return [this[goToPlay][1], this[goToPlay][0]]    
