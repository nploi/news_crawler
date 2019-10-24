
# news_crawler

News crawler là một công cụ giúp bạn có  crawl dữ liệu các website tin tức

## Tác giả: 
- [Nguyễn Phúc Lợi](https://github.com/nploi)

#### Chức năng
* Crawl theo website được tích hợp
* Crawl theo chủ đề
* Crawl tất cả chủ đề
* Có thể giới hạn số trang

#### Trang web được tích hợp vào để crawl
* [VNEXPRESS](https://vnexpress.net/)
* [BÁO MỚI](https://baomoi.com/)

#### Chủ đề
* Giáo dục
* Y tế
* Khoa học
* Công nghệ
* Giải trí
* Thể thao
* Sức khoẻ
* Đời sống
* Du lịch

Web/Chủ đề| Giáo dục | Y tế | Khoa học | Công nghệ | Giải trí | hể thao | Sức khoẻ| Đời sống | Du lịch
--- | --- | --- | --- |--- |--- |--- |--- |---|--- 
[VNEXPRESS](https://vnexpress.net/) | OK | OK | OK | OK | OK | OK | OK | OK | OK
[BÁO MỚI](https://baomoi.com/) | OK | OK | OK | OK | OK | OK | OK | OK | OK


### Hướng đẫn

[Cài đặt scrapy](http://doc.scrapy.org/en/latest/intro/install.html) trước khi chạy
```bash
pip install Scrapy
```

Sau khi cài đặt xong bạn cần kiểm tra bằng lệnh sau
```bash
scrapy --version
```
Clone repository này về  nhé, tiếp theo rõ và chạy command line `scrapy list` để hiện thị danh sách website để  crawl
```bash
git clone https://github.com/nploi/news_crawler.git
cd news_crawler
scrapy list
```
Output sẽ là
```bash
baomoi
vnexpress
```
Chọn `vnexpress` hoặc `baomoi` nhé :))
```bash
scrapy crawl vnexpress -a category=the-thao -a limit=2
```
Chúc mừng bạn đã chạy thành công, hy vọng là vậy =]], vào thư mục `vnexpress/Thể thao/` và xem thành quả của mình nào :v

Bạn cũng có thể chạy lệnh như sao để xuất tất cả dữ liệu vào một file `.json`

```bash
scrapy crawl vnexpress -a category=the-thao -a limit=2 -o vnexpress.json
```

Giải thích các tham số:
- `category`: Chủ đề để crawl, có thể bỏ trống. Các chủ đề
    * giao-duc
    * suc-khoe
    * khoa-hoc
    * giai-tri
    * the-thao
    * doi-song
    * du-lich
- `limit`: Giới hạn số trang để crawl, tốt nhất là nên có tham số này để k phải đợi lâu, có thể bỏ trống.

