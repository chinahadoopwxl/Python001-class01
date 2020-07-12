from homework2.position_info import Position
from homework2 import lagou_config
from homework2 import global_var
import requests
import threading

mutex = threading.Lock()
check_nums_lock = threading.Lock()

# 将抓取到到数据放入队列中
def data_entry_queue(city, result, data_queue):
    for item in result:
        p = Position(city, item["positionName"], item["salary"])
        drop_duplicate(p, data_queue)

def check_data_nums(city):
    if lagou_config.crawlnum_of_city == 0:
        return True
    nums = global_var.counter_of_citys[city.name].counter
    return nums != lagou_config.crawlnum_of_city

# 相同地区、相同职位及相同待遇的职位需去重。
def drop_duplicate(p, data_queue):
    if mutex.acquire(1):
        if p not in global_var.position_set:
            # 如果已抓取条数和目标条数不相等，继续将数据放入data_queue
            if  check_data_nums(p.city):     
                data_queue.put(p)
                global_var.position_set.add(p)
                counter_of_city(p.city)
    mutex.release()

# 每个城市的抓取数据计数器
def counter_of_city(city):
    global_var.counter_of_citys[city.name].counting()

def get_max_page(total, size):
    max_page = total // size
    return max_page + 1 if total % size else max_page

# 重置cookies
def reset_cookies(city):
    jobs_url = f"https://www.lagou.com/jobs/list_python/p-city_{city.code}?&cl=false&fromSearch=true&labelWords=&suginput="
    headers = {
        "User-Agent": lagou_config.user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Host": lagou_config.host,
        "Origin": "https://" + lagou_config.host + "/", 
        "referer": jobs_url, 
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    s = requests.session()
    s.get(jobs_url, headers=headers)

    global_var.citys_cookies[city] = s.cookies
    global_var.citys_headers[city] = headers
    s.keep_alive = False