#encoding=utf-8
'''
Created on 2017年5月31日

@author: Administrator
'''
from test import url_manager, html_downloader, html_parser, outputer



class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = outputer.Outputer()

    
    def crawl(self, rootUrl, countSum):
        self.urls.add_new_url(rootUrl)
        count = 1
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('crawl %d: %s'%(count, new_url))
                cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.append(new_data)
            except Exception as e:
                print('crawl failed %s'%e)
            if countSum < count:
                break
            count += 1
            #print('collect %d'%self.outputer.get_data_count())
            
        self.outputer.output()
            
if __name__ == '__main__':
    spiderMain = SpiderMain()
    rootUrl = 'http://www.pp63.com/mj/2013-09-25/21456.html'
    spiderMain.crawl(rootUrl, 100) # 10万张图片
    


