from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from eprogress import LineProgress
import os
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
        self.progress = None
        self.i = 0
    
    def run(self):
        if self.f == 'ping':
            # 实例化执行ping命令的进度条
            self.progress = LineProgress(title='ping progress')
            self.ping()
            print("\nping result:", self.result)

        if self.f == 'tcp':
            # 实例化执行tcp命令的进度条
            self.progress = LineProgress(title='tcp progress')
            self.telnet()
            print("\ntelnet result:", self.result)

        if self.w:
            print('start write json file ...')
            self.write_json()
            print('write success.')

        if self.v:
            print("耗时：", self.use_times())

    def show_progress(self, total):
        if self.progress:
            self.progress.update(int(self.i / (total - 1) * 100))
            self.i += 1

    def ping(self):
        result_data = {'ip': []}

        iplist = self.parse_ip_list()
        executor = self.get_executor()
        print("executor:",executor)

        total = len(iplist)
        for ping_result in executor.map(self.exec_ping, iplist):
            self.show_progress(total)
            flag = ping_result[0]
            ip = ping_result[1]
            if not flag:
                result_data['ip'].append(ip)

        self.result = result_data

    def ip_is_list(self):
        return '-' in self.ip
    
    def parse_ip_list(self):
        iplist = []

        if self.ip_is_list():
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
        code = os.system(f'ping -c 1 {ip} > /dev/null 2>&1')
        # 成功后 code 为 0
        return (code, ip)

    def get_executor(self):
        print(f"开启 {self.n} 个进程..." if self.m == 'proc' else f"开启 {self.n} 个线程...")
        return ProcessPoolExecutor(self.n) if self.m == 'proc' else ThreadPoolExecutor(self.n)
      
    def telnet(self):
        result_data = {'ip': self.ip,'port': []}
        executor = self.get_executor()
        # 端口个数
        total = 65535
        for telnet_result in executor.map(self.exec_telnet, range(1, total + 1)):
            self.show_progress(total)
            if telnet_result: result_data['port'].append(telnet_result)
        self.result = result_data
    
    def exec_telnet(self, port):
        try:
            telnetlib.Telnet(self.ip, port=str(port), timeout=0.5)
        except Exception:
            # 连接超时即连接失败返回None
            return
        # 连接成功返回port
        return port

    def write_json(self):
        with open(self.w, 'w+', encoding='utf8') as f:
            f.write(json.dumps(self.result))

    def use_times(self):
        return time.time() - self.start_time if self.start_time else None

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