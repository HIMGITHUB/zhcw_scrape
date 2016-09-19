#encoding:utf-8
from scrapy.http import Request,Response,HtmlResponse,FormRequest
import scrapy
import zhcw_scrape.settings
from ghost import Ghost
class WebkitDownloader(object):
    def process_request(self,request,spider):
        if spider.name in zhcw_scrape.settings.WEBKIT_DOWNLOADER:
            if(type(request) is not FormRequest):
                # print request.meta
                if request.meta.has_key('flag') and request.meta['flag'] == 1:
                    # print '111' + request.url
                    ghost = Ghost()
                    session = ghost.start()
                    session.evaluate('window.localStorage=undefined')
                    session.evaluate('window.sessionStorage=undefined')
                    session.evaluate('window.RTCPeerConnection=undefined')
                    session.evaluate('window.webkitRTCPeerConnection=undefined')
                    session.evaluate('window.mozRTCPeerConnection=undefined')
                    try:
                        session.open(request.url)
                    except:
                        pass
                    session.page = None
                    result, resource = session.evaluate('document.documentElement.innerHTML')

                    """
                    保留会话到爬虫，用以在爬虫里面执行js代码
                    """
                    # print result
                    spider.webkit_session = session
                    renderedBody = result.encode('utf8')
                    """
                    #返回rendereBody就是执行了js后的页面
                    """
                # print request.url
                    return HtmlResponse(request.url, body=renderedBody)
                return None
