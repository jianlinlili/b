from urllib import parse

import datetime
from scrapy.spider import Spider, Request

from education_law.items import EducationLawItem


class EducationLawSpider(Spider):
    name = 'education_law_4'
    # 海南省
    allowed_domains = ["gov.cn"]
    start_urls = [
                # 政策解读
                'http://edu.hainan.gov.cn/news-list-633-1.html',
                # # #媒体聚焦
                 'http://edu.hainan.gov.cn/news-list-596-1.html',
                # 重要通知
                # 'http://www.hbe.gov.cn/itemList.php?item=zytz',
                # 公示公告
                # 'http://www.hbe.gov.cn/itemList.php?item=gsgg',
                # # 本厅动态
                # 'http://www.hbe.gov.cn/itemList.php?item=jydt',
                # #  教育动态
                # 'http://www.hbe.gov.cn/itemList.php?item=gddt',

                ]

    def parse(self, response):
        # 当前页面所用的url
        post_nodes = response.css("ul.listbox li a")
        for post_node in post_nodes:
            # 提取开始url
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

            # 提取下一页并交给scrapy进行下载
            next_url = response.css("span.next_page a::attr(href)").extract()[0]
            if next_url:
               yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = EducationLawItem()



        item['PublishingUnits'] = response.css("div.conbox_t2 span::text ").extract()[1]
        item['Heat'] = response.css("div.conbox_t2 span::text ").extract()[3].replace('浏览次数：', '').strip()
        item['PublishTime'] = response.css("div.conbox_t2 span::text ").extract()[2].replace('发布时间：', '').strip()
        item['Title'] = response.css("div.conbox_t ::text ").extract()[0].strip()
        item['ArticleUrl'] = response.url
        item['CrawlTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")
        item['Area'] = '海南省'

        Conten = response.css(".conbox_m ::text").extract() # 解决类容是数组类型
        item['Content'] = ''.join(Conten).strip().replace('\xa0', '').replace('\n', '').replace('\u3000', '').strip()

        machthClassification = response.css("div.conbox_t ::text ").extract()[0].strip()
        if "政策" in machthClassification:
            item['Classification'] = '政策解读'
        elif "通知" in machthClassification:
            item['Classification'] = '重要通知'
        elif "公"in machthClassification:
            item['Classification'] = '公示公告'
        else:
            item['Classification'] = '通知公告'

        item['Annex'] = '无'

        yield item

