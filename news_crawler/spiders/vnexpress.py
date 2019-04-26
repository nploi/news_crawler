#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import os
import json
from codecs import open
from datetime import datetime

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
    '''Khai thác dữ liệu tin tức từ https://vnexpress.net website
    ### Các tham số:
        category: Chủ đề để crawl, có thể bỏ trống. Các chủ đề
                 * giao-duc
                 * suc-khoe
                 * khoa-hoc
                 * giai-tri
                 * the-thao
                 * doi-song
                 * du-lich  
        limit: Giới hạn số trang để crawl, có thể bỏ trống.
    '''
    name = "vnexpress"
    folder_path = "vnexpress"
    page_limit = None
    page_count = 0
    count = 0
    start_urls = [
    ]

    def __init__(self, category=None, limit=None, *args, **kwargs):
        super(VnExpress, self).__init__(*args, **kwargs)
        if limit != None:
            self.page_limit = int(limit)
        # Tạo thư mục
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        if category in CATEGORYS:
            folders_path = self.folder_path + '/' + CATEGORYS[category];
            if not os.path.exists(folders_path):
                os.makedirs(folders_path)
            self.start_urls = [URL + category]
        else:
            for CATEGORY in CATEGORYS:
                folders_path = self.folder_path + '/' + CATEGORYS[CATEGORY];
                if not os.path.exists(folders_path):
                    os.makedirs(folders_path)
                self.start_urls.append(URL + CATEGORY);

    def start_requests(self):
        for url in self.start_urls:
            self.page_count = 0
            yield scrapy.Request(url=url, callback=self.parse_list_news)

    def parse_list_news(self, response):
        self.page_count = self.page_count + 1
        if self.page_count > self.page_limit and self.page_limit is not None:
            return

        section = response.css("section section")
        for list_news in section.css("article.list_news"):
            relative_url = list_news.css('h4 a::attr(href)').extract_first()
            abs_url = response.urljoin(relative_url)
            yield scrapy.Request(abs_url, callback=self.parse_news)

        # Lấy link trang kế tiếp
        url = response.url;
        next_page_url = section.css("div.pagination.mb10 > a.next::attr(href)").extract_first()
        if "doi-song" in url:
            next_page_url = section.css("div.pagination.mb10 > a.pagination_btn.pa_next.next::attr(href)").extract_first()
        if "du-lich" in url or "giai-tri" in url or "suc-khoe" in url:
            next_page_url = section.css("p.pagination.mb10 > a.next::attr(href)").extract_first()
        
        # Đệ qui để crawl trang kế tiếp
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_list_news)

    def parse_news(self, response):
        news = response.css("section section section");

        jsonData = {
            'date': news.css("header span::text").extract_first(),
            'title': news.css("h1::text").extract_first(),
            'link': response.url,
            'content': news.css("article p::text").getall(),
        }

        yield jsonData

        items = response.url.split('/')

        # Write to file
        if len(items) >= 5 and items[3] in CATEGORYS:
            self.count += 1
            filename = '%s/%s-%s.json' % (CATEGORYS[items[3]], CATEGORYS[items[3]], self.count)
            with open(self.folder_path+"/"+filename, 'wb', encoding= 'utf-8') as fp:
                json.dump(jsonData, fp, ensure_ascii= False)
            self.log('Saved file %s' % filename)
        