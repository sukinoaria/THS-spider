import os
import time
import random
import requests
from bs4 import BeautifulSoup

class Spider:
    def __init__(self, stock_file, base_url, xls_base_url,xls_download_path="download/", proxy_file=None):
        self.stocks = [line.strip() for line in open(stock_file,'r').readlines()]
        self.base_url = base_url
        self.xls_base_url = xls_base_url

        if not os.path.exists(xls_download_path):
            os.mkdir(xls_download_path)
        self.xls_download_path = xls_download_path

        self.proxy_pool = None if not proxy_file else \
            [line.strip() for line in open(proxy_file,'r').readlines()]

        self.REQUEST_HEADER = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Cookie': 'spversion=20130314; searchGuide=sg; skin_color=black; historystock=300369|*|HK0883|*|HK1810|*|INTC|*|MSFT; usersurvey=1; reviewJump=nojump; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1614391027,1614413456,1614422866,1614437125; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1614437125; v=A9mbgOPs3XJ9hIHmMChNJeHk6M6wZs0Yt1rxrPuOVYB_Avc4Q7bd6EeqAX6I'
        }

    def crawl_once(self,stock_code):

        tgt_url = self.base_url.format(stock_code)
        xls_url = self.xls_base_url.format(stock_code)

        print("start crawl stock:",stock_code)
        web_source = requests.get(tgt_url, headers=self.REQUEST_HEADER)
        print(web_source.status_code)
        if web_source.status_code != "200":
            pass #todo retry mechanism
        soup = BeautifulSoup(web_source.content.decode("gbk"), 'lxml')
        table = soup.select('.J-ajax-table')[0]
        tbody = table.select('tbody tr')
        # 同花顺网站有反爬虫的机制，爬取速度过快很可能被封
        time.sleep(random.randint(4,20))

    def run(self):
        for code in self.stocks:
            self.crawl_once(code)
        print("spider run over ... ")

def t(stock_code):
    base_url = 'http://basic.10jqka.com.cn/'
    #url = base_url + stock_code + '/finance.html'

    url = "http://basic.10jqka.com.cn/api/stock/export.php?export=main&type=report&code=000034"
    #url = "http://d.10jqka.com.cn/v2/realhead/hs_000034/last.js"
    print("URL:", url)
    REQUEST_HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Cookie': 'spversion=20130314; searchGuide=sg; skin_color=black; historystock=300369|*|HK0883|*|HK1810|*|INTC|*|MSFT; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1614342793,1614391027,1614413456,1614422866; reviewJump=nojump; usersurvey=1; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1614430615; v=A8yO724PwCUdt9TZl7MAcsT3nSH9BXCvcqmEcyaN2HcasWIXThVAP8K5VAF1'

    }
    web_source = requests.get(
        url, headers=REQUEST_HEADER, allow_redirects=True)
    print(web_source.status_code)
    with open("python_logo.xls", 'wb') as f:
        f.write(web_source.content)

    # soup = BeautifulSoup(web_source.content.decode("utf8"), 'lxml')
    # print(soup)


if __name__ == '__main__':
    stock_file = "stocks.txt"
    base_url = "http://basic.10jqka.com.cn/{}/finance.html#stockpage"
    xls_base_url = "http://basic.10jqka.com.cn/api/stock/export.php?export=main&type=report&code={}"
    spider = Spider(stock_file,base_url,xls_base_url)
    spider.run()
