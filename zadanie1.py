# Задание 1. Защита записи в общий список auditLog через lock
import threading

THREADS = 10
RECORDS_PER_THREAD = 1000

audit_log = []                  # общий список
log_lock = threading.Lock()     # замок для списка


def write_operations(thread_id):
    for i in range(RECORDS_PER_THREAD):
        with log_lock:          # аналог lock (_lock) { ... }
            audit_log.append(f"Запись {len(audit_log) + 1}: поток {thread_id}, операция {i}")


threads = [threading.Thread(target=write_operations, args=(n,)) for n in range(1, THREADS + 1)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Ожидалось записей: {THREADS * RECORDS_PER_THREAD}")
print(f"Получено записей:  {len(audit_log)}")
print(f"Последняя запись:  {audit_log[-1]}")
