# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhcwScrapeItem_brief(scrapy.Item):
    # define the fields for your item here like:
    """#获奖情况摘要
    """
    """#开奖日期
    """
    open_date = scrapy.Field()
    """#开奖期号
    """
    issue_no = scrapy.Field()
    """#销售总额
    """
    ticket_sold = scrapy.Field()
    """#奖池累计总额
    """
    money_still = scrapy.Field()
    """#蓝色球号码
    """
    blue_no = scrapy.Field()
    """#红球1
    """
    red1 = scrapy.Field()
    """#红球2
    """
    red2 = scrapy.Field()
    """#红球3
    """
    red3 = scrapy.Field()
    """#红球4
    """
    red4 = scrapy.Field()
    """#红球5
    """
    red5 = scrapy.Field()
    """#红球6
    """
    red6 = scrapy.Field()
    """#1等奖金额
    """
    prize1 = scrapy.Field()
    """#2等奖金额
    """
    prize2 = scrapy.Field()
    """#3等奖金额
    """
    prize3 = scrapy.Field()
    """#4等奖金额
    """
    prize4 = scrapy.Field()
    """#5等奖金额
    """
    prize5 = scrapy.Field()
    """#6等奖金额
    """
    prize6 = scrapy.Field()
    """#1等奖获奖人数
    """
    wwp1 = scrapy.Field()
    """#2等奖获奖人数
    """
    wwp2 = scrapy.Field()
    """#3等奖获奖人数
    """
    wwp3 = scrapy.Field()
    """#4等奖获奖人数
    """
    wwp4 = scrapy.Field()
    """#5等奖获奖人数
    """
    wwp5 = scrapy.Field()
    """#6等奖获奖人数
    """
    wwp6 = scrapy.Field()

    pass
class ZhcwScrapeItem_infos(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """#各省开奖情况详情
    """
    """#省名
    """
    state_name = scrapy.Field()
    """#开奖期号
    """
    issue_no = scrapy.Field()
    """#省内销售额
    """
    state_ticket_sold = scrapy.Field()
    """#1等奖省内获奖人数
    """
    state_wwp1 = scrapy.Field()
    """#2等奖省内获奖人数
    """
    state_wwp2 = scrapy.Field()
    """#3等奖省内获奖人数
    """
    state_wwp3 = scrapy.Field()
    """#4等奖省内获奖人数
    """
    state_wwp4 = scrapy.Field()
    """#5等奖省内获奖人数
    """
    state_wwp5 = scrapy.Field()
    """#6等奖省内获奖人数
    """
    state_wwp6 = scrapy.Field()
    """#幸运二等奖等奖省内获奖人数
    """
    state_luckysecond = scrapy.Field()
    pass

