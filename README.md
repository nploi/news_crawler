
# news_crawler

News crawler là một công cụ giúp bạn có thể khai thác dữ liệu của một trang tin tức

## Tác giả: 
- Nguyễn Phúc Lợi
- 1660321
- HCMUS

#### Các chức năng
* Theo website được tích hợp
* Khai thác theo chủ đề
* Tất cả chủ đề
* Có thể giới hạn số trang

#### Các trang web được tích hợp vào để khai thác
* [VNEXPRESS](https://vnexpress.net/)
* [BAOMOI](https://baomoi.com/) (comming soon)

#### Các chủ đề
* Giáo dục
* Y tế
* Khoa học – Công nghệ
* Giải trí
* Thể thao
* Sức khoẻ
* Đời sống
* Du lịch

Web/Chủ đề| Giáo dục | Y tế | Khoa học – Công nghệ | Giải trí | hể thao | Sức khoẻ| Đời sống | Du lịch
--- | --- | --- | --- |--- |--- |--- |--- |--- 
 [VNEXPRESS](https://vnexpress.net/) | OK | OK | OK | OK | OK | OK | OK | OK 
[BAOMOI](https://baomoi.com/) | X | X | X | X | X | X | X | X 


### Hướng đẫn chạy chương trình

[Cài đặt scrapy](http://doc.scrapy.org/en/latest/intro/install.html) trước khi chạy

Sau khi cài đặt xong bạn cần kiểm tra bằng lệnh sau
```bash
scrapy --version
```
Clone repository này về  nhé
```bash
git clone https://github.com/nploi/news_crawler.git
cd news_crawler
```
Tiếp nha
``` bash
# Tiếp theo chạy lệnh như sau để hiện thị danh sách website để khai thác
scrapy list
```
Output sẽ là
```bash
baomoi
vnexpress
```
Chọn vnexpress nhé, baomoi mình chưa tích hợp xong :)), bây giờ bạn có thể chọn chủ đề hoặc bỏ trống thì tool crawl hết chủ đề :v.
```bash
# nếu chạy command line này thì sẽ crawl hết chủ đề nhé
scrapy crawl vnexpress -a category=the-thao -a limit=5
```
OK, chúc mừng bạn đã chạy thành công, hy vọng là vậy =]], vào thư mục `vnexpress/Thể thao/` và xem thành quả của mình nào :v

Giải thích các tham số:
- category: Chủ đề để crawl, có thể bỏ trống. Các chủ đề
    * giao-duc
    * suc-khoe
    * khoa-hoc
    * giai-tri
    * the-thao
    * doi-song
    * du-lich  
- limit: Giới hạn số trang để crawl, có thể bỏ trống. 

**Lưu ý là** : các tham số trên mình chỉ hổ trợ cho VnExpress
