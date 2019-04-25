# -*- coding: utf-8 -*-
import scrapy
import os

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

    def __init__(self, category=None, *args, **kwargs):
        super(BaoMoi, self).__init__(*args, **kwargs)
        # Tạo thư mục
        os.mkdir(self.folder_path)

        if category in CATEGORYS:
            path = self.folder_path + '/' + CATEGORYS[category];
            os.makedirs(path)
            self.start_urls = [URL % category + '.epi']
        else:
            for CATEGORY in CATEGORYS:
                path = self.folder_path + '/' + CATEGORYS[category];
                os.makedirs(path)
                self.start_urls.append(URL % CATEGORY + '.epi');

    def start_requests(self):
        print("Comming soon :D")
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for a in response.css("nav.p_menu a"):

            yield {
                'chu_de': a.css("::text").extract(),
                'link': a.css("::attr(href)").extract()
            }
            value = {
                'chu_de': a.css("::text").extract(),
                'link': a.css("::attr(href)").extract()
            }
        print("Comming soon :D")