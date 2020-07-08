from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from eprogress import LineProgress
from ping3 import ping
import os
import sys
import traceback
import argparse
import time
import telnetlib
import json

class Pmap():
    def __init__(self, m, n, f, ip, w, v):
        self.m = m
        self.n = n
        self.f = f
        self.ip = ip
        self.w = w
        self.v = v
        self.start_time = time.time() if v else None
        self.result = None
    
    def run(self):
        if self.f == 'ping':
            try:
                self.ping()
            except PermissionError:
                print("权限不够，请使用root用户或者sudo命令执行.")
                print("例如: sudo python3 pmap.py -n 255 -f ping -ip 192.168.0.1-192.168.0.255 -v -m thread -w ping_thread_result.json")
                exit(0)
            except Exception:
                traceback.print_exc(file=sys.stdout)
            print("\nping result:", self.result)

        if self.f == 'tcp':
            try:
                self.telnet()
            except Exception:
                traceback.print_exc(file=sys.stdout)
                exit(0)
            print("\ntelnet result:", self.result)

        if self.w and self.result:
            print('start write json file ...')
            self.write_json()
            print('write success.')

        if self.v:
            print("耗时：", self.use_times())

    def ping(self):
        result_data = {'ip': []}

        iplist = self.parse_ip_list()
        total = len(iplist)
        print(total)

        # 实例化执行ping命令的进度条
        progress = Progress(title='ping progress', total=total)

        for ping_result in self.get_executor().map(self.exec_ping, iplist):
            progress.show_progress()

            flag = ping_result[0]
            ip = ping_result[1]

            if flag: result_data['ip'].append(ip)

        self.result = result_data
    
    def parse_ip_list(self):
        iplist = []

        if '-' in self.ip:
            two_ips = self.ip.split('-')

            split_idx = two_ips[0].rindex('.')
            pre_ip = two_ips[0][:split_idx + 1]

            _min = two_ips[0][split_idx + 1:]
            _max = two_ips[1].split('.')[-1]

            for i in range(int(_min), int(_max) + 1):
                new_ip = pre_ip + str(i)
                iplist.append(new_ip)
        else:
            iplist.append(self.ip)

        return iplist

    def exec_ping(self, ip):
        flag = False 
        # 成功后返回延迟秒数，失败返回None或者False
        try:
            p = ping(ip)
            if p: flag = True 
        except Exception as e:
            raise e

        # 成功后 code 为 0
        # code = os.system(f'ping -c 1 {ip} > /dev/null 2>&1')
        # flag = not code

        return (flag, ip)

    def get_executor(self):
        print(f"开启 {self.n} 个进程..." if self.m == 'proc' else f"开启 {self.n} 个线程...")
        return ProcessPoolExecutor(self.n) if self.m == 'proc' else ThreadPoolExecutor(self.n)
      
    def telnet(self):
        result_data = {'ip': self.ip,'port': []}
        # 端口个数
        total = 65535
        # 实例化执行tcp命令的进度条
        progress = Progress(title='telnet progress', total=total)
        for telnet_result in self.get_executor().map(self.exec_telnet, range(1, total + 1)):
            progress.show_progress()
            if telnet_result: result_data['port'].append(telnet_result)
        self.result = result_data
    
    def exec_telnet(self, port):
        try:
            telnetlib.Telnet(self.ip, port=port, timeout=1)
        except Exception:
            # 端口连接失败返回None
            return
        # 连接成功返回port
        return port

    def write_json(self):
        with open(self.w, 'w+', encoding='utf8') as f:
            f.write(json.dumps(self.result))

    def use_times(self):
        return time.time() - self.start_time if self.start_time else None

class Progress():
    def __init__(self, title, total):
        self._counter = 0
        self.total = total
        self.progress = LineProgress(title=title)
    
    def show_progress(self):
        self._counter += 1
        self.progress.update(int(self._counter / self.total * 100))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", required=False, type=str, default='proc', choices=['proc', 'thread'], help="通过参数 [-m proc|thread] 指定扫描器使用多进程或多线程模型。")
    parser.add_argument("-n", required=True, type=int, default=1, help="参数 并发数量。")
    parser.add_argument("-f", required=True, type=str, choices=['ping', 'tcp'], help="ping 进行 ping 测试， -f tcp 进行 tcp 端口开放、关闭测试。")
    parser.add_argument("-ip", required=True, type=str, help="连续 ip 地址支持 192.168.0.1-192.168.0.100 写法。")
    parser.add_argument("-w", required=False, type=str, help="file name")
    parser.add_argument("-v", required=False, action='store_true', help="增加 -v 参数打印扫描器运行耗时 (用于优化代码)。")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    Pmap(args.m, args.n, args.f, args.ip, args.w, args.v).run()
    # sudo python3 pmap.py -n 255 -f ping -ip 192.168.0.1-192.168.0.255 -v -m proc -w ping_proc_result.json
    # sudo python3 pmap.py -n 255 -f ping -ip 192.168.0.1-192.168.0.255 -v -m thread -w ping_thread_result.json

    # python3 pmap.py -n 500 -f tcp -ip 192.168.0.1 -v -m proc -w tcp_proc_result.json
    # python3 pmap.py -n 500 -f tcp -ip 192.168.0.1 -v -m thread -w tcp_thread_result.json