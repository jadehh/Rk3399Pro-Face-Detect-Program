# 首先实现一个数组

class Array(object):
    def __init__(self,size = 32):
        self._size = size
        self._items = [None] * size  # 容器_items, 是一个每个值为None的列表


    def __getitem__(self, index):      # 实现下标访问
        return self._items[index]


    def __setitem__(self, index, value):
        self._items[index] = value


    def __len__(self):
        return self._size


    def clear(self, value=None):
        for i in range(len(self._items)):
            self._items[i] = value


    def __iter__(self):
        for item in self._items:
            yield item


class ArrayQueue(object):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.array = Array(maxsize)
        self.head = 0
        self.tail = 0


    def push(self, value):
        if len(self) > self.maxsize:
            raise Exception('queue full')

        self.array[self.head % self.maxsize] = value
        self.head += 1


    def pop(self):
        value = self.array[self.tail % self.maxsize]
        self.tail += 1
        return value

    def __getitem__(self, index):      # 实现下标访问
        return self.array.__getitem__(index)

    def __len__(self):
        return self.head - self.tail
