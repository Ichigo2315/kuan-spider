import re
import os
import time

import scrapy
from scrapy import Selector, Request
from xpinyin import Pinyin

from kuan.items import KuanItem

class KuanSpySpider(scrapy.Spider):
    apk_type_list = ['system','desktop','themes','sns','news','network','media',
                      'photography','life','tools','business','finance','sport',
                      'education','trave','shopping']
    name = 'kuan_spy'
    allowed_domains = ['www.coolapk.com']
    start_urls = []
    for apktype in apk_type_list:
            tagged_url = 'https://www.coolapk.com/apk/' + apktype +'/?p=1'
            start_urls.append(tagged_url)
    
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS" :{
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37'

        }
    }

    def getinfo(self,response):#OK
        info = response.css(".apk_topba_message::text").re("\s+(.*?)\s+/\s+(.*?)下载\s+/\s+(.*?)人关注\s+/\s+(.*?)个评论.*?")
        return info

    def gettags(self,response):
        tags = response.css('.apk_left_span2')
        tags = [item.css('::text').extract_first() for item in tags]
        return tags

    def get_perm_and_intro(self,response):
        i = 8
        commented = 1
        sel = Selector(response)
        KuAncomment = sel.css('body > div > div:nth-child(2) > div.app_left > div.apk_left_two > div > div.apk_left_first-title').extract_first().split('\n')[1]
        #i表示应用权限的div序号,如果有"酷安点评"板块则 i=8,否则为7或6
        
        if "应用截图" in KuAncomment :
            i -= 1
            commented = 0
        
        intro_text = str(response.xpath(f'/html/body/div/div[2]/div[2]/div[2]/div/div[{3+commented}]/div').get())

        #处理获得的字符串
        intro_text = intro_text.replace('class="apk_left_title_info"','')
        intro_text = intro_text.replace('<','')
        intro_text = intro_text.replace('>','')
        intro_text = intro_text.replace('/','')
        intro_text = intro_text.replace('br','')
        intro_text = intro_text.replace('div','')
        intro_text = intro_text.replace('\xa0','')
        intro_text = intro_text.strip()
        intro_text = intro_text.strip('p')
 
        #如果没有分类标签则i--
        indic = True if response.xpath(f'/html/body/div/div[2]/div[2]/div[2]/div/div[{i+1}]').get() is not None else False
        if not indic: i -= 1

        plist = sel.css(f'body > div > div:nth-child(2) > div.app_left > div.apk_left_two > div > div:nth-child({i}) > div')
        #body > div > div:nth-child(2) > div.app_left > div.apk_left_two > div > div:nth-child(8) > div
        perms = plist.extract_first().split('\n')
        res_perm = []
        for perm in perms[1:-1]:
            perm = str(perm).strip()
            perm = str(perm).replace('<br>','')
            perm = str(perm).replace('· ','')
            if perm != '': res_perm.append(perm)
        return res_perm , intro_text

    def getdownloadurl(self,response):
        durl = response.css(".show-discalog::attr('href')").extract_first()
        return durl
    
    def parse_url(self,response):
        item = KuanItem()
        p = Pinyin()

        head = 'https://www.coolapk.com/apk/'
        item['apkname'] = str(response.url).replace(head,'')
        item['origin'] = response.url

        body_text = response.body.decode(response.encoding)
        item['update_time'] = re.findall(r"更新时间：(.*)?[<]",body_text)[0]
        item['developer_name'] = str(re.findall(r"开发者名称：(.*)?[<]", body_text)[0]).strip()

        item['title'] = response.css(".detail_app_title::text").extract_first()
        item['pinyin'] = p.get_pinyin(item['title'],'-')

        info = self.getinfo(response)        
        item['volume'] = info[0]
        item['downloads'] = info[1]
        item['follow'] = info[2]
        item['comment'] = info[3]

        item['tags'] = self.gettags(response)
        
        item['rank_num'] = response.css('.rank_num::text').extract_first()
        item['rank_num_users'] = response.css('.apk_rank_p1::text').re("共(.*?)个评分")[0]

        item['permissions'],item['intro'] = self.get_perm_and_intro(response)

        yield item

    def parse(self, response):
        list_apps = response.css(".app_list_left>a")
        for app in list_apps:
            apkname = app.css("::attr('href')").extract_first()
            tar_url = 'https://www.coolapk.com' + apkname
            yield scrapy.Request(url=tar_url,callback=self.parse_url)

'''
        list_items = response.css(".app_left_list>a")
        for item in list_items:
            apkname = item.css("::attr('href')").extract_first()
            url = response.urljoin(apkname)
            yield scrapy.Request(url=url,callback=self.parse_url)
            
        next_page = response.css('.pagination li:nth-child(8) a::attr(href)').extract_first()
        next_url = response.urljoin(next_page)
        yield scrapy.Request(url=next_url, callback=self.parse)
'''

