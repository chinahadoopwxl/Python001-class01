from homework2 import lagou_config, lagou_util, global_var
import threading
import traceback
import requests
import random
import json
import time
import sys

class ParserThread(threading.Thread):
    '''
    解析json数据
    '''
    def __init__(self,thread_id, page_queue, data_queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        while True:
            try:
                pq = self.page_queue.get() # 参数为false时队列为空，抛出异常
                if pq:
                    for city, pn in pq.items():
                        global_var.check_data_lock.acquire(1)
                        if lagou_util.check_data_nums(city):
                            self.parse_position(city, pn)
                        global_var.check_data_lock.release()
            except Exception as e:
                print("ParserThread错误", e)
            finally:
                self.page_queue.task_done() # get之后检测是否会阻塞
            time.sleep(lagou_config.delay())
    
    def parse_position(self, city, pn):
        data={
            'first': True,
            'pn': pn,
            'kd': lagou_config.key_word
        }
        url = f"https://www.lagou.com/jobs/positionAjax.json?city={city.name}&needAddtionalResult=false"
        headers = global_var.citys_headers[city]
        headers["User-Agent"] = lagou_config.user_agent()
        cookies = global_var.citys_cookies[city]
        proxy = lagou_config.proxy()
        result_json = {}
        try:
            response = requests.post(url, headers=headers, data=data, cookies=cookies, proxies=proxy)
            result_json = response.json()
            position_result = result_json["content"]["positionResult"]
            result = position_result["result"]
            result_size = position_result["resultSize"]
            print(f"已抓取 {city.name} 地区，第 {pn} 页，{result_size} 条数据")
            lagou_util.data_entry_queue(city, result, self.data_queue)
        except Exception:
            if not self.process_error(result_json, city, pn):
                traceback.print_exc(file=sys.stdout)

    # 您操作太频繁,请稍后再访问 
    def process_error(self, result_json, city, pn): 
        if not result_json["status"]:
            print(result_json["msg"])
            # 重新获取cookies
            lagou_util.reset_cookies(city)
            print("已清理 cookie 系统会再次尝试爬取")
            self.page_queue.put({city: pn})
            print(f'{city.name}地区第{pn}页数据请求失败，系统将其重新放入page_queue中')
            return True
        return False