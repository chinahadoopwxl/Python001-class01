#### 爬虫基础
##### 网络协议
##### 重学前端
##### 爬虫原理
###### 基本原理
* 模拟人类使用浏览器的行为对站点进行操作
* 爬取到页面后分析页面 URI 并遍历所有页面
###### 常见头部
* User-Agent：识别是哪类爬虫
* From：提供爬虫机器人管理者的邮箱地址
* Accept：告知服务器爬虫对哪些资源类型感兴趣
* Referer：相当于包含了当前请求的页面 URI
###### robots.txt：告知爬虫哪些内容不应爬取
* User-agent：允许哪些机器人
* Disallow：禁止访问特定目录
* Crawl-delay：访问间隔秒数
* Allow：抵消 Disallow 指令
* Sitemap：指出站点地图的 URI
#### [Scrapy](https://scrapy.org) 
```
pip3 install scrapy
```
##### 架构介绍
* 引擎（Enfine）
* 调度器（Scheduler）
* 下载器（Downloader）
* 爬虫（Spiders）
* 项目管道（Item Pipeline）
* 下载器中间件（Downloader Middlewares）
* 爬虫中间件（Spider MIddlewares）
##### 数据流程
* Engine 首先打开一个网站及处理该网站的 Spider 并向该 Spider 请求第一个要爬取的 URL
* Engine 从 Spider 获取第一个要爬取的 URL 并通过 Schedule 以 Request 的形式调度
* Engine 向 Schedule 请求下一个要爬取的 URL
* Schedule 返回下一个要爬取的 URL 给 Engine 将 URL 通过 Downloader Middlewares 转发给 Downloader 下载
* 一旦页面下载完毕 Downloader 生成该页面的 Request 并将其通过 Downloader Middlewares 发送给 Engine
* Engine 从 Downloader 中接收到 Response 并将其通过 Spider Middlewares 发送给 Spider 处理
* Spider 处理 Response 并返回提取到的 Item及新的 Request 给 Engine
* Engine 将 Spider 返回的 Item 给 Item Pipeline 将新的 Request 给 Schedule
* 重复以上步骤直到 Schedule 中没有更多的 Request 关闭 Engine 爬虫结束
##### 项目实践
###### 创建项目：scrapy startproject tutorial
* 项目模块文件：tutorial/
1. 爬取处理文件：spiders/
2. 爬取数据结构：items.py
3. 爬取的中间件：middlewares.py
5. 项目配置文件：settings.py
* 部署配置文件：scrapy.cfg
###### 明确目标 -> Item
```
import scrapy


class TutorialItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
```
###### 制作爬虫 -> Spider
* 两件事情
1. 定义爬取网页的动作
2. 分析爬取下来的网页
* 运行流程
1. 以初始的 URL 初始化 Request 并设置回调函数
2. 当 Request 成功请求并返回时 Response 生成并作为参数传给该回调函数
3. 在回调函数内分析返回的网页内容
4. 如果返回的是字典或 Item 对象将返回结果保存到文件
5. 如果返回的是 Request 将执行成功得到的 Response 传递给 Request 中定义的回调函数
6. 重复以上步骤直到完成站点的爬取 
* Selector 的用法
1. 直接使用
2. Scrapy shell：scrapy shell https://...
3. XPath 选择器
4. CSS 选择器
5. 正则匹配
* Spider 类分析
```
cd tutorial
scrapy genspider quotes quotes.toscrape.com
```
```
import scrapy


class QuotesSpider(scrapy.Spider):
    # 每个项目唯一名称
    name = 'quotes'
    # 允许爬取的域名（可选配置）
    allowed_domains = ['quotes.toscrape.com']
    # 起始 URL 列表：没有实现 start_request() 方法时默认开始抓取
    start_urls = ['http://quotes.toscrape.com/']

    # 解析返回的响应、提取数据或进一步生成要处理的请求
    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = TutorialItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        # 通过 CSS 选择器获取下一个页面的链接
        next = response.css('.pager .next a::attr("href")').extract_first()
        # 调用 urljoin() 方法将相对 URL 构造成绝对 URL
        url = response.urljoin(next)
        # 通过 url 和 callback 回调函数构造一个新的请求
        yield scrapy.Request(url=url, callback=self.parse)
```
###### 存储内容
* 运行时存储 -> Feed Exports
1. scrapy crawl quotes -o quotes.json/jl/jsonlines
2. scrapy crawl quotes -o quotes.csv
3. scrapy crawl quotes -o quotes.xml
4. scrapy crawl quotes -o quotes.pickle
5. scrapy crawl quotes -o quotes.marshal
6. scrapy crawl quotes -o ftp://user:pass@ftp.example.com/..
* 使用数据管道 -> Item Pipelines
1. 清理 HTML 数据
2. 验证爬取数据及检查爬取字段
3. 查重并丢弃重复内容
4. 将爬取结果保存到数据库等
```
from scrapy.exceptions import DropItem
import pymongo


class TutorialPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 获取 settings.py 中的配置
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_UTI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db['item.collection'].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
```
```
ITEM_PIPELINES = {
    'tutorial.pipelines.TutorialPipeline': 300,
    'tutorial.pipelines.MongoPipeline': 400,
}
MONGO_URI = 'xxx.xxx.xxx.xxx:27017'
MONGO_DB = 'tutorial'
```