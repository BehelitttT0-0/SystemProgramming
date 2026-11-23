# Задание 1. Имитация авторизации
import asyncio


async def login_async(user: str, password: str) -> bool:
    """Проверяет логин и пароль с задержкой 1,5 секунды."""
    await asyncio.sleep(1.5)
    return user == "student" and password == "qwerty2026"


async def main():
    print("Проверяем данные для входа...")
    ok = await login_async("student", "qwerty2026")
    print("Вход выполнен" if ok else "Неверный логин или пароль")

    print("Проверяем данные для входа...")
    ok = await login_async("student", "12345")
    print("Вход выполнен" if ok else "Неверный логин или пароль")


asyncio.run(main())
