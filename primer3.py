# Пример 3. Monitor.TryEnter: не ждём вечно, если ресурс занят
import threading
import time

locker = threading.Lock()


def update_rates(name):
    # аналог Monitor.TryEnter(locker, 500, ref lockTaken): ждём не больше 0,5 с
    lock_taken = locker.acquire(timeout=0.5)
    if not lock_taken:
        print(f"{name}: ресурс занят, беру курсы из кэша")  # запасной план (fallback)
        return
    try:
        print(f"{name}: захватил замок, обновляю курсы...")
        time.sleep(1.5)
        print(f"{name}: курсы обновлены")
    finally:
        locker.release()


threads = []
for i in range(1, 4):
    t = threading.Thread(target=update_rates, args=(f"Поток {i}",))
    threads.append(t)
    t.start()
    time.sleep(0.1)

for t in threads:
    t.join()
