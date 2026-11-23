# Самостоятельное задание 6. Менеджер заказов с таймаутом (аналог WhenAny)
import asyncio

WAREHOUSE_DELAY = 3
TIMEOUT = 2


async def check_inventory_async() -> bool:
    await asyncio.sleep(WAREHOUSE_DELAY)
    return True


async def main():
    inventory = asyncio.create_task(check_inventory_async())
    timer = asyncio.create_task(asyncio.sleep(TIMEOUT))

    done, _ = await asyncio.wait({inventory, timer},
                                 return_when=asyncio.FIRST_COMPLETED)

    if inventory in done:
        timer.cancel()
        print("Товар в наличии")
    else:
        inventory.cancel()
        print("Таймаут операции: склад не отвечает")


asyncio.run(main())
