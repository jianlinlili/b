from urllib import parse

import datetime


from scrapy.spider import Spider, Request

from education_law.items import EducationLawItem


class EducationLawSpider(Spider):
    name = 'education_law'
    # 四川教育网
    allowed_domains = ["scedu.net"]
    start_urls = [
                #教育文件
                'http://www.scedu.net/p/48/?tfid=636203266718134497',
                'http://www.scedu.net/p/48/?tfid=635874997663998784',
                'http://www.scedu.net/p/48/?tfid=635538212734448750',
                'http://www.scedu.net/p/48/?tfid=635537174764761250',
                'http://www.scedu.net/p/48/?tfid=636203266718134497',
                'http://www.scedu.net/p/48/?tfid=635679029439808535',

        #政策解读

                'http://www.scedu.net/p/48/?tfid=635679029559665391_',
                'http://www.scedu.net/p/48/?tfid=635874997663998784',
                'http://www.scedu.net/p/48/?tfid=635538212734448750',
                'http://www.scedu.net/p/48/?tfid=635537174535230000',
                'http://www.scedu.net/p/48/?tfid=635537174764761250',
                'http://www.scedu.net/p/48/?tfid=635537174827573750',
                'http://www.scedu.net/p/48/?tfid=635537175103980000',

                #高校动态
                'http://www.scedu.net/p/8/?StId=st_app_news_search_x635532828009292500_x_',
                'http://www.scedu.net/p/8/?StId=st_app_news_search_x635532826176480000_x_',
                'http://www.scedu.net/p/8/?StId=st_app_news_search_x635532826176480000_x_',
                'http://www.scedu.net/p/8/?StId=st_app_news_search_x635532826176480000_x_',
                'http://www.scedu.net/p/48/?tfid=635679029439808535',
                ]

    def parse(self, response):
        # 当前页面所用的url
        post_nodes = ((response.css("div.div_list .div_item .div_title a"))or (response.css("div.st_div .div_item .div_itemtitle a")))


        for post_node in post_nodes:
            # 提取开始url
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

            # 提取下一页并交给scrapy进行下载
            next_url = response.css("div.myp2c_div_paging  ::attr(href)").extract_first("")
            #（未实现）  解析javasrip下一页，本处是自动提取下一个也页面的关键
            #     javascript:fn_loaditems_id_6a4e96a3_7f4b_46f4_b383_5c6b27673ec3(2)'
            # t _url = response.css("div.myp2c_div_paging  ::attr(href)").extract_first("")
            # next_url = document.execCommand(t_url)

            if next_url:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item = EducationLawItem()
        item['PublishingUnits'] = response.xpath('//div[@class="box"]/div/text()').extract()[3].strip()  # response.css("div.box div::text").extract()[3].strip()
        item['Title'] = response.xpath('//div[@class="div_title"]/text()').extract()[0]   #  response.css(".div_title ::text").extract()[0]
        item['PublishTime'] = response.xpath('//div[@class="box"]/div/text()').extract()[2].strip().replace('发布时间：', '').replace(r'年', '-').replace(r'月', '-').replace(r'日', '')
        item['ArticleUrl'] = response.url
        item['Content'] = response.css(".div_content").xpath("string(div)").extract_first(default="").strip().replace('\xa0', '').replace('\n', '').replace('\u3000', '')
        item['CrawlTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")
        macthArea = response.xpath('//div[@class="box"]/div/text()').extract()[3].strip()
        if "四川" in macthArea:
            item['Area'] = '四川省'
        else:
            item['Area'] = '成都市'

        machthClassification = response.xpath('//div[@class="div_title"]/text()').extract()[0]
        if "政策" in machthClassification:
            item['Classification'] = '政策解读'
        elif "教育" in machthClassification :
            item['Classification'] = '教育厅文件'
        else:
            item['Classification'] = '高等学校动态'

        item['Annex'] = '无'
        item['Heat'] = '暂无'

        yield item






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

            # ！！！！！！！！！！！！！！！！！提取下一页未完成
            next_url = response.css('div.list_body_box1 .pagingNormal a')
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

