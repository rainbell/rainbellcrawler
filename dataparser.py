#coding:utf-8
from bs4 import BeautifulSoup
import re

class DataParser:

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser', from_encoding = 'utf-8')
        new_data = {}
        new_data = self._get_data(soup)
        return new_data

    def _get_data(self, soup):
        res_data = {}
        author_node = re.search(r'_.*_',soup.find('title').get_text())
        if author_node is not None:
            author_node_text = author_node.group().strip('_')
            if author_node_text.endswith(u'古诗'):
                author_node_text.startswith(u'古诗')
            res_data['author'] = author_node_text
        else:
            author_node_text = u'佚名'
        res_data['author'] = author_node_text
        title_node = soup.find('div',class_='shileft').find('div',class_='son1').find('h1')
        res_data['title'] = title_node.get_text()
        tmp = soup.find_all('meta')
        content_node = tmp[len(tmp)-1]
        res_data['content'] = content_node['content'].replace(u'　',u'').replace(u' ',u'')
        content_node = soup.find('div',class_='para')
        if content_node is not None:
            res_data['content'] = content_node.get_test()
        else:
            content_node = soup.find('div',class_='shileft').find('div',class_='son2')
            if  content_node != None:
                tstr = content_node.get_text()
                tstr = tstr.split(u'原文：')
                res_data['content'] = tstr[1].strip().replace('\n','')
        return res_data