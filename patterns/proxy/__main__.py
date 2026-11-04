"""Демо: python -m patterns.proxy"""

import time

from patterns.proxy import machine as module
from patterns.proxy.machine import (
    CoffeeMachine,
    LazyCoffeeMachine,
    LoggingCoffeeMachine,
    RealCoffeeMachine,
    RemoteMenu,
    StaffOnlyCoffeeMachine,
)


def serve(machine: CoffeeMachine, drink: str) -> None:
    """Клиентский код: ему всё равно, настоящая машина перед ним или заместитель."""
    try:
        print("  ", machine.brew(drink))
    except PermissionError as error:
        print("   Отказ:", error)


def main() -> None:
    print("=== Заместитель ===")

    print("\n[Виртуальный заместитель: ленивое создание]")
    lazy = LazyCoffeeMachine()
    print("Заместитель создан, прогревов машины:", RealCoffeeMachine.warmups)
    serve(lazy, "Эспрессо")
    serve(lazy, "Американо")
    print("После двух заказов прогревов машины:", RealCoffeeMachine.warmups)

    print("\n[Защищающий заместитель: проверка прав]")
    serve(StaffOnlyCoffeeMachine(lazy, role="бариста"), "Латте")
    serve(StaffOnlyCoffeeMachine(lazy, role="посетитель"), "Латте")

    print("\n[Заместители можно вкладывать друг в друга]")
    logged = LoggingCoffeeMachine(lazy)
    for drink in ("Капучино", "Раф"):
        serve(StaffOnlyCoffeeMachine(logged, role="управляющий"), drink)
    print("Журнал:", logged.log)

    print("\n[Меню на сервере без кэша]")
    menu = RemoteMenu()
    start = time.perf_counter()
    for drink in ("Латте", "Латте", "Эспрессо", "Латте"):
        menu.get_price(drink)
    print(f"4 запроса цены: {time.perf_counter() - start:.1f} c, обращений к серверу: {menu.requests}")

    # Когда студент добавит CachingMenuProxy, он автоматически появится в демо.
    if hasattr(module, "CachingMenuProxy"):
        print("\n[Меню через CachingMenuProxy]")
        remote = RemoteMenu()
        cached = module.CachingMenuProxy(remote)
        start = time.perf_counter()
        for drink in ("Латте", "Латте", "Эспрессо", "Латте"):
            cached.get_price(drink)
        print(f"4 запроса цены: {time.perf_counter() - start:.1f} c, обращений к серверу: {remote.requests}")


if __name__ == "__main__":
    main()
