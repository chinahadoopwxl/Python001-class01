import sys, os
sys.path.append(os.path.abspath('..'))
print(sys.path)
from homework2.mysql_manger import SaveMysqlThread
from homework2.position_info import Position, City, CounterOfCity
from homework2.lagou_cookies import CookiesThread
from homework2.lagou_parser import ParserThread
from homework2.lagou_crawl import CrawlThread
from homework2 import lagou_config
from homework2 import global_var
from queue import Queue
import time

if __name__ == "__main__":
    start_time = time.time()
    citys = {'北京': '2', '上海': '3', '广州': '213', '深圳': '215'}

    # 初始化抓取每个城市的职位计数器
    global_var.counter_of_citys = CounterOfCity.get_dict(citys)

    citys_cookies_queue = Queue()    
    page_queue = Queue()
    data_queue = Queue()

    # cookies线程
    cookies_threads = []
    print('开启cookies线程')
    for name, code in citys.items():
        thread = CookiesThread(name + "cookies", City(name, code), citys_cookies_queue)
        thread.start()
        cookies_threads.append(thread)

    # 爬虫线程
    crawl_threads = []
    print('开启爬虫线程')
    for thread_id in citys.keys():
        thread = CrawlThread(thread_id + "_crawl", citys_cookies_queue, page_queue, data_queue)
        thread.start() 
        crawl_threads.append(thread)
    
    # 抓取json数据线程
    print('开启抓取json数据线程')
    parser_threads = []
    for thread_id in range(lagou_config.thread_nums):
        thread = ParserThread(str(thread_id) + "_parser", page_queue, data_queue)
        thread.setDaemon(True)
        thread.start()
        parser_threads.append(thread)

    # 保存到数据库线程
    print('开启save_mysql线程')
    mysql_thread = SaveMysqlThread("save_mysql", data_queue)
    mysql_thread.setDaemon(True)
    mysql_thread.start()

    # 结束cookies线程
    for t in cookies_threads:
        t.join()
    print("cookies线程已完成")

    # 结束crawl线程
    for t in crawl_threads:
        t.join()
    print("爬虫线程已完成")
    
    print("抓取 json 的数据线程读取 page_queue 中的数据")
    page_queue.join()

    print("等待所有数据保存到MySql中")
    data_queue.join()
    print('退出主线程\n')
    sum = 0
    print('拉钩应有数据信息：')
    print(global_var.city_log_info)
    if lagou_config.crawlnum_of_city == 0:
        print('抓取全部数据并去重：')
    else:
        print(f'指定每个城市抓取 {lagou_config.crawlnum_of_city} 条数据并去重：')
    for c in global_var.counter_of_citys.values():
        print(f'{c.city_name} 抓取了 {c.counter} 条数据')
        sum += c.counter
    print(f'总共抓取了 {sum} 条数据')
    print(f'耗时 {time.time() - start_time}')