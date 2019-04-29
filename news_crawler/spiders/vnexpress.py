#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import os
import json
from codecs import open
from datetime import datetime
import re

URL = 'https://vnexpress.net/'

# Hash table chưa tên chủ đề, để tạo thư mục
CATEGORIES = {
    'giao-duc': 'Giáo dục',
    'suc-khoe': 'Sức khoẻ - Y tế',
    'khoa-hoc': 'Khoa học',
    'so-hoa': ' Công nghệ',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch'
}

CATEGORIES_COUNTER = {
    'giao-duc': [0, 0],
    'suc-khoe': [0, 0],
    'khoa-hoc': [0, 0],
    'so-hoa': [0, 0],
    'giai-tri': [0, 0],
    'the-thao': [0, 0],
    'doi-song': [0, 0],
    'du-lich': [0, 0]
}

class VnExpress(scrapy.Spider):
    '''Crawl tin tức từ https://vnexpress.net website
    ### Các tham số:
        category: Chủ đề để crawl, có thể bỏ trống. Các chủ đề
                 * giao-duc
                 * suc-khoe
                 * khoa-hoc
                 * so-hoa
                 * giai-tri
                 * the-thao
                 * doi-song
                 * du-lich
        limit: Giới hạn số trang để crawl, có thể bỏ trống.
    '''
    name = "vnexpress"
    folder_path = "vnexpress"
    page_limit = None
    start_urls = [
    ]

    def __init__(self, category=None, limit=None, *args, **kwargs):
        super(VnExpress, self).__init__(*args, **kwargs)
        if limit != None:
            self.page_limit = int(limit)
        # Tạo thư mục
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        if category in CATEGORIES:
            folders_path = self.folder_path + '/' + CATEGORIES[category];
            if not os.path.exists(folders_path):
                os.makedirs(folders_path)
            self.start_urls = [URL + category]
        else:
            for CATEGORY in CATEGORIES:
                folders_path = self.folder_path + '/' + CATEGORIES[CATEGORY];
                if not os.path.exists(folders_path):
                    os.makedirs(folders_path)
                self.start_urls.append(URL + CATEGORY);

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list_news)

    def parse_list_news(self, response):
        category = self.get_category_from_url(response.url)

        if (CATEGORIES_COUNTER[category][1] >= self.page_limit or self.page_limit <= 0) and self.page_limit is not None:
            return

        next_page_url = self.extract_next_page_url(response)

        if category in CATEGORIES and next_page_url is not None:
            CATEGORIES_COUNTER[category][1] = CATEGORIES_COUNTER[category][1] + 1
            # Đệ qui để crawl trang kế tiếp
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_list_news)
        else:
            return

        # Xử lý
        section = response.css("section section")
        for list_news in section.css("article.list_news"):
            relative_url = list_news.css('h4 a::attr(href)').extract_first()
            abs_url = response.urljoin(relative_url)
            yield scrapy.Request(abs_url, callback=self.parse_news)

                
    def extract_next_page_url(self, response):
        section = response.css("section section")
        # Lấy link trang kế tiếp
        url = response.url;
        next_page_url = section.css("div.pagination.mb10 > a.next::attr(href)").extract_first()
        if "doi-song" in url:
            next_page_url = section.css("div.pagination.mb10 > a.pagination_btn.pa_next.next::attr(href)").extract_first()
        if "du-lich" in url or "giai-tri" in url or "suc-khoe" in url:
            next_page_url = section.css("p.pagination.mb10 > a.next::attr(href)").extract_first()

        return next_page_url

    def parse_news(self, response):

        jsonData = self.extract_news(response)

        yield jsonData

        items = response.url.split('/')

        # Write to file
        if len(items) >= 5 and items[3] in CATEGORIES:
            CATEGORIES_COUNTER[items[3]][0] = CATEGORIES_COUNTER[items[3]][0] + 1
            filename = '%s/%s-%s.json' % (CATEGORIES[items[3]], CATEGORIES[items[3]], CATEGORIES_COUNTER[items[3]][0])
            with open(self.folder_path + "/" + filename, 'wb', encoding = 'utf-8') as fp:
                json.dump(jsonData, fp, ensure_ascii= False)
                self.log('Saved file %s' % filename)
    

    def get_category_from_url(self, url):
        items = url.split('/')
        category = None
        if len(items) >= 4:
            category = re.sub(r'-p[0-9]+', '', items[3])
        return category

    def extract_news(self, response):

        date = self.extract_date(response)
        title = self.extract_title(response)
        content = self.extract_content(response)
        author = self.extract_author(response)
        description = self.extract_description(response)

        jsonData = {
            'date': date,
            'title': title,
            'link': response.url,
            'content': content,
            'author': author,
            'description': description
        }

        return jsonData

    def extract_title(self, response):
        news = response.css("section section section")
        title = news.css("h1::text").extract_first()
        if title is None:
            title = news.css("h1.title_news_detail.mb10::text").extract_first()
        if title is None:
            title = response.css("section section h1::text").extract_first()
        return title

    def extract_description(self, response):
        news = response.css("section section section")
        description = news.css("p::text").extract_first()
        return description

    def extract_content(self, response):
        news = response.css("section section section")
        content = news.css("article p::text").getall()
        if content is None:
            content = response.css("section section article p.Normal::text").getall()
        return content

    def extract_date(self, response):
        news = response.css("section section section")
        date = news.css("header span::text").extract_first()
        if date is None:
            date = response.css("section section header span::text").extract_first()
        return date
    
    def extract_author(self, response):
        news = response.css("section section section")
        author = news.css("article p strong::text").extract_first()
        if author is None:
            author = news.css("p.Normal strong::text").extract_first()
        if author is None:
            author = response.css("section section p.Normal strong::text").extract_first()
        return author