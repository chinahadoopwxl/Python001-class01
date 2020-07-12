from homework2 import lagou_config, global_var
import threading
import requests

class CookiesThread(threading.Thread):
    '''
    获取cookie类
    '''
    def __init__(self, thread_id, city, citys_cookies_queue):
        super().__init__() 
        self.thread_id = thread_id
        self.city = city
        self.citys_cookies_queue = citys_cookies_queue
        self.jobs_url = f"https://www.lagou.com/jobs/list_{lagou_config.key_word}/p-city_{city.code}?&cl=false&fromSearch=true&labelWords=&suginput="
        self.headers = {
            "User-Agent": lagou_config.user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Host": lagou_config.host,
            "Origin": "https://" + lagou_config.host + "/", 
            "referer": self.jobs_url, 
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
    
    def run(self):
        '''
        重写run方法
        '''
        self.set_cookie()
    
    def set_cookie(self):
        s = requests.session()
        s.get(self.jobs_url, headers=self.headers)
        self.citys_cookies_queue.put({self.city: s.cookies})

        global_var.citys_cookies[self.city] = s.cookies
        global_var.citys_headers[self.city] = self.headers

        s.keep_alive = False
