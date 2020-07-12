
import threading
import pymysql

class SaveMysqlThread(threading.Thread):
    '''
    页面内容分析
    '''
    def __init__(self, thread_id, data_queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.data_queue = data_queue
    
    def run(self):
        '''
        重写run方法
        '''
        while True:
            if not self.data_queue.empty():
                data = self.data_queue.get()  
                self.save_data(data)
                self.data_queue.task_done()

    def save_data(self, data):
        LagouPipeline().process_item([(data.city.name, data.position_name, data.salary)])
            

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'root',
    'db' : 'lagou',
    'charset' : 'utf8'
}

class LagouPipeline():
    def __init__(self):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.charset = dbInfo['charset']
    
    def process_item(self, items):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db,
            charset = self.charset
        )
        cur = conn.cursor()

        insert_sql = "insert into lagou_position(city_name, position_name, salary) VALUES (%s, %s, %s)"

        try:
            cur.executemany(insert_sql, items)
            cur.close()
            conn.commit()
        except Exception as e:
            print("执行插入语句时，发生错误：", e)
            conn.rollback()
        finally:
            conn.close()