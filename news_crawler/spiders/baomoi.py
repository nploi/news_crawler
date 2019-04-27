# -*- coding: utf-8 -*-
import scrapy
import os
import json
from codecs import open

URL = 'https://baomoi.com'
# Hash table chưa tên chủ đề, để tạo thư mục
CATEGORIES = {
    'giao-duc': 'Giáo dục',
    'suc-khoe-y-te': 'Sức khoẻ - Y tế',
    'khoa-hoc-cong-nghe': 'Khoa học - Công nghệ',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch'
}

CATEGORIES_COUNTER = {
    'giao-duc': [0, 0],
    'suc-khoe-y-te': [0, 0],
    'khoa-hoc-cong-nghe': [0, 0],
    'giai-tri': [0, 0],
    'the-thao': [0, 0],
    'doi-song': [0, 0],
    'du-lich': [0, 0]
}

class BaoMoi(scrapy.Spider):
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
        items = response.url.split('/')
        if len(items) >= 4:
            category = items[3].replace('.epi', '')
        gridMain = response.css("div.wrapper.category_page div.main-content div.l-grid__main")
        for timeline in gridMain.css("div.timeline.loadmore div"):
            
            value = {
                'title': timeline.css("h4.story__heading a::text").extract_first(),
                'source': timeline.css("div.story__meta a::text").extract_first(),
                'link': '%s%s' % (URL ,timeline.css("h4.story__heading a::attr(href)").extract_first()),
                'date': timeline.css("div.story__meta time.time.friendly::attr(datetime)").extract()
            }
            
            yield value
            
            CATEGORIES_COUNTER[category][0] = CATEGORIES_COUNTER[category][0] + 1
            filename = '%s/%s-%s.json' % (CATEGORIES[category], CATEGORIES[category], CATEGORIES_COUNTER[category][0])
            with open(self.folder_path + "/" + filename, 'wb', encoding= 'utf-8') as fp:
                json.dump(value, fp, ensure_ascii= False)
                self.log('Saved file %s' % filename)
        
        # Lấy link trang kế tiếp
        url = response.url;
        next_page_url = gridMain.css("div.control span > a.control__next::attr(href)").extract_first()

        if len(items) >= 4 and category in CATEGORIES:
            if CATEGORIES_COUNTER[category][1] < self.page_limit or self.page_limit is None:
                if next_page_url is not None:
                    CATEGORIES_COUNTER[category][1] = CATEGORIES_COUNTER[category][1] + 1
                    # Đệ qui để crawl trang kế tiếp
                    yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)