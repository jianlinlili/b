from urllib import parse

import datetime


from scrapy.spider import Spider, Request

from education_law.items import EducationLawItem

#山东省
class JianshuSpider(Spider):
    name = 'education_law_2'
    allowed_domains = ["gov.cn"]
    start_urls = [
        # 政策文件
        'http://www.sdedu.gov.cn/sdjy/_zcwj/index.html',
        #处室文件
        'http://www.sdedu.gov.cn/sdjy/_cshj/index.html',
        #公示公告
        'http://www.sdedu.gov.cn/sdjy/_gsgg/index.html',
        #本科高校
        'http://www.sdedu.gov.cn/sdjy/_jycz/_bkgx/index.html',

      ]

    def parse(self, response):
        # 当前页面所用的url
        post_nodes = response.css("div.list_body_box1 .art_tit a")
        for post_node in post_nodes:
            # 提取开始url
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)
            # 提取下一页并交给scrapy进行下载

            #  提取下一页完成
            next_url = response.css('.pagingNormal ::attr(tagname)').extract()[0]
            if next_url:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = EducationLawItem()

        item['PublishingUnits'] = response.xpath('//table[@class="normal"]/tbody//div/text()').extract()[0].strip().strip()
        item['PublishTime'] = response.xpath('//table[@class="normal"]/tbody//div/text()').extract()[0].strip().replace('发布时间：', '').replace('来源：本站', '').replace(r'年', '-').replace(r'月', '-').replace(r'日', '')
        item['Title'] = response.xpath('//td[@class="xxbt"]/text()').extract()[1].strip()  # response.xpath('//div[@class="div_title"]/text()').extract()[ 0]  # response.css(".div_title ::text").extract()[0]
        item['ArticleUrl'] = response.url
        item['Content'] = response.css(".conzt").xpath("string(div)").extract_first(default="").strip().replace('\xa0', '').replace('\n', '').replace('\u3000', '')
        item['CrawlTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")  # str(datetime.datetime.now().replace(microsecond=0))

        item['Area'] = '山东省'

        macthAreaContent = response.css(".conzt").xpath("string(div)").extract_first(default="").strip().replace('\xa0', '').replace('\n', '').replace('\u3000', '')
        if "厅" in macthAreaContent:
            item['Classification'] = '政策文件'
        elif "处" in macthAreaContent:
            item['Classification'] = '处室文件'
        elif "公示" in macthAreaContent:
            item['Classification'] = '公示公告'

        else:
            item['Classification'] = '高校动态'

        item['Annex'] = '暂无'
        item['Heat'] = '暂无'
        yield item

