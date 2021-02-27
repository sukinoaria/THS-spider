import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

statements_type = ["main", "debt", "benefit", "cash"]

base_url = "http://basic.10jqka.com.cn/api/stock/export.php?export={}&type=report&code=688001"

options = Options()
options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"')


options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)

# download path
if not os.path.exists("download/"):
    os.mkdir("download/")
prefs = {"download.default_directory": "C:\home\Download\stocks"}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=options)

driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                       "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})


driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

for statement_name in statements_type:
    url = base_url.format(statement_name)
    driver.get(url)
    time.sleep(random.randint(5, 10))
