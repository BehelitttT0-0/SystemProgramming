# Пример 4. Wait/Pulse: Производитель - Потребитель (блокирующая очередь)
import threading
import time
from collections import deque


class BlockingQueue:
    def __init__(self):
        self._queue = deque()
        self._cond = threading.Condition()  # монитор с Wait/Pulse

    def enqueue(self, item):
        with self._cond:
            self._queue.append(item)
            self._cond.notify()             # Monitor.Pulse - будим потребителя

    def dequeue(self):
        with self._cond:
            while not self._queue:          # именно while, а не if
                self._cond.wait()           # Monitor.Wait - спим, пока пусто
            return self._queue.popleft()


queue = BlockingQueue()


def producer():
    for i in range(1, 6):
        time.sleep(0.5)
        order = f"Заказ №{i}"
        print(f"Производитель: добавил {order}")
        queue.enqueue(order)
    queue.enqueue(None)  # сигнал "работа закончена"


def consumer():
    while True:
        item = queue.dequeue()
        if item is None:
            print("Потребитель: заказов больше нет, завершаюсь")
            break
        print(f"Потребитель: обработал {item}")


t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t2.start()
t1.start()
t1.join()
t2.join()
