# -*- coding: utf-8 -*-
import scrapy
import os
import urlparse

URL = 'https://vnexpress.net/'
# Hash table chưa tên chủ đề, để tạo thư mục
CATEGORYS = {
    'giao-duc': 'Giáo dục',
    'suc-khoe': 'Sức khoẻ - Y tế',
    'khoa-hoc': 'Khoa học – Công nghệ',
    'so-hoa': 'Khoa học – Công nghệ',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch'
}

class VnExpress(scrapy.Spider):
    name = "vnexpress"
    folder_path = "vnexpress"

    start_urls = [
    ]

    def __init__(self, category=None, *args, **kwargs):
        super(VnExpress, self).__init__(*args, **kwargs)
        # Tạo thư mục


        # Create target Directory if don't exist
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)


        if category in CATEGORYS:
            path = self.folder_path + '/' + CATEGORYS[category];
            if not os.path.exists(path):
                os.makedirs(path)    
            self.start_urls = [URL + category]
        else:
            for CATEGORY in CATEGORYS:
                path = self.folder_path + '/' + CATEGORYS[CATEGORY];
                if not os.path.exists(path):
                    os.makedirs(path)  
                self.start_urls.append(URL + CATEGORY);

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list_news)
            for index in range(2,50):
                yield scrapy.Request(url=url + '/p%s' % index, callback=self.parse_list_news)
    

    def parse_list_news(self, response):
        for list_news in response.css("section section article.list_news"):
            relative_url = list_news.css('h4 a::attr(href)').extract_first()
            abs_url = response.urljoin(relative_url)
            # print(abs_url)
            yield scrapy.Request(abs_url, callback=self.parse_news)

    def parse_news(self, response):
        # news = response.css("section section section");
        # yield {
        #     'title': news.css("h1::text").extract(),
        #     'content': news.css("article p::text").getall(),
        #     'link': response.url
        # }
        # print ({
        #     'title': news.css("h1::text").extract(),
        #     'content': news.css("article p::text").getall(),
        #     'link': response.url
        # })

        print('Downdload: ' + response.url + '......');

        items = response.url.split('/')
        filename = '%s/%s' % (CATEGORYS[items[3]], items[4])
        with open(self.folder_path+"/"+filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        