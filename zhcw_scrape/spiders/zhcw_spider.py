#encoding:utf-8
__author__ = 'Him666'
import scrapy
import re
from lxml import etree
from zhcw_scrape.items import ZhcwScrapeItem_brief,ZhcwScrapeItem_infos
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy import FormRequest
import time
import json
from ghost import Ghost


class zhcw_scrape(CrawlSpider):

    u'''
    获取双色球相关信息
    '''

    def __init__(self):
        self.webkit_session = None
    name = "zhcw_spider"
    allowed_domains = ['zhcw.com']
    start_urls = ['http://kaijiang.zhcw.com/zhcw/html/ssq/list.html']
    base_url = 'http://kaijiang.zhcw.com'
    tail_url = '/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum='
    pagenum = 2
    # ghost = Ghost()

    def parse(self, response):

        selector = Selector(response)
        main_infos = selector.xpath('//table[@class="wqhgt"]')
        minfo = main_infos
        trs = minfo.xpath('//tr/td[@align="center"]')
        '''
        不知道为什么filter在这里不起作用。。。
        filter(self.filter_helper,trs)
        '''
        issue_nos = []
        for tr in trs:
            if self.filter_helper(tr) == True:
                issue_nos.append(tr.xpath('text()').extract()[0])

        for issue_no in issue_nos:
            json_url = "http://app.zhcw.com/wwwroot/zhcw/jsp/kjggServ.jsp?catalogId=14609&issueNo=" + issue_no + "&jsonpcallback=?"
            time.sleep(1)
            yield Request(json_url, callback=self.json_parse, meta={'issue_n' : issue_no})
        # issue_no = '2010001'
        # json_url = "http://app.zhcw.com/wwwroot/zhcw/jsp/kjggServ.jsp?catalogId=14609&issueNo=" + issue_no + "&jsonpcallback=?"
        # yield Request(json_url, callback=self.json_parse, meta={'issue_n': issue_no})

        time.sleep(2)
        if self.pagenum < 101:
            yield Request(self.base_url+self.tail_url+str(self.pagenum), callback=self.parse)
            self.pagenum += 1

    def json_parse(self, response):
        res_str = response.body_as_unicode()
        res_str = res_str.strip('?; \n\r()')
        print res_str
        json_ids = json.loads(res_str)
        iid = json_ids['id']
        url = "http://www.zhcw.com/ssq/kjgg/"+iid+".shtml"
        issue_n = response.meta['issue_n']
        if int(issue_n) >= 2015001:
            yield Request(url, callback=self.brief_js_parse_new, meta={'flag': 1})
        else:
            yield Request(url, callback=self.brief_js_parse_old, meta={'issue_n': issue_n})

    def brief_js_parse_new(self, response,):
        item = ZhcwScrapeItem_brief()
        dictt = self.webkit_session.evaluate('zj')
        dictt = dictt[0]
        item['issue_no'] = dictt['KJ_ISSUE']
        item['open_date'] = dictt['KJ_DATE']
        item['ticket_sold'] = dictt['TZ_MONEY']
        item['money_still'] = dictt['JC_MONEY']
        item['blue_no'] = dictt['KJ_T_NUM']
        rs = dictt['KJ_Z_NUM']
        rss = rs.split()
        item['red1'] = rss[0]
        item['red2'] = rss[1]
        item['red3'] = rss[2]
        item['red4'] = rss[3]
        item['red5'] = rss[4]
        item['red6'] = rss[5]

        item['prize1'] = dictt['ONE_J']
        item['prize2'] = dictt['TWO_J']
        item['prize3'] = dictt['THREE_J']
        item['prize4'] = dictt['FOUR_J']
        item['prize5'] = dictt['FIVE_J']
        item['prize6'] = dictt['SIX_J']
        item['wwp1'] = dictt['ONE_Z']
        item['wwp2'] = dictt['TWO_Z']
        item['wwp3'] = dictt['THREE_Z']
        item['wwp4'] = dictt['FOUR_Z']
        item['wwp5'] = dictt['FIVE_Z']
        item['wwp6'] = dictt['SIX_Z']
        yield item
        pass

    def brief_js_parse_old(self,response,):
        '''
        针对15年以前的页面，可以在页面里直接取值
        :param response:
        :return:
        '''
        item = ZhcwScrapeItem_brief()
        selector = Selector(response)
        item['issue_no'] = response.meta['issue_n']

        redballs = selector.xpath('//span[@class="redball_bigst"]/text()').extract()
        blueball = selector.xpath('//span[@class="blueball_bigst"]/text()').extract()

        win_scales = selector.xpath('//table[@class="result_tab"]//td/text()').extract()

        win_text = selector.xpath('//div[@class="win_text"]/text()').extract()
        ts = win_text[0]
        ts = ts.split("  ")
        pattern = re.compile(r'\d+\.?\d*')
        tickets_sold = re.findall(pattern,ts[0])
        money_still = re.findall(pattern,ts[1])
        open_date = re.findall(pattern,win_text[1])
        item['open_date'] = '/'.join(open_date)
        item['ticket_sold'] = ''.join(tickets_sold)
        item['money_still'] = ''.join(money_still)
        item['blue_no'] = blueball[0]
        item['red1'] = redballs[0]
        item['red2'] = redballs[1]
        item['red3'] = redballs[2]
        item['red4'] = redballs[3]
        item['red5'] = redballs[4]
        item['red6'] = redballs[5]
        item['prize1'] = win_scales[1]
        item['prize2'] = win_scales[3]
        item['prize3'] = win_scales[5]
        item['prize4'] = win_scales[7]
        item['prize5'] = win_scales[9]
        item['prize6'] = win_scales[11]
        item['wwp1'] = win_scales[0]
        item['wwp2'] = win_scales[2]
        item['wwp3'] = win_scales[4]
        item['wwp4'] = win_scales[6]
        item['wwp5'] = win_scales[8]
        item['wwp6'] = win_scales[10]
        yield item

    def len_selector(self, x):
        y = 0
        if x.xpath('text()').extract() != []:
            y = len(x.xpath('text()').extract()[0])
        return y

    def filter_helper(self, x):
        tmp = self.len_selector(x)
        if tmp == 7:
            return True
        return False