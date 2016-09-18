# -*- coding: utf-8 -*-
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy import log
SETTINGS = get_project_settings()

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhcwScrapePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        # Instantiate DB
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host=SETTINGS['DB_HOST'],
                                            user=SETTINGS['DB_USER'],
                                            passwd=SETTINGS['DB_PASSWD'],
                                            port=SETTINGS['DB_PORT'],
                                            db=SETTINGS['DB_DB'],
                                            charset='utf8',
                                            use_unicode=True,
                                            cursorclass=MySQLdb.cursors.DictCursor
                                            )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, tx, item):

        tx.execute("select * from main_info where issue_no = %s", (item['issue_no'],))

        result = tx.fetchone()
        print result
        if result:
            log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        else:
            result = tx.execute( \
                "insert into main_info (issue_no,open_date,ticket_sold,money_still,blue_no,red1,red2,red3,red4,\
                red5,red6,prize1,prize2,prize3,prize4,prize5,prize6,\
                wwp1,wwp2,wwp3,wwp4,wwp5,wwp6,other_message1,other_message2) "
                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (item['issue_no'],item['open_date'],item['ticket_sold'],item['money_still'],\
                 item['blue_no'],item['red1'],item['red2'],item['red3'],item['red4'],item['red5'],\
                 item['red6'],item['prize1'],item['prize2'],item['prize3'],item['prize4'],item['prize5'],item['prize6'],\
                 item['wwp1'],item['wwp2'],item['wwp3'],item['wwp4'],item['wwp5'],item['wwp6'],'','')
            )
            if result > 0:
                self.stats.inc_value('database/items_added')
        log.msg("Item stored in db: %s" % item, level=log.DEBUG)



    def _handle_error(self, e):
        log.err(e)

