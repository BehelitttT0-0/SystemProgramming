# Задание 3. Monitor.TryEnter: не допускаем наложения бэкапов
import threading
import time

BACKUP_TIME = 1.2   # создание бэкапа, секунды (1200 мс)
INTERVAL = 0.5      # период таймера, секунды (500 мс)
TRIGGERS = 6        # сколько раз сработает таймер

locker = threading.Lock()
t0 = time.perf_counter()


def now():
    return f"{time.perf_counter() - t0:.1f} с"


def run_backup(n):
    # аналог Monitor.TryEnter(locker, 0, ref lockTaken): не ждём ни миллисекунды
    lock_taken = locker.acquire(blocking=False)
    if not lock_taken:
        print(f"[{now()}] Бэкап №{n} пропущен: предыдущий ещё идёт")
        return
    try:
        print(f"[{now()}] Бэкап №{n} запущен")
        time.sleep(BACKUP_TIME)
        print(f"[{now()}] Бэкап №{n} завершён")
    finally:
        locker.release()   # замок откроется, даже если при записи будет сбой


threads = []
for n in range(1, TRIGGERS + 1):
    t = threading.Thread(target=run_backup, args=(n,))
    threads.append(t)
    t.start()
    time.sleep(INTERVAL)

for t in threads:
    t.join()
