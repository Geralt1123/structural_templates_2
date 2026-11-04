"""
Декоратор (Decorator).

Идея: добавлять объекту новое поведение, «оборачивая» его в другой объект
с тем же интерфейсом. Обёрток может быть сколько угодно, и их можно
комбинировать в любом порядке прямо во время работы программы.

Участники:
    Beverage           — Компонент (общий интерфейс напитка)
    Espresso, Americano, Tea — Конкретные компоненты (базовые напитки)
    CondimentDecorator — Базовый декоратор (хранит обёрнутый напиток и всё делегирует ему)
    Milk, Syrup, WhippedCream — Конкретные декораторы (добавки)

Во второй части файла — декораторы функций Python (синтаксис @).
Это та же идея, только оборачивается не объект, а функция.
"""

import functools
from abc import ABC, abstractmethod
from typing import Callable


# ---------------------------------------------------------------------------
# Компонент
# ---------------------------------------------------------------------------

class Beverage(ABC):
    """Любой напиток: базовый или «обёрнутый» добавками."""

    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def cost(self) -> int: ...

    def __str__(self) -> str:
        return f"{self.description()} — {self.cost()} ₽"


# ---------------------------------------------------------------------------
# Конкретные компоненты
# ---------------------------------------------------------------------------

class Espresso(Beverage):
    def description(self) -> str:
        return "Эспрессо"

    def cost(self) -> int:
        return 120


class Americano(Beverage):
    def description(self) -> str:
        return "Американо"

    def cost(self) -> int:
        return 150


class Tea(Beverage):
    def description(self) -> str:
        return "Чай"

    def cost(self) -> int:
        return 100


# ---------------------------------------------------------------------------
# Базовый декоратор
# ---------------------------------------------------------------------------

class CondimentDecorator(Beverage):
    """Добавка к напитку.

    Сама является напитком (наследует Beverage), поэтому её можно снова обернуть.
    По умолчанию просто передаёт вызовы обёрнутому напитку.
    """

    def __init__(self, beverage: Beverage) -> None:
        self._beverage = beverage

    def description(self) -> str:
        return self._beverage.description()

    def cost(self) -> int:
        return self._beverage.cost()


# ---------------------------------------------------------------------------
# Конкретные декораторы
# ---------------------------------------------------------------------------

class Milk(CondimentDecorator):
    def __init__(self, beverage: Beverage, kind: str = "коровье") -> None:
        super().__init__(beverage)
        self.kind = kind

    def description(self) -> str:
        return f"{self._beverage.description()} + молоко ({self.kind})"

    def cost(self) -> int:
        extra = 60 if self.kind != "коровье" else 40  # растительное молоко дороже
        return self._beverage.cost() + extra


class Syrup(CondimentDecorator):
    def __init__(self, beverage: Beverage, flavor: str) -> None:
        super().__init__(beverage)
        self.flavor = flavor

    def description(self) -> str:
        return f"{self._beverage.description()} + сироп ({self.flavor})"

    def cost(self) -> int:
        return self._beverage.cost() + 30


class WhippedCream(CondimentDecorator):
    def description(self) -> str:
        return f"{self._beverage.description()} + взбитые сливки"

    def cost(self) -> int:
        return self._beverage.cost() + 50


# ЗАДАНИЕ (часть 1): добавьте здесь декоратор ExtraShot.


# ---------------------------------------------------------------------------
# Декораторы функций Python
# ---------------------------------------------------------------------------
#
# Запись
#     @takeaway
#     def checkout(beverage): ...
# означает ровно то же, что
#     checkout = takeaway(checkout)
# Функция оборачивается другой функцией с тем же «интерфейсом» (аргументами),
# которая добавляет поведение до или после вызова.

def takeaway(func: Callable[..., int]) -> Callable[..., int]:
    """Добавляет к цене 20 ₽ за стакан с крышкой навынос."""

    @functools.wraps(func)  # сохраняет имя и docstring исходной функции
    def wrapper(*args, **kwargs) -> int:
        return func(*args, **kwargs) + 20

    return wrapper


def checkout(beverage: Beverage) -> int:
    """Цена напитка в зале."""
    return beverage.cost()


@takeaway
def checkout_takeaway(beverage: Beverage) -> int:
    """Цена напитка навынос."""
    return beverage.cost()


# ЗАДАНИЕ (часть 2): добавьте здесь декоратор с параметром discount(percent).


# ---------------------------------------------------------------------------
# ЗАДАНИЕ.
#
#   1. Добавьте класс ExtraShot(CondimentDecorator) — дополнительный шот эспрессо:
#        description() -> "<описание напитка> + доп. шот"
#        cost()        -> цена напитка + 50
#
#   2. Добавьте декоратор функций с параметром discount(percent):
#
#        @discount(10)
#        def checkout_happy_hour(beverage): return beverage.cost()
#
#      Он уменьшает результат функции на percent процентов
#      (округление вниз до целого рубля: 175 * 0.9 = 157.5 -> 157).
#      Не забудьте functools.wraps.
#      Подсказка: discount(10) должен ВЕРНУТЬ обычный декоратор,
#      то есть здесь три вложенные функции.
#
# Проверка: pytest tests/test_decorator.py
# ---------------------------------------------------------------------------
