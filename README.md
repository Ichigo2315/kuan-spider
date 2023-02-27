#### 从酷安网爬取apk以及应用信息（基于浏览器自动化工具selenium)



- 使用框架：```scrapy```

```bash
pip install scrapy
```

- Run

```bash
cd kuan
scrapy crawl kuan_spy -o kuan_apps.csv
```



#### 数据内容

```items.py```

```python
import scrapy

class KuanItem(scrapy.Item):
    title = scrapy.Field()								#应用中文名
    volume = scrapy.Field()								#安装包大小
    downloads = scrapy.Field()							#下载量
    follow = scrapy.Field()								#关注人数
    comment = scrapy.Field()							#评论数
    tags = scrapy.Field()								#应用标签，格式为一个list
    rank_num = scrapy.Field()							#评分
    rank_num_users = scrapy.Field()						#点评数
    intro = scrapy.Field()								#应用简介
    apkname = scrapy.Field()							#apk包名
    update_time = scrapy.Field()						#更新时间
    developer_name = scrapy.Field()						#开发者/开发商名称
    download_url = scrapy.Field()						#下载链接
    permissions = scrapy.Field()						#权限信息，格式为一个list
```






#### Environment：
- python >= 3.7
- selenium==4.5.0
- xpinyin
- scrapy
- driver:[geckodriver.exe](https://github.com/mozilla/geckodriver/releases) v0.31.0
- software:[Firefox](https://www.firefox.com.cn/) v105.0.3




一些小问题：

- Firefox profile中的‘browser.download.dir’项不起作用，导致脚本无法指定下载目录，只能下载到默认的C盘
- 点击下载按钮时，有小部分app会跳转到应用宝（下载链接直接定向到应用宝，可能本来就没法从酷安下载）
