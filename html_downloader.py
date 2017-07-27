#encoding=utf-8
'''
Created on 2017年5月31日

@author: Administrator
'''
import urllib.request


class HtmlDownloader(object):
    
    
    def download(self, url):
        if url is None:
            return
        req = urllib.request.urlopen(url, timeout=1000)
        if req.getcode() != 200:
            return
        return req.read()
    
    



