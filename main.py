import os
import time
import json
import random
import requests
from bs4 import BeautifulSoup

class Spider:
    def __init__(self, stock_file, base_url,download_path="download/", proxy_file=None):

        self.stocks = None
        # 初始股票代码文件
        self.stock_file = stock_file
        #已完成的股票
        self.finished_file = "finished_stocks.txt"
        # 爬虫失败的代码文件
        self.failed_file = "failed_stocks.txt"
        # 数据不完整的代码文件
        self.ignored_file = "ignored_stocks.txt"



        self.base_url = base_url

        # 下载路径
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        self.download_path = download_path

        self.proxy_pool = None if not proxy_file else \
            [line.strip() for line in open(proxy_file,'r').readlines()]

        self.REQUEST_HEADER = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Cookie': 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1614327245; spversion=20130314; reviewJump=nojump; searchGuide=sg; historystock=300369%7C*%7C300078%7C*%7C430335; usersurvey=1; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1614495825; v=A9Vpn-8fGS-fbD1TmQ2JaQUI5NqM0onkU4ZtOFd6kcybrv8MHyKZtOPWfQzk'
        }
        self.init_task()

    def init_task(self):
        origin_data = [line.strip() for line in open(self.stock_file,'r').readlines()]
        try:
            finished_data = [line.strip() for line in open(self.finished_file,'r').readlines()]
        except:
            finished_data = []
        try:
            ignored_data = [line.strip() for line in open(self.ignored_file,'r').readlines()]
        except:
            ignored_data = []
        self.stocks = sorted(list(set(origin_data) - set(finished_data) - set(ignored_data)))

    def crawl_once(self,stock_code,idx):
        tgt_url = self.base_url.format(stock_code)
        web_source = requests.get(tgt_url, headers=self.REQUEST_HEADER)
        #save new cookie
        new_cookie = web_source.request.headers['Cookie']
        self.REQUEST_HEADER['Cookie'] = new_cookie

        print("[{}/{}]start crawl stock:{}, STATUS CODE:[{}]".format(idx,len(self.stocks),
                                                                     stock_code,web_source.status_code))
        if web_source.status_code != 200:
            #todo retry mechanism
            print("  ....  Status Code ERROR ........")
            exit(-1)
        soup = BeautifulSoup(web_source.content.decode("gbk"), 'lxml')
        # 判断是否爬取到正确的页面： 包含财务诊断的部分，且没有触发同花顺的反爬验证机制
        if soup.find(id="chartData") and soup.find(id="finance"):
            self.get_data(soup,stock_code)
        elif not soup.find(id="chartData") and not soup.find(id="finance"):
            #可能触发了反爬虫，保存stock code
            with open(self.failed_file,'a') as f:
                f.write(stock_code+"\n")
            print("ERROR: get data for stock:{} error, save stock code to {}".format(stock_code,self.failed_file))
        else:
            # 数据不完整，略过
            with open(self.ignored_file,'a') as f:
                f.write(stock_code+"\n")
            print("IGNORED: cannot get corresponding files for stock:{}, save code to {}".format(stock_code,self.ignored_file))
        # 同花顺网站有反爬虫的机制，爬取速度过快很可能被封
        time.sleep(random.randint(8,20))

    def get_data(self,soup,stock_code):
        stock_info = {}

        # 股票的大体描述
        chart_data = eval(soup.find(id="chartData").attrs['value'])
        stock_info['analysis'] = chart_data[0]['2020-09-30']
        # 股票几个方面的具体数值型分析
        detailed_analysis = {}
        detailed_data = soup.find_all(name='div',attrs={'class':'courier_cont bg-dark'})
        assert len(detailed_data) == 5
        for i in range(5):
            cur_type_data = detailed_data[i].find_all(name="li")
            cur_type = cur_type_data[0].contents[0].attrs['cid']
            cur_data = []
            for _li in cur_type_data:
                cur_data.append(_li.contents[1]) #具体的数值型描述
            detailed_analysis[cur_type] = cur_data
        stock_info['detailed_analysis'] = detailed_analysis
        # 报表数据
        statement_data = soup.find(id='main').contents[0]
        statement_data = statement_data.replace("false","False")
        statement_data = statement_data.replace("true","True")
        stock_info['stock_statements'] = eval(statement_data)
        #save to json file
        with open(os.path.join(self.download_path,"{}.json".format(stock_code)),'w') as f:
            json.dump(stock_info,f,ensure_ascii=False)
        # 成功爬取该股票信息
        with open(self.finished_file,'a') as f:
            f.write(stock_code+"\n")

    def run(self):
        for idx,code in enumerate(self.stocks):
            self.crawl_once(code,idx)
        print("spider run over ... ")


if __name__ == '__main__':
    stock_file = "stocks.txt"
    base_url = "http://basic.10jqka.com.cn/{}/finance.html#stockpage"
    spider = Spider(stock_file,base_url)
    spider.run()
