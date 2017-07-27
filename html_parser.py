#encoding=utf-8
'''
Created on 2017年5月31日

@author: Administrator
'''
from bs4 import BeautifulSoup
import urllib.request
import re

class HtmlParser(object):
    
    
    def _get_all_urls(self, url, soup):
        new_urls = set()
        links_node = soup.find_all('a')
        for link in links_node:
            new_urls.add(urllib.request.urljoin(url, link['href']))
        return new_urls
    
    def _get_data(self, url, soup):
        new_data = set()
        links_node = soup.find_all('img', alt=re.compile(r'^.*(图片).*$'))
        for link in links_node:
            src = urllib.request.urljoin(url, link['src'])
            new_data.add(src)
        return new_data
    
    '''
            获取url
    格式：http://www.6vhao.com/dy/2017-06-01/BJHJDQR.html
    '''
    def _get_all_urls_6vhao(self, url, soup):
        new_urls = set()
        links_node = soup.find_all('a')
        for link in links_node:
            new_url = urllib.request.urljoin(url, link['href'])
            pattern = re.compile(r'http://www.6vhao.com/(.*?)/\d{4}-\d{2}-\d{2}/(\w*).html')
            if pattern.match(new_url):
                new_urls.add(new_url)
        return new_urls   
    
    def _get_all_urls_pp63(self, url, soup):
        new_urls = set()
        links_node = soup.find_all('a')
        for link in links_node:
            new_url = urllib.request.urljoin(url, link['href'])
            pattern = re.compile(r'http://www.pp63.com/(.*?)/\d{4}-\d{2}-\d{2}/(\w*).html')
            if pattern.match(new_url):
                new_urls.add(new_url)
        return new_urls
    
    def _get_data_core(self, cont, keyword):
        try:
            m = re.compile(r'(?<='+ keyword +r')　(?P<sign>.*?)').search(cont)
            if m:
                return m.groupdict()['sign'].strip()
            else:
                m = re.compile(r'(?<='+ keyword[0] + '　　' + keyword[1] +r')　(?P<sign>.*?)<br />').search(cont)
                if m:
                    return m.groupdict()['sign'].strip()
                else:
                    m = re.compile(r'(?<='+ keyword[0] + '    ' + keyword[1] +r')　(?P<sign>.*?)<br />').search(cont)
                    if m:
                        return m.groupdict()['sign'].strip()
                    else:
                        m = re.compile(r'(?<=\['+ keyword[0] + ' ' + keyword[1] +r'\])　(?P<sign>.*?)<br />').search(cont)
                        if m:
                            return m.groupdict()['sign'].strip()
        except:
            pass
        return
    
    def _get_data_movie(self, url, soup, cont):
        new_data = {}
        node = soup.find('meta', attrs={'name':'description'})
        if not node is None:
            value = self._get_data_core(node['content'], '片名')
            if value:
                new_data['name'] = value
            
            value = self._get_data_core(node['content'], '译名')
            if value:
                new_data['alias'] = value
                
            value = self._get_data_core(node['content'], '年代')
            if value:
                new_data['year'] = value
            #类　　别/语　　言/国　　家
            value = self._get_data_core(node['content'], '类型')
            if value:
                new_data['type'] = value
            value = self._get_data_core(node['content'], '语言')
            if value:
                new_data['language'] = value
            value = self._get_data_core(node['content'], '国家')
            if value:
                new_data['country'] = value
            '''
            <p>◎简　　介　</p>
<p>　　影片发生在不远的未来，地球气候已经不适合粮食生长，水资源枯竭，饥荒肆掠，人类面临着灭绝的威胁。这时科学家们发现了一个<a href="http://www.6vhao.com/s/shenmi/" target="_blank"  title="神秘片">神秘</a>的&ldquo;时空裂口&rdquo;，通过它可以到外太空寻找延续生命希望的机会。一个探险小组穿越到太阳系之外，他们的目标是找到一颗适合人类移民的星球。在这艘名叫做&ldquo;Endurance&rdquo;的飞船上，探险队员着面临着前所未有，人类思想前所未及的巨大挑战。然而，通过虫洞的时候，他们发现飞船上的一个小时相当于地球上的七年时间，即使探险小组的任务能够完成，他们能提供的救赎对于对地球上活着的人来说已经是太晚。飞行员库珀(马修&middot;麦康纳 饰演)必须在与自己的儿女重逢以及拯救人类的未来之间做出抉择。</p>
            '''
            value = self._get_data_core(node['content'], '简介')
            if value:
                new_data['summary'] = value
            else:
                try:
                    m = re.compile(r'<p>◎简　　介 ?　?</p>\s*<p>　*(?P<sign>[\s|\S]*?)</p>').search(cont)
                    if m:
                        new_data['summary'] = m.groupdict()['sign'].strip()
                        pass
                except:
                    pass
                
            # 获取下载链接
            #<table border="0" cellspacing="1" cellpadding="10" width="100%" bgcolor="#0099cc">
            '''
            <a target="_blank" href=""></a> 密码: kj2b</td>
            <a target="_blank" href=""></a> 密码：tvi6</td>
            '''
            if new_data:
                table = soup.find('table', attrs={'border': '0', 'cellspacing': '1', 'cellpadding': '10', 
                                              'width': '100%', 'bgcolor':'#0099cc'})
    
                downloadUrl_tmp = []
                downloadUrl = []
                links_node = table.find_all('a')
                for link_node in links_node:
                    downloadUrl.append(link_node['href'])
                for path in downloadUrl:
                    if path.find('http://pan.baidu.com') != -1:
                        m = re.compile(r'<a target="_blank" href="'+ path + r'">'
                                   + path + r'</a> 密码[：|:] ?(?P<sign>\w*?)</td>').search(cont)
                        if m:
                            downloadUrl_tmp.append({'url': path, 'pwd': m.groupdict()['sign']})
                        else:
                            downloadUrl_tmp.append(path)
                    else:
                        downloadUrl_tmp.append(path)
                if len(downloadUrl_tmp) !=0:
                    new_data['downloadUrl'] = downloadUrl_tmp
                
        if new_data:
            new_data['url'] = url
            return new_data
        return
         
         
    def parse(self, url, cont):
        #soup = BeautifulSoup(cont, 'html.parser', from_encoding='utf-8')
        #new_urls = self._get_all_urls(url, soup)
        #new_data = self._get_data(url, soup)
        soup = BeautifulSoup(cont, 'html.parser', from_encoding='gbk')
        new_urls = self._get_all_urls_pp63(url, soup)
        new_data = self._get_data_movie(url, soup, cont.decode('gbk'))
        return new_urls, new_data
    



