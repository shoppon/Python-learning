# coding: utf-8
import os
import sys

from oslo_config import cfg
from scrapy import Spider
from scrapy import cmdline

from shoppon.db.mongo import api
from shoppon.logs import my_syslog

CONF = cfg.CONF
LOG = my_syslog.get_logger()

opts = [
    cfg.StrOpt("url",
               help="Spider url."),
    cfg.StrOpt("allowed_domains",
               help="Allowed domains."),
    cfg.StrOpt("database",
               help="Database name of mongodb to store."),
    cfg.StrOpt("collection",
               help="Collection name of mongodb to store."),
]
CONF.register_opts(opts, group="planning")


class PlanningSpider(Spider):
    name = 'gov_planning_spider'
    start_urls = [CONF.planning.url]
    allowed_domains = CONF.planning.allowed_domains

    def parse(self, response):
        LOG.info("Get response-->%s." % response)
        mongo_client = api.get_client(CONF.planning.database,
                                      CONF.planning.collection)

        for item in response.css('.info_title'):
            title = item.css('a ::text').extract_first().encode("utf-8")
            mongo_client.insert({'item': title})
            yield {'title': title}

        for next_page in response.css('li>a'):
            yield response.follow(next_page, self.parse)


if __name__ == '__main__':
    LOG.info("Start run spiders.")
    cur_dir = os.path.dirname(__file__)
    top_dir = os.path.join(cur_dir[:cur_dir.index('shoppon')],
                           'shoppon', 'etc')
    CONF(sys.argv[1:], project='shoppon',
         default_config_dirs=[top_dir])
    try:
        # Python第一个参数是文件名，这里可以不填
        cmdline.execute(argv=['', 'runspider', __file__])
    except Exception as err:
        LOG.exception("An exception occurred: %s" % err)
        sys.exit(-1)
    else:
        LOG.info("Run spiders successfully.")