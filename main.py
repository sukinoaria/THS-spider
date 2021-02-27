import time

import requests
from bs4 import BeautifulSoup


def execute(bizdate, *args, **kwargs):
    for name, base_url in BASE_URl.items():
        # 爬取数据的存储路径
        dt_path = '/data/%s_%s.csv' % (bizdate, name)

        with open(dt_path, "a+") as f:
            # 记录数据文件的当前位置
            pos = f.tell()
            f.seek(0)
            lines = f.readlines()
            # 读取文件中的全部数据并将第一列存储下来作为去重依据，防止爬虫意外中断后重启程序时，重复写入相同
            crawled_list = list(map(lambda line: line.split(",")[0], lines))
            f.seek(pos)
            # 循环500次，从第一页开始爬取数据，当页面没有数据时终端退出循环
            for i in range(1, 500):
                print("start crawl %s, %s" % (name, base_url % i))
                web_source = requests.get(base_url % i, headers=REQUEST_HEADER)
                soup = BeautifulSoup(web_source.content.decode("gbk"), 'lxml')
                table = soup.select('.J-ajax-table')[0]
                tbody = table.select('tbody tr')
                # 当tbody为空时，则说明当前页已经没有数据了，此时终止循环
                if len(tbody) == 0:
                    break
                for tr in tbody:
                    fields = tr.select('td')
                    # 将每行记录第一列去掉，第一列为序号，没有存储必要
                    record = [field.text.strip() for field in fields[1:]]
                    # 如果记录还没有写入文件中，则执行写入操作，否则跳过这行写入
                    if record[0] not in crawled_list:
                        f.writelines([','.join(record) + '\n'])
                # 同花顺网站有反爬虫的机制，爬取速度过快很可能被封
                time.sleep(1)


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
    code = "000032"
    t(code)
