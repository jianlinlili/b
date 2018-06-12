from urllib import parse

import datetime
from scrapy.spider import Spider, Request

from education_law.items import EducationLawItem


class EducationLawSpider(Spider):
    name = 'education_law_5'
    # 海南省
    allowed_domains = ["gov.cn"]
    start_urls = [
                # 政策解读
                'https://www.hljedu.gov.cn/zwgk/zcjd/',
                # # # #媒体聚焦
                'https://www.hljedu.gov.cn/zwgk/sytj/',
                # 重要通知
                'https://www.hljedu.gov.cn/zhuanti/jyfzzl/',
                # 公示公告
                # 'http://www.hbe.gov.cn/itemList.php?item=gsgg',
                 # 本厅动态
                # 'http://www.hbe.gov.cn/itemList.php?item=jydt',
                #  教育动态
                # 'http://www.hbe.gov.cn/itemList.php?item=gddt',

                ]

    def parse(self, response):
        # 当前页面所用的url
        post_nodes = response.css("div.class_one_lb li a")
        for post_node in post_nodes:
            # 提取开始url
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

            # 提取下一页并交给scrapy进行下载!!!!!!未解决
            # next_url = response.css("div.pagenum a::attr(href)").extract()[0]
            #
            # if next_url:
            #  yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = EducationLawItem()
        #item['PublishingUnits'] = response.css("div.end_tit p a::text").extract()[3]
        item['PublishingUnits'] = '教育部'
        item['Heat'] = '暂无'
        item['PublishTime'] = response.css("div.end_tit p::text").extract()[5].replace('更新时间：', '').strip()
        item['Title'] = response.css("div.end_tit h1::text ").extract()[0]
        item['ArticleUrl'] = response.url
        item['CrawlTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")
        item['Area'] = '海南省'

        Conten = response.css(".TRS_Editor p::text").extract()  # 解决类容是数组类型
        item['Content'] = ''.join(Conten).strip().replace('\xa0', '').replace('\n', '').replace('\u3000', '').strip()

        machthClassification = response.css("div.end_tit h1::text ").extract()[0]
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

