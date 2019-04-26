# -*- coding: utf-8 -*-
import scrapy
import os
import json
from codecs import open

URL = 'https://baomoi.com/'
# Hash table chưa tên chủ đề, để tạo thư mục
CATEGORYS = {
    'giao-duc': 'Giáo dục',
    'suc-khoe-y-te': 'Sức khoẻ - Y tế',
    'khoa-hoc-cong-nghe': 'Khoa học – Công nghệ',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch'
}

class BaoMoi(scrapy.Spider):
    name = "baomoi"
    folder_path = "baomoi"

    start_urls = [
    ]
    count = 0

    def __init__(self, category=None, *args, **kwargs):
        super(BaoMoi, self).__init__(*args, **kwargs)
        # Tạo thư mục
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        if category in CATEGORYS:
            path = self.folder_path + '/' + CATEGORYS[category];
            if not os.path.exists(path):
                os.makedirs(path)   
            self.start_urls = [URL + category + '.epi']
        else:
            for CATEGORY in CATEGORYS:
                path = self.folder_path + '/' + CATEGORYS[CATEGORY];
                if not os.path.exists(path):
                    os.makedirs(path) 
                self.start_urls.append(URL + CATEGORY + '.epi');

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.url.split('/')
        if len(items) >= 4:
            category = items[3].replace('.epi', '')
            category = CATEGORYS[category]

        for storyHeading in response.css("div.wrapper.category_page div.main-content div.l-grid__main div.timeline.loadmore div div.story__heading"):

            yield {
                'title': storyHeading.css("a::text").extract(),
                'link': response.urljoin(storyHeading.css("a::attr(href)").extract())
            }
            value = {
                'title': storyHeading.css("a::text").extract(),
                'link': response.urljoin(storyHeading.css("a::attr(href)").extract())
            }

            self.count += 1
            filename = '%s/%s-%s.txt' % (category, category, self.count)
            with open(self.folder_path+"/"+filename, 'wb+', encoding= 'utf-8') as fp:
                json.dump(value, fp, ensure_ascii= False)

            self.log('Saved file %s' % filename)