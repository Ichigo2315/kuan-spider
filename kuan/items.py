import scrapy

class KuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    pinyin = scrapy.Field()
    origin = scrapy.Field()
    volume = scrapy.Field()
    downloads = scrapy.Field()
    follow = scrapy.Field()
    comment = scrapy.Field()
    tags = scrapy.Field()
    rank_num = scrapy.Field()
    rank_num_users = scrapy.Field()
    intro = scrapy.Field()
    apkname = scrapy.Field()
    update_time = scrapy.Field()
    developer_name = scrapy.Field()
    permissions = scrapy.Field()
