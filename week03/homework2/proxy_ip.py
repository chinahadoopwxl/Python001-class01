from fake_useragent import UserAgent
import threading
import json, requests, random
import telnetlib
import time

class ProxyIPPool():
    
    def __init__(self):
        print('初始化IP代理池...')
        self._pool = set()

        proxys = read_proxy_file("proxy_ip.txt")

        failed_proxys = set()
        for proxy in proxys:
            splits = proxy.split(":")
            protocol = splits[0]
            proxy_ip = splits[1][2:]
            proxy_port = splits[2]
            if exec_telnet(proxy_ip, proxy_port):
                p = ProxyIP(protocol, proxy_ip, proxy_port)
                self._pool.add(p)
            else:
                failed_proxys.add(proxy)
                print(f"删除无效代理IP: {proxy}")
        alive_proxys = proxys - failed_proxys
        with open("proxy_ip.txt", "w+", encoding="utf8") as f:
            for line in alive_proxys:
                f.write(f"{line}\n")

    def random_proxyip(self):
        return random.choice(list(self._pool))
    
    def add(self, proxy_ip):
        if proxy_ip not in self._pool:
            self._pool.add(proxy_ip)
            print('向代理IP池中添加一个代理IP：', proxy_ip)
        else:
            print('代理IP池中已经有此代理IP：', proxy_ip, '无需重复添加')


class ProxyIP():
    '''
    代理ip类
    '''
    def __init__(self, protocol=None, ip=None, port=None):
        self.protocol = protocol
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"{self.protocol}://{self.ip}:{self.port}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __hash__(self):
        return hash(self.protocol + self.ip + self.port)

    @classmethod
    def get_proxy_ip(cls):
        url = "https://ip.jiangxianli.com/api/proxy_ip"
        ua = UserAgent(verify_ssl=False)
        user_agent = ua.random

        proxy_info = json.loads(requests.get(url, headers={"user-agent": user_agent}).text).get("data")

        protocol = proxy_info.get("protocol")
        ip = proxy_info.get("ip")
        port = proxy_info.get("port")
        
        proxys = read_proxy_file("proxy_ip.txt")

        proxy_ip = ProxyIP(protocol, ip, port)
        if str(proxy_ip) not in proxys:
            with open("proxy_ip.txt", "a+", encoding="utf8") as f:
                f.write(f"{proxy_ip}\n")
            print(f"抓取一个免费代理IP：{proxy_ip}")
        else:
            print(f'代理IP {proxy_ip} 已经被抓取过，无需写入本地文件')
        return proxy_ip
    
def exec_telnet(ip, port):
    try:
        telnetlib.Telnet(ip, port=port, timeout=1)
    except Exception:
        # 端口连接失败返回None
        return False
# 连接成功返回port
    return True

def read_proxy_file(filename):
    proxys = set()
    with open(filename, "r", encoding="utf8") as f:
        for line in f.readlines():
            proxys.add(line.rstrip())
    return proxys


if __name__ == "__main__":
    pool = ProxyIPPool()
    for _ in range(10):
       pool.add(ProxyIP.get_proxy_ip())
       time.sleep(3)