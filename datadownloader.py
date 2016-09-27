import urllib2
class DataDownloader:
    def downlaod(self, url):
        if url is None:
            return None
        # request_header = {'Connection': 'Keep-Alive',
        # 'Accept': 'text/html, application/xhtml+xml, */*',
        # 'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        # request_timeout = 10
        # request = urllib2.Request(url,None,request_header)
        # response = urllib2.urlopen(request,None,request_timeout)
        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()