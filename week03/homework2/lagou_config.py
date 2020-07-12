from fake_useragent import UserAgent
from homework2.proxy_ip import ProxyIPPool, ProxyIPPool
from homework2 import global_var
import random

host = 'www.lagou.com'
# 抓取数据的线程数
thread_nums = 100
# 限制抓取条数, 0 表示抓取全部数据
crawlnum_of_city = 100
# 搜索 python 相关职位
key_word = 'python' 
# IP代理池
proxy_ip_pool = ProxyIPPool()

def proxy():
    proxy_ip = proxy_ip_pool.random_proxyip()
    return {f'{proxy_ip.protocol}': f'{proxy_ip.protocol}://{proxy_ip.ip}:{proxy_ip.port}'}

def user_agent():
    return UserAgent(verify_ssl=False).random

def delay():
    return random.randint(3, 10)