from homework2 import global_var, lagou_util, lagou_config
import threading
import requests
import traceback
import sys

class CrawlThread(threading.Thread):
    '''
    爬虫类
    '''
    def __init__(self, thread_id, citys_cookies_queue, page_queue, data_queue):
        super().__init__() 
        self.thread_id = thread_id
        self.citys_cookies_queue = citys_cookies_queue
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        '''
        重写run方法
        '''
        try:
            self.scheduler(self.citys_cookies_queue.get())
        except Exception as e:
            print("city_cookies_queue.get()出错",e)
        finally:
            self.citys_cookies_queue.task_done()


    # 模拟任务调度
    def scheduler(self, city_cookies):
        for city, cookies in city_cookies.items():
            # print('下载线程为：',self.thread_id," 下载页面：",page)
            url = f"https://www.lagou.com/jobs/positionAjax.json?city={city.name}&needAddtionalResult=false"

            data={
                'first': True,
                'pn': 1,
                'kd': lagou_config.key_word
            }
            proxy = lagou_config.proxy()
            headers = global_var.citys_headers[city]

            try:
                response = requests.post(url, headers=headers, data=data, cookies=cookies, proxies=proxy)
                content = response.json()["content"]
                page_size = content["pageSize"]

                position_result = content["positionResult"]
                total_count = position_result["totalCount"]
                
                max_page = lagou_util.get_max_page(total_count, page_size)

                [self.page_queue.put({city: pn}) for pn in range(2, max_page + 1)]
                global_var.city_log_info += f'{city.name}总共有 {total_count} 条数据\n'
                result = position_result["result"]
                lagou_util.data_entry_queue(city, result, self.data_queue)
                result_size = position_result["resultSize"]
                print(f'已抓取 {city.name} 地区，第 1 页，{result_size} 条数据')
            except Exception as e:
                print('下载出现异常',e)
                traceback.print_exc(file=sys.stdout)
