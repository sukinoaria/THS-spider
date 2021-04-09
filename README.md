# THS-spider
### 说明

- 本项目用于爬取同花顺网站中上市公司财务报表数据，以便在data2text任务中应用，网站上示例图片如图：![示例](data-example.png)

- 使用方法：先用浏览器访问同花顺，拿到cookie后修改`main.py`中请求头的Cookie，开启爬虫。
- 为处理cookie过期的问题，使用selenium控制浏览器重新访问来获得新的session（PS:该方法有时候会失效，导致一直使用selenium爬取数据，效率较低）
- 为了避免被网站识别出selenium，需要对其启动的chrome进行伪装，具体见`main.py`的48-62行。
- selenium需要结合webdriver来使用。[webdriver使用方法](https://blog.csdn.net/weixin_44613063/article/details/86758576)
- 后续可能要做的改进：
  - 换用headless的浏览器
  - 处理selenium遇到滑块验证的问题[解决方法](https://blog.csdn.net/u012067766/article/details/79793264)