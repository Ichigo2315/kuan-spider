import os
import time

from itemadapter import ItemAdapter
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

driver_path = r"F:\\geckodriver-v0.31.0-win64\\geckodriver.exe"
dl_dir = 'C:\\Users\\Namophobia\\Downloads'
service = Service(executable_path = driver_path)
options = webdriver.FirefoxOptions()
pf = webdriver.FirefoxProfile()
pf.set_preference('dom.block_download_insecure',False)
#firefox_dl_path = 'E:/Firefox_dl'
#pf.set_preference('browser.download.dir', firefox_dl_path)
#pf.set_preference('browser.download.folderList',2)
#pf.set_preference('browser.download.manager.showWhenStarting', False)
options.profile = pf

options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('-disable-dev-shm-usage')
#options.add_argument('headless')

def download_by_kuan_url(detail_page_url):
    #tar_site = 'kuan'
    driver = webdriver.Firefox(service = service,options = options)
    driver.get(detail_page_url)
    kuan_download_btn = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div/div/div[1]/a[1]/button')
    kuan_download_btn.click()
    wait_until_fin()
    driver.close()

def wait_until_fin(directory = dl_dir, timeout = 100):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        for fname in files:
            if fname.endswith('.part'):
                dl_wait = True
        seconds += 1

def findnewestfile(file_path = dl_dir):
    filenames = os.listdir(file_path)
    name_ = []
    time_ = []
    for filename in filenames:
        if '.apk' == filename[-4:]:
            c_time = os.path.getctime(file_path+'\\'+filename)
            #name_.append(file_path+'\\'+filename)
            name_.append(filename)
            time_.append(c_time)

    newest_file = name_[time_.index(max(time_))]
    return newest_file

def apkrename(apkdir = dl_dir,app_pinyin = 'Pinyin_Notgiven'):
    oldname = apkdir + os.sep + findnewestfile()
    newname = apkdir + os.sep + app_pinyin + '.apk'
    os.rename(oldname,newname)

class KuanPipeline:
    def process_item(self, item, spider):
        download_by_kuan_url(detail_page_url = item['origin'])
        apkrename(app_pinyin = item['pinyin'])
        return item