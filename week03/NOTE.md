学习笔记
# 多进程
```python
from multiprocessing import Process
def f(name):
    print(f'hello {name}')
p = Process(target=f, args=('john',))
p.start()
p.join()
```
- target: 表示调用对象，你可以传入方法的名字
- args: 表示被调用对象的位置参数元组，比如target是函数a，他有两个参数m，n，那么args就传入(m, n)即可

# 进程间通信
## Queue
注意引入进程中的Queue
```python
from multiprocessing import Queue
```
- Queue 类是一个近似 queue.Queue 的克隆
- 现在有这样一个需求：我们有两个进程，一个进程负责写(write)一个进程负责读(read)。
- 当写的进程写完某部分以后要把数据交给读的进程进行使用
- write()将写完的数据交给队列，再由队列交给read()

## Pipe 
Pipe() 函数返回一个由管道连接的连接对象，默认情况下是双工（双向）
```python
from multiprocessing import Process, Pipe
def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
```
- 返回的两个连接对象 Pipe() 表示管道的两端。
- 每个连接对象都有 send() 和 recv() 方法（相互之间的）。
- 请注意，如果两个进程（或线程）同时尝试读取或写入管道的 同一 端，
- 则管道中的数据可能会损坏。当然，同时使用管道的不同端的进程不存在损坏的风险。

# 进程锁
```python
import multiprocessing as mp
l = mp.Lock() # 定义一个进程锁
l.acquire() # 锁住
l.release() # 释放
```

# 进程池
Pool 类表示一个工作进程池
如果要启动大量的子进程，可以用进程池的方式批量创建子进程
```python
from multiprocessing.pool import Pool
from time import sleep, time
import random
import os

def run(name):
    print("%s子进程开始，进程ID：%d" % (name, os.getpid()))
    start = time()
    sleep(random.choice([1, 2, 3, 4]))
    end = time()
    print("%s子进程结束，进程ID：%d。耗时0.2%f" % (name, os.getpid(), end-start))

if __name__ == "__main__":
    print("父进程开始")
    # 创建多个进程，表示可以同时执行的进程数量。默认大小是CPU的核心数
    p = Pool(4)
    for i in range(10):
        # 创建进程，放入进程池统一管理
        p.apply_async(run, args=(i,))
    # 如果我们用的是进程池，在调用join()之前必须要先close()，
    # 并且在close()之后不能再继续往进程池添加新的进程
    p.close()
    # 进程池对象调用join，会等待进程池中所有的子进程结束完毕再去结束父进程
    p.join()
    print("父进程结束。")
    p.terminate()
```
- close()：如果我们用的是进程池，在调用join()之前必须要先close()，
- 并且在close()之后不能再继续往进程池添加新的进程
- join()：进程池对象调用join，会等待进程池中所有的子进程结束完毕再去结束父进程
- terminate()：一旦运行到此步，不管任务是否完成，立即终止。

# 多线程
## 多线程函数调用
```python
import threading

# 这个函数名可随便定义
def run(n):
    print("current task：", n)

if __name__ == "__main__":
    t1 = threading.Thread(target=run, args=("thread 1",))
    t2 = threading.Thread(target=run, args=("thread 2",))
    t1.start()
    t2.start()
```
## 多线程类调用
```python
import threading

class MyThread(threading.Thread):
    def __init__(self, n):
        super().__init__() # 重构run函数必须要写
        self.n = n

    def run(self):
        print("current task：", self.n)

if __name__ == "__main__":
    t1 = MyThread("thread 1")
    t2 = MyThread("thread 2")

    t1.start()
    t2.start()
    # 将 t1 和 t2 加入到主线程中
    t1.join()
    t2.join()
```
# 线程锁
```python
import threading

mutex = threading.Lock()

if mutex.acquire(1):    # 加锁 
    print('执行操作')
mutex.release()   #解锁
```
# 线程通信
## 队列
python的数据类型Queue，注意这里和多进程使用的队列不同。
```python
import queue
```
# 线程池
Pool类
```python
import requests
from multiprocessing.dummy import Pool as ThreadPool

urls = [
   'http://www.baidu.com',
   'http://www.sina.com.cn',
   'http://www.163.com',
   'http://www.qq.com',
   'http://www.taobao.com',            
   ]

# 开启线程池
pool = ThreadPool(4)
# 获取urls的结果
results = pool.map(requests.get, urls)
# 关闭线程池等待任务完成退出
pool.close()
pool.join()

for  i in results:
    print(i.url)
```