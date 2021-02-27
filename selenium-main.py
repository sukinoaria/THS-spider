import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#url = "http://stockpage.10jqka.com.cn/000034/finance/"
url = "http://basic.10jqka.com.cn/000034/finance.html#stockpage"

options = Options()
options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"')


options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)

#download path
if not os.path.exists("download/"):
    os.mkdir("download/")
prefs = {"download.default_directory" : "download/"}
options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(chrome_options=options)

driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                       "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})


driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


driver.get(url)
time.sleep(5)
# print(driver.page_source)

res = driver.find_elements_by_xpath('//*[@id="dataifm"]')

print(".....")
print(res)

driver.nav
