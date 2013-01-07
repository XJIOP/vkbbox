# -*- coding: utf-8 -*-

import urlparse,urllib2,urllib,re
import os,sys

try:
    import json
except ImportError:
    import simplejson as json

def geturl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    return link

# Returns an array of possible video url's from the page_url
def getURL(page_url , quality = 3):
    data = geturl(page_url.replace("amp;",""))
    videourl = ""
    regexp = re.compile(r'vkid=([^\&]+)\&')
    match = regexp.search(data)
    vkid = ""
    
    if match is not None:
        vkid = match.group(1)

    patron  = "var video_host = '([^']+)'.*?"
    patron += "var video_uid = '([^']+)'.*?"
    patron += "var video_vtag = '([^']+)'.*?"
    patron += "var video_no_flv = ([^;]+);.*?"
    patron += "var video_max_hd = '([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)

    video_urls = []

    if len(matches)>0:    
        for match in matches:
            if match[3].strip() == "0" and match[1] != "0":
                tipo = "flv"
                if "http://" in match[0]:
                    videourl = "%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                else:
                    videourl = "http://%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                
                # Lo acade a la lista
                video_urls.append( ["FLV",videourl])

            elif match[1]== "0" and vkid != "":     #http://447.gt3.vkadre.ru/assets/videos/2638f17ddd39-75081019.vk.flv 
                tipo = "flv"
                if "http://" in match[0]:
                    videourl = "%s/assets/videos/%s%s.vk.%s" % (match[0],match[2],vkid,tipo)
                else:
                    videourl = "http://%s/assets/videos/%s%s.vk.%s" % (match[0],match[2],vkid,tipo)
                
                # Lo acade a la lista
                video_urls.append( ["FLV",videourl])
                
            else:                                   
                
                #Si la calidad elegida en el setting es HD se reproducira a 480 o 720, caso contrario solo 360, este control es por la xbox
                if match[4]=="0":
                    video_urls.append( ["240p",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                elif match[4]=="1":
                    video_urls.append( ["240p",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                elif match[4]=="2":
                    video_urls.append( ["240p",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                    video_urls.append( ["480p",get_mp4_video_link(match[0],match[1],match[2],"480.mp4")])
                elif match[4]=="3":
                    video_urls.append( ["240p",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                    video_urls.append( ["480p",get_mp4_video_link(match[0],match[1],match[2],"480.mp4")])
                    video_urls.append( ["720p",get_mp4_video_link(match[0],match[1],match[2],"720.mp4")])
                    #video_urls.append( ["1080p",get_mp4_video_link(match[0],match[1],match[2],"1080.mp4")])
                else:
                    video_urls.append( ["240p",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])

    return video_urls
    
    
def get_mp4_video_link(match0,match1,match2,tipo):
    if match0.endswith("/"):
        videourl = "%su%s/videos/%s.%s" % (match0,match1,match2,tipo)
    else:
        videourl = "%s/u%s/videos/%s.%s" % (match0,match1,match2,tipo)
    return videourl
