#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import os
import json
import json
from codecs import open

URL = 'https://vnexpress.net/'

# Hash table chưa tên chủ đề, để tạo thư mục
CATEGORYS = {
    'giao-duc': 'Giáo dục', #
    'suc-khoe': 'Sức khoẻ - Y tế',
    'khoa-hoc': 'Khoa học – Công nghệ',#
    'giai-tri': 'Giải trí',#
    'the-thao': 'Thể thao',#
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch'
}

class VnExpress(scrapy.Spider):
    name = "vnexpress"
    folder_path = "vnexpress"
    page = "/p"
    count = 0
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

    def parse_list_news(self, response):
        section = response.css("section section")
        for list_news in section.css("article.list_news"):
            relative_url = list_news.css('h4 a::attr(href)').extract_first()
            abs_url = response.urljoin(relative_url)
            # print(abs_url)
            yield scrapy.Request(abs_url, callback=self.parse_news)
        
        url = response.url;
        next_page_url = section.css("div.pagination.mb10 > a.next::attr(href)").extract_first()
        if "doi-song" in url:
            next_page_url = section.css("div.pagination.mb10 > a.pagination_btn.pa_next.next::attr(href)").extract_first()
        if "du-lich" in url or "giai-tri" in url or "suc-khoe" in url:
            next_page_url = section.css("p.pagination.mb10 > a.next::attr(href)").extract_first()

        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_list_news)

    def parse_news(self, response):
        news = response.css("section section section");
        items = response.url.split('/')

        # yield {
        #     'title': news.css("h1::text").extract(),
        #     'content': news.css("article p::text").getall(),
        #     'link': response.url,
        # }

        jsonData = {
            'title': news.css("h1::text").extract(),
            'content': news.css("article p::text").getall(),
            'link': response.url,
        }

        if len(items) >= 5 and items[3] in CATEGORYS:
            self.count += 1
            # filename = '%s/%s' % (CATEGORYS[items[3]], items[4])
            # with open(self.folder_path+"/"+filename, 'wb') as f:
            #     f.write(response.body)
            filename = '%s/%s.json' % (CATEGORYS[items[3]], CATEGORYS[items[3]])
            with open(self.folder_path+"/"+filename, 'a+', encoding= 'utf-8') as fp:
                json.dump(jsonData, fp, ensure_ascii= False)
            self.log('Saved file %s' % filename)
        