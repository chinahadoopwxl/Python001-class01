学习笔记
# 一、异常捕获与处理
## 1.异常原理
    1.异常也是一个类
    2.异常捕获过程：
        1.异常类把错误消息打包到一个对象
        2.然后该对象会自动查找到调用栈
        3.直到运行系统找到明确声明如何处理这些类异常的位置
    3.所有异常继承自BaseException
    4.Traceback显示了出错的位置，显示的顺序和异常信息对象传播的方向是相反的
## 2.异常捕获
    try...except 语法
## 3.常见异常
    1. LookupError下的IndexError和KeyError
    2.IOError
    3.NameError
    4.TypeError
    5.AttributeError
    6.ZeroDivisionError
## 4.自定义异常
``` python
class UserInputError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo
```
``` python
# 抛出自定义异常
raise UserInputError('用户输入错误')
```
## 5.with语法
``` python
class Open:
    def __enter__(self):
        print("open")
    
    def __exit__(self, type, value, trace):
        print("close")
    
    def __call__(self):
        pass
with Open() as f:
    pass
```
# 二.反爬虫
## 1.模拟浏览器头部信息
    1.User-Agent
    2.Referer
    3.cookie
## 2.UserAgent库
```python
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
# 随机生成
ua.random
```
## 3.登录获取cookies
### 1.直接请求登录链接
```python
import time
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
headers = {
'User-Agent' : ua.random,
'Referer' : 'https://accounts.douban.com/passport/login_popup?login_source=anony'
}

s = requests.Session()
# 会话对象：在同一个 Session 实例发出的所有请求之间保持 cookie， 
# 期间使用 urllib3 的 connection pooling 功能。
# 向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
login_url = 'https://accounts.douban.com/j/mobile/login/basic'
form_data = {
'ck':'',
'name':'15055495@qq.com',
'password':'',
'remember':'false',
'ticket':''
}

# post数据前获取cookie
pre_login = 'https://accounts.douban.com/passport/login'
pre_resp = s.get(pre_login, headers=headers)

response = s.post(login_url, data=form_data, headers=headers, cookies=s.cookies)

# 登陆后可以进行后续的请求
# url2 = 'https://accounts.douban.com/passport/setting'

# response2 = s.get(url2,headers = headers)
# response3 = newsession.get(url3, headers = headers, cookies = s.cookies)

# with open('profile.html','w+') as f:
    # f.write(response2.text)
```
### 2.使用WebDriver
    由于不能直接请求登录链接，而是由页面js切换到登录界面。这时就用到webdriver来操作浏览器。
```python
from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    # 需要安装chrome driver, 和浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html
    
    browser.get('https://www.douban.com')
    time.sleep(1)

    browser.switch_to_frame(browser.find_elements_by_tag_name('iframe')[0])
    btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    btm1.click()

    browser.find_element_by_xpath('//*[@id="username"]').send_keys('15055495@qq.com')
    browser.find_element_by_id('password').send_keys('test123test456')
    time.sleep(1)
    browser.find_element_by_xpath('//a[contains(@class,"btn-account")]').click()

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:    
    browser.close()
```

## 4.验证码识别
```python
# 先安装依赖库libpng, jpeg, libtiff, leptonica
# brew install leptonica
# 安装tesseract
# brew install  tesseract
# 与python对接需要安装的包
# pip3 install Pillow
# pip3 install pytesseract
import requests
import os
from PIL import Image
import pytesseract

# 下载图片
# session = requests.session()
# img_url = 'https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1320441599,4127074888&fm=26&gp=0.jpg'
# agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# headers = {'User-Agent': agent}
# r = session.get(img_url, headers=headers)

# with open('cap.jpg', 'wb') as f:
#     f.write(r.content)

# 打开并显示文件
im = Image.open('cap.jpg')
im.show()

# 灰度图片
gray = im.convert('L')
gray.save('c_gray2.jpg')
im.close()

# 二值化
threshold = 100
table = []

for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

out = gray.point(table, '1')
out.save('c_th.jpg')

th = Image.open('c_th.jpg')
print(pytesseract.image_to_string(th,lang='chi_sim+eng'))

# 各种语言识别库 https://github.com/tesseract-ocr/tessdata
# 放到 /usr/local/Cellar/tesseract/版本/share/tessdata
```
## 5.自定义中间件&代理IP
### 1.自定义下载中间件,主要重写4个方法
    1.process_request(request, spider)
    2.process_response(request, response, spider)
    3.process_exception(request, exception, spider)
    4.from_crawler(cls, crawler)
### 2.代理IP
```python
# 修改配置文件settings.py,设置HTTP_PROXY_LIST。如下：
# HTTP_PROXY_LIST = [
#     'http://163.125.75.144:9797',
#     'http://188.226.141.211:3128',
#     'http://88.198.24.108:8080',
#     'http://36.94.77.39:8080'
#]
class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, auth_encoding='utf-8', proxy_list = None):
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')  
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')

        return cls(auth_encoding, http_proxy_list)

    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
```
# 三、分布式爬虫
    1.多机之间需要Redis实现队列和管道到共享。
    2.scrapy-redis特点：
        1.使用了RedisSpider类替代类Spider类
        2.Scheduler到queue由Redis实现
        3.item pipline由Redis实现
    3.安装并启动：pip install scrapy-redis