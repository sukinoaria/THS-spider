import time
import random
import requests
from bs4 import BeautifulSoup


def t(stock_code):
    statements_type = ["main", "debt", "benefit", "cash"]

    base_url = "http://basic.10jqka.com.cn/api/stock/export.php?export={}&type=report&code=688001"

    REQUEST_HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Cookie': 'spversion=20130314; searchGuide=sg; skin_color=black; historystock=300369|*|HK0883|*|HK1810|*|INTC|*|MSFT; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1614342793,1614391027,1614413456,1614422866; reviewJump=nojump; usersurvey=1; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1614430615; v=A8yO724PwCUdt9TZl7MAcsT3nSH9BXCvcqmEcyaN2HcasWIXThVAP8K5VAF1'

    }
    for statement_name in statements_type:
        url = base_url.format(statement_name)
        web_source = requests.get(
            url, headers=REQUEST_HEADER, allow_redirects=True)
        print(web_source.status_code)
        if web_source.status_code == '200':
            with open("{}.xls".format(statement_name), 'wb') as f:
                f.write(web_source.content)
                time.sleep(random.randint(5, 10))

    # soup = BeautifulSoup(web_source.content.decode("utf8"), 'lxml')
    # print(soup)


if __name__ == '__main__':
    code = "000032"
    t(code)
