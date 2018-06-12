from urllib import parse

import datetime


from scrapy.spider import Spider, Request

from education_law.items import EducationLawItem

# 福建
class JianshuSpider(Spider):
    name = 'education_law_3'
    allowed_domains = ["gov.cn"]
    start_urls = [
        # 政策法规
        'http://jyt.jiangsu.gov.cn/col/col38737/index.html',
        # #处室文件
         'http://www.fjedu.gov.cn/html/xxgk/zcjd/qtzcwjjd/1.html',
        #公示公告
         'http://www.fjedu.gov.cn/html/xxgk/zcjd/bmzcwjjd/1.html',
        #本科高校
        'http://www.fjedu.gov.cn/html/xxgk/gggs/1.html',

      ]

    def parse(self, response):
        # 当前页面所用的url
        post_nodes = response.css("ul.n_list li a")
        for post_node in post_nodes:
            # 提取开始url
            post_url = post_node.css("::attr(href)").extract_first()
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)
            # 提取下一页并交给scrapy进行下载

            #  提取下一页完成
            next_url = response.css("li.nextpage a::attr(href)").extract_first()
            if next_url:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = EducationLawItem()


        item['PublishTime'] = response.xpath('//div[@class="detail_main_content"]/h1/text()').extract()[1]
        item['PublishingUnits'] = response.xpath('//div[@class="detail_main_content"]/h1/span/text()').extract()[1]
        item['Title'] = response.css("div.detail_main_content h3::text ").extract()[0].strip()
        item['ArticleUrl'] = response.url
        item['CrawlTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")
        item['Area'] = '福建省'

        conten = response.xpath('//div[@class="detail_content_display"]/div/p/text()').extract()
        item['Content'] = ''.join(conten).strip().replace('\xa0', '').replace('\n', '').replace('\u3000', '').strip()
        item['Heat'] = '暂无'
        machthClassification = response.css("div.detail_main_content h3::text ").extract()[0].strip()
        if "通知" in machthClassification:
            item['Classification'] = '信息公开'
        else:
            item['Classification'] = '政策解读'

        item['Annex'] = '无'
        yield item
