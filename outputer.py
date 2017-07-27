#encoding=utf-8
'''
Created on 2017年5月31日

@author: Administrator
'''
from pip._vendor.pyparsing import basestring


class Outputer(object):
    
    def __init__(self):
        self.data = []
    
    def append(self, data):
        if data is None:
            return
        self.data.append(data)

    
    def get_data_count(self):
        return len(self.data)

    
    def output(self):
        with open('index.html', 'w') as f:
            f.write('<html>')
            f.write('<body>')
            f.write('<table>')
            f.write('<tr>')
            f.write('<th>片名</th><th>译名</th><th>年代</th><th>语言</th><th>类型</th><th>国家</th><th>简介</th><th>下载网址</th>')
            f.write('<tr>')
            for item in self.data:
                f.write('<tr>')
                f.write('<td>'+ item.get('name', '') +'</td>')
                f.write('<td>'+item.get('alias', '')+'</td>')
                f.write('<td>'+item.get('year', '')+'</td>')
                f.write('<td>'+ item.get('language', '') +'</td>')
                f.write('<td>' + item.get('type', '')+'</td>')
                f.write('<td>'+item.get('country', '') + '</td>')
                f.write('<td>'+ item.get('summary', '') +'</td>')
                f.write('<td>'+item.get('url', '')+'</td>')
                '''
                f.write('<td>')
                if 'downloadUrl' in item.keys():
                    for path in item['downloadUrl']:
                        if isinstance(path, basestring):
                            f.write(path+'<br>')
                        else:
                            f.write(path['url'] + ' 密码：' + path['pwd'] +'<br>')
                f.write('</td>')
                '''
                f.write('<tr>')
                pass
            f.write('<table>')
            f.write('</body>')
            f.write('</html>')
    
    
    
    
    
                



