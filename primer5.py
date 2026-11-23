# Пример 5. Дедлок (взаимная блокировка) и его решение
import threading
import time

lock_a = ("A", threading.Lock())
lock_b = ("B", threading.Lock())


def worker(name, first, second):
    with first[1]:
        print(f"{name}: взял замок {first[0]}")
        time.sleep(0.5)
        print(f"{name}: жду замок {second[0]}...")
        
        if second[1].acquire(timeout=2):
            try:
                print(f"{name}: взял оба замка, работаю")
            finally:
                second[1].release()
        else:
            print(f"{name}: ДЕДЛОК! замок {second[0]} так и не освободился")
            time.sleep(0.5)

def run(order1, order2, title):
    print(f"--- {title} ---")
    t1 = threading.Thread(target=worker, args=("Поток 1", *order1))
    t2 = threading.Thread(target=worker, args=("Поток 2", *order2))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print()


run((lock_a, lock_b), (lock_b, lock_a), "Дедлок: разный порядок захвата")

run((lock_a, lock_b), (lock_a, lock_b), "Решение: одинаковый порядок захвата")