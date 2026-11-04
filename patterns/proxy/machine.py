"""
Заместитель (Proxy).

Идея: клиент работает не с настоящим объектом, а с его «заместителем»,
у которого тот же интерфейс. Заместитель сам решает, когда и как
передать вызов настоящему объекту: отложить создание, проверить права,
закэшировать ответ, записать в журнал...

Участники (первый пример — кофемашина):
    CoffeeMachine            — Субъект (общий интерфейс)
    RealCoffeeMachine        — Реальный субъект (долго прогревается при создании)
    LazyCoffeeMachine        — Виртуальный заместитель: создаёт машину только при первом заказе
    StaffOnlyCoffeeMachine   — Защищающий заместитель: пускает к машине только персонал
    LoggingCoffeeMachine     — Заместитель-журнал: записывает каждый вызов

Второй пример — меню с ценами, которое хранится на «удалённом сервере»:
    Menu        — Субъект
    RemoteMenu  — Реальный субъект (каждый запрос медленный)
    CachingMenuProxy — кэширующий заместитель (это ваше ЗАДАНИЕ)
"""

import time
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Субъект
# ---------------------------------------------------------------------------

class CoffeeMachine(ABC):
    @abstractmethod
    def brew(self, drink: str) -> str: ...


# ---------------------------------------------------------------------------
# Реальный субъект
# ---------------------------------------------------------------------------

class RealCoffeeMachine(CoffeeMachine):
    """Настоящая кофемашина. Её создание — дорогая операция (прогрев бойлера)."""

    warmups = 0  # сколько раз машину включали (общий счётчик для наглядности)

    def __init__(self) -> None:
        RealCoffeeMachine.warmups += 1
        print("  [машина] прогрев бойлера... готово")

    def brew(self, drink: str) -> str:
        return f"{drink} готов"


# ---------------------------------------------------------------------------
# Заместители
# ---------------------------------------------------------------------------

class LazyCoffeeMachine(CoffeeMachine):
    """Виртуальный заместитель: откладывает создание машины до первого заказа.

    Если за день никто не заказал кофе — машину так и не включили.
    """

    def __init__(self) -> None:
        self._machine: RealCoffeeMachine | None = None

    def brew(self, drink: str) -> str:
        if self._machine is None:
            self._machine = RealCoffeeMachine()
        return self._machine.brew(drink)


class StaffOnlyCoffeeMachine(CoffeeMachine):
    """Защищающий заместитель: к машине допускаются только сотрудники."""

    STAFF_ROLES = {"бариста", "управляющий"}

    def __init__(self, machine: CoffeeMachine, role: str) -> None:
        self._machine = machine
        self._role = role

    def brew(self, drink: str) -> str:
        if self._role not in self.STAFF_ROLES:
            raise PermissionError(f"Роль {self._role!r} не может пользоваться кофемашиной")
        return self._machine.brew(drink)


class LoggingCoffeeMachine(CoffeeMachine):
    """Заместитель-журнал: записывает каждый заказ, затем передаёт его машине."""

    def __init__(self, machine: CoffeeMachine) -> None:
        self._machine = machine
        self.log: list[str] = []

    def brew(self, drink: str) -> str:
        self.log.append(drink)
        return self._machine.brew(drink)


# ---------------------------------------------------------------------------
# Второй пример: меню на удалённом сервере
# ---------------------------------------------------------------------------

class Menu(ABC):
    @abstractmethod
    def get_price(self, drink: str) -> int: ...


class RemoteMenu(Menu):
    """Меню на сервере сети кофеен. Каждый запрос идёт по сети и занимает время."""

    PRICES = {"Эспрессо": 120, "Американо": 150, "Латте": 220, "Капучино": 210}

    def __init__(self, delay: float = 0.3) -> None:
        self.delay = delay
        self.requests = 0  # сколько раз реально сходили на сервер

    def get_price(self, drink: str) -> int:
        self.requests += 1
        time.sleep(self.delay)  # имитация сетевой задержки
        if drink not in self.PRICES:
            raise KeyError(f"Напитка {drink!r} нет в меню")
        return self.PRICES[drink]


# ЗАДАНИЕ: добавьте здесь класс CachingMenuProxy.


# ---------------------------------------------------------------------------
# ЗАДАНИЕ: кэширующий заместитель для меню.
#
#   Добавьте класс CachingMenuProxy(Menu):
#     * __init__(self, menu: Menu) — запоминает настоящее меню;
#     * get_price(self, drink) — при первом запросе напитка спрашивает
#       настоящее меню и запоминает ответ, при повторных возвращает
#       сохранённую цену, не обращаясь к серверу;
#     * clear_cache(self) — забывает все сохранённые цены
#       (например, когда управляющий поменял цены).
#
#   Клиент не должен замечать подмены: у заместителя тот же интерфейс Menu.
#
# Проверка: pytest tests/test_proxy.py
# ---------------------------------------------------------------------------
