from urllib import parse

import datetime
from scrapy.spider import Spider, Request

from education_law.items import EducationLawItem


class EducationLawSpider(Spider):
    name = 'education_law_1'
    # 湖北教育厅
    allowed_domains = ["hbe.gov.cn"]
    start_urls = [
                #政策解读
                'http://www.hbe.gov.cn/page_zcjd.php',
                # #媒体聚焦
                'http://www.hbe.gov.cn/itemList.php?item=mtjj',
                # 重要通知
                'http://www.hbe.gov.cn/itemList.php?item=zytz',
                #公示公告
                'http://www.hbe.gov.cn/itemList.php?item=gsgg',
                # 本厅动态
                'http://www.hbe.gov.cn/itemList.php?item=jydt',
                #  教育动态
                'http://www.hbe.gov.cn/itemList.php?item=gddt',

                ]

    def parse(self, response):
        # 当前页面所用的url
        post_nodes = response.css("div.in-news-list li a")
        for post_node in post_nodes:
            # 提取开始url
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

            # 提取下一页并交给scrapy进行下载
            next_url = response.css("span.blue12  ::attr(href)").extract()[2]
            if next_url:
               yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = EducationLawItem()

        publishingunit_heat_publishtime = response.css("div.zhongji-biaoti span::text ").extract()[0].split()
        item['PublishingUnits'] = publishingunit_heat_publishtime[2]
        item['Heat'] = publishingunit_heat_publishtime[3].replace('浏览数：', '').replace('次', '')
        item['PublishTime'] = publishingunit_heat_publishtime[0].replace('发布时间：', '')
        item['Title'] = response.css("div.zhongji-biaoti h2::text ").extract()[0]
        item['ArticleUrl'] = response.url
        item['CrawlTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")
        item['Area'] = '湖北省'
        Conten = ((response.css(".zhongji-neirong").xpath("p/text()").extract()) or (response.css(".zhongji-neirong").css("a::text").extract()))#是个数组，解决取出所有值问题
        item['Content'] = ''.join(Conten).strip().replace('\xa0', '').replace('\n', '').replace('\u3000', '').strip()

        machthClassification = response.css("div.zhongji-biaoti h2::text ").extract()
        if "政策" in machthClassification:
            item['Classification'] = '政策解读'
        elif "通知" in machthClassification:
            item['Classification'] = '重要通知'
        elif "公"in machthClassification:
            item['Classification'] = '公示公告'
        else:
            item['Classification'] = '媒体聚焦'

        item['Annex'] = '无'

        yield item

