
class Position():
    def __init__(self, city, position_name, salary):
        self.city = city
        self.position_name = position_name
        self.salary = salary

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __hash__(self):
        return hash(self.city.name + self.position_name + self.salary)

class City():
    def __init__(self, name, code, position_set=set()):
        self.name = name
        self.code = code
        self.position_set = position_set

    def position_counter(self):
        return len(self.position_set)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __hash__(self):
        return hash(self.name + self.code)

import threading
class CounterOfCity():

    def __init__(self, city_name=None):
        self.counter = 0
        self.city_name = city_name
        self._lock = threading.Lock() if city_name else None

    def counting(self):
        if self._lock.acquire(1):
            self.counter += 1
        self._lock.release()
    
    @classmethod
    def get_dict(cls, citys):
        _dict = {}
        for name in citys:
            _dict[name] = CounterOfCity(name)
        return _dict

if __name__ == "__main__":
    citys = {'北京': '2', '上海': '3', '广州': '213', '深圳': '215'}
    c = CounterOfCity.get_dict(citys)

    print(c['北京'].counter)
    c['北京'].counting()
    print(c['北京'].counter)