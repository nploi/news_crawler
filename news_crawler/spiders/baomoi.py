# -*- coding: utf-8 -*-
import scrapy
import os
import json
from codecs import open
import re

URL = 'https://baomoi.com'
# Hash table chưa tên chủ đề, để tạo thư mục
CATEGORIES = {
    'giao-duc': 'Giáo dục',
    'suc-khoe-y-te': 'Sức khoẻ - Y tế',
    'khoa-hoc': 'Khoa học',
    'khoa-hoc-cong-nghe': 'Khoa học - Công nghệ',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch'
}

CATEGORIES_COUNTER = {
    'giao-duc': [0, 0],
    'suc-khoe-y-te': [0, 0],
    'khoa-hoc': [0, 0],
    'khoa-hoc-cong-nghe': [0, 0],
    'giai-tri': [0, 0],
    'the-thao': [0, 0],
    'doi-song': [0, 0],
    'du-lich': [0, 0]
}

class BaoMoi(scrapy.Spider):
    '''Crawl tin tức từ https://baomoi.com website
    ### Các tham số:
        category: Chủ đề để crawl, có thể bỏ trống. Các chủ đề
                 * giao-duc
                 * suc-khoe-y-te
                 * khoa-hoc
                 * khoa-hoc-cong-nghe
                 * giai-tri
                 * the-thao
                 * doi-song
                 * du-lich  
        limit: Giới hạn số trang để crawl, có thể bỏ trống.
    '''

    name = "baomoi"
    folder_path = "baomoi"
    page_limit = None
    start_urls = [
    ]

    def __init__(self, category=None, limit=None, *args, **kwargs):
        super(BaoMoi, self).__init__(*args, **kwargs)
        if limit != None:
            self.page_limit = int(limit)

        # Tạo thư mục
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        if category in CATEGORIES:
            path = self.folder_path + '/' + CATEGORIES[category];
            if not os.path.exists(path):
                os.makedirs(path)   
            self.start_urls = ['%s/%s.epi' % (URL, category)]
        else:
            for CATEGORY in CATEGORIES:
                path = self.folder_path + '/' + CATEGORIES[CATEGORY];
                if not os.path.exists(path):
                    os.makedirs(path) 
                self.start_urls.append('%s/%s.epi' % (URL, CATEGORY));

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        category = self.get_category_from_url(response.url)

        if CATEGORIES_COUNTER[category][1] >= self.page_limit and self.page_limit is not None:
            return

        # Lấy link trang kế tiếp
        next_page_url = self.extract_next_page_url(response)

        if category in CATEGORIES and next_page_url is not None:
            CATEGORIES_COUNTER[category][1] = CATEGORIES_COUNTER[category][1] + 1
            # Đệ qui để crawl trang kế tiếp
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
        else:
            return

        # xử lý
        gridMain = response.css("div.wrapper.category_page div.main-content div.l-grid__main")
        for timeline in gridMain.css("div.timeline.loadmore div"):
            
            title = self.extract_title(timeline)
            link = self.extract_link(timeline)
            source = self.extract_source(timeline)
            date = self.extract_date(timeline)

            value = {
                'title': title,
                'source': source,
                'link': '%s%s' % (URL , link),
                'date': date
            }
            
            yield value

            CATEGORIES_COUNTER[category][0] = CATEGORIES_COUNTER[category][0] + 1
            filename = '%s/%s-%s.json' % (CATEGORIES[category], CATEGORIES[category], CATEGORIES_COUNTER[category][0])
            with open(self.folder_path + "/" + filename, 'wb', encoding= 'utf-8') as fp:
                json.dump(value, fp, ensure_ascii= False)
                self.log('Saved file %s' % filename)
        

    def get_category_from_url(self, url):
        items = url.split('/')
        category = None
        if len(items) >= 4:
            category = items[3].replace('.epi', '')
        return category

    def extract_title(self, timeline):
        title = timeline.css("h4.story__heading a::text").extract_first()
        if title is None:
            title = timeline.css("a.relate::text").extract_first()
        return title

    def extract_link(self, timeline):
        link = timeline.css("h4.story__heading a::attr(href)").extract_first()
        if link is None:
            link = timeline.css("a::attr(href)").extract_first()
        return link

    def extract_source(self, timeline):
        source = timeline.css("div.story__meta a::text").extract_first()
        return source

    def extract_date(self, timeline):
        date = timeline.css("div.story__meta time.time.friendly::attr(datetime)").extract()
        return date
    
    def extract_next_page_url(self, response):
        gridMain = response.css("div.wrapper.category_page div.main-content div.l-grid__main")
        next_page_url = gridMain.css("div.control span > a.control__next::attr(href)").extract_first()
        return next_page_url