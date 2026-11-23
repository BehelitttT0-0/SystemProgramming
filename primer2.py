# Пример 2. Два потока списывают деньги с одного счёта
import threading
import time

balance = 500
locker = threading.Lock()


def withdraw_unsafe(name, amount):
    global balance
    if balance >= amount:        # проверка
        time.sleep(0.1)          # имитация обращения к банку
        balance -= amount        # списание
        print(f"{name}: снял {amount}, остаток {balance}")
    else:
        print(f"{name}: недостаточно средств (остаток {balance})")


def withdraw_safe(name, amount):
    global balance
    locker.acquire()             # Monitor.Enter(locker)
    try:
        if balance >= amount:
            time.sleep(0.1)
            balance -= amount
            print(f"{name}: снял {amount}, остаток {balance}")
        else:
            print(f"{name}: недостаточно средств (остаток {balance})")
    finally:
        locker.release()         # Monitor.Exit(locker)


def run(func, title):
    global balance
    balance = 500
    print(f"--- {title} ---")
    t1 = threading.Thread(target=func, args=("Поток 1", 400))
    t2 = threading.Thread(target=func, args=("Поток 2", 400))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print(f"Итоговый баланс: {balance}\n")


run(withdraw_unsafe, "Без блокировки")
run(withdraw_safe, "С Monitor (Lock)")
