#coding:utf-8

from bs4 import BeautifulSoup
import urlparse
import re
from collections import deque
from dataoutputer import DataOutputer
from dataparser import DataParser
from datadownloader import DataDownloader

class PoemCrawler:

    def __init__(self):
        self.downlaoder = DataDownloader()
        self.parser = DataParser()
        self.outputer = DataOutputer()

    def craw(self, page_url,type):
        html_cont = self.downlaoder.downlaod(page_url)
        soup = BeautifulSoup(html_cont,'html.parser', from_encoding = 'utf-8')
        links = []
        links = soup.find_all('a', href = re.compile(r"/view_.*"))
        new_urls = deque()
        new_datas_head = deque()
        for link in links:
            new_url = link['href']
            if not new_url.startswith('/view_'):
                new_full_url = urlparse.urljoin("http://www.gushiwen.org/", new_url)
            else:
                new_full_url = urlparse.urljoin("http://so.gushiwen.org/", new_url)
            new_urls.append(new_full_url)
            new_datas_head.append(link.find_parent().get_text())
        count = 0
        while len(new_urls)!=0:
            count += 1
            print count
            new_url = new_urls.popleft()
            new_data_head = new_datas_head.popleft()
            tauthor = u'佚名'
            ttitle = new_data_head
            if new_data_head.find('(')!=-1:
                tauthor = new_data_head.split('(')[1].strip(')')
                ttitle = new_data_head.split('(')[0]
            try:
                html_cont = self.downlaoder.downlaod(new_url)
                new_data = self.parser.parse(new_url,html_cont)
                if tauthor != u'佚名':
                    new_data['author'] = tauthor
                new_data['title'] = ttitle
                self.outputer.collect_data(new_data)
                print new_url+' '+new_data['title']+':'+new_data['author']
            except Exception as e:
                print new_url+' '+ttitle+':'+tauthor+' '+'failed'
            #if count==10:break
        self.outputer.output_html(type)

if __name__ == "__main__":
    obj_spider = PoemCrawler()
    root_url = "http://so.gushiwen.org/gushi/tangshi.aspx"
    obj_spider.craw(root_url,0)
    obj_spider.outputer.output_db(0)
    obj_spider.outputer.clear_data()
    root_url = "http://so.gushiwen.org/gushi/songsan.aspx"
    obj_spider.craw(root_url,1)
    obj_spider.outputer.output_db(1)
    obj_spider.outputer.output_db(1)
    obj_spider.outputer.clear_data()