import pytest

from patterns.decorator import beverage
from patterns.decorator.beverage import (
    Americano,
    Beverage,
    CondimentDecorator,
    Espresso,
    Milk,
    Syrup,
    Tea,
    WhippedCream,
    checkout,
    checkout_takeaway,
    takeaway,
)


# ---------------------------------------------------------------------------
# Тесты примера
# ---------------------------------------------------------------------------

def test_base_beverages():
    assert (Espresso().cost(), Americano().cost(), Tea().cost()) == (120, 150, 100)
    assert Espresso().description() == "Эспрессо"


def test_decorator_is_a_beverage():
    drink = Milk(Espresso())
    assert isinstance(drink, Beverage)
    assert isinstance(drink, CondimentDecorator)


def test_single_decorator():
    drink = Milk(Espresso())
    assert drink.cost() == 160
    assert drink.description() == "Эспрессо + молоко (коровье)"


def test_nested_decorators():
    drink = WhippedCream(Syrup(Syrup(Milk(Americano(), "овсяное"), "карамель"), "ваниль"))
    assert drink.cost() == 150 + 60 + 30 + 30 + 50
    assert drink.description() == (
        "Американо + молоко (овсяное) + сироп (карамель) + сироп (ваниль) + взбитые сливки"
    )


def test_decorator_does_not_change_wrapped_object():
    espresso = Espresso()
    Milk(espresso)
    assert espresso.cost() == 120


def test_function_decorator():
    latte = Milk(Espresso())
    assert checkout(latte) == 160
    assert checkout_takeaway(latte) == 180
    assert checkout_takeaway.__name__ == "checkout_takeaway"
    assert takeaway(lambda: 100)() == 120


# ---------------------------------------------------------------------------
# Тесты задания (SKIPPED, пока код не добавлен)
# ---------------------------------------------------------------------------

def _require(name: str, hint: str):
    obj = getattr(beverage, name, None)
    if obj is None:
        pytest.skip(f"ЗАДАНИЕ: {hint} (patterns/decorator/beverage.py)")
    return obj


def test_task_extra_shot_is_decorator():
    ExtraShot = _require("ExtraShot", "добавьте класс ExtraShot")
    assert issubclass(ExtraShot, CondimentDecorator), "ExtraShot должен наследовать CondimentDecorator"


def test_task_extra_shot_cost_and_description():
    ExtraShot = _require("ExtraShot", "добавьте класс ExtraShot")
    drink = ExtraShot(Americano())
    assert drink.cost() == 200
    assert drink.description() == "Американо + доп. шот"


def test_task_extra_shot_combines():
    ExtraShot = _require("ExtraShot", "добавьте класс ExtraShot")
    drink = Syrup(ExtraShot(ExtraShot(Milk(Espresso()))), "орех")
    assert drink.cost() == 120 + 40 + 50 + 50 + 30
    assert drink.description() == "Эспрессо + молоко (коровье) + доп. шот + доп. шот + сироп (орех)"


def test_task_discount_decorator():
    discount = _require("discount", "добавьте декоратор discount(percent)")

    @discount(10)
    def checkout_happy_hour(drink):
        """Цена в счастливый час."""
        return drink.cost()

    assert checkout_happy_hour(Espresso()) == 108
    assert checkout_happy_hour(Syrup(Espresso(), "мята")) == 135  # 150 * 0.9
    assert checkout_happy_hour(Milk(Espresso(), "овсяное")) == 162  # 180 * 0.9


def test_task_discount_rounds_down():
    discount = _require("discount", "добавьте декоратор discount(percent)")
    assert discount(10)(lambda: 175)() == 157
    assert discount(50)(lambda: 99)() == 49
    assert discount(0)(lambda: 200)() == 200


def test_task_discount_keeps_function_name():
    discount = _require("discount", "добавьте декоратор discount(percent)")

    @discount(20)
    def checkout_student(drink):
        """Скидка для студентов."""
        return drink.cost()

    assert checkout_student.__name__ == "checkout_student", "используйте functools.wraps"
    assert checkout_student.__doc__ == "Скидка для студентов."


def test_task_discount_stacks_with_takeaway():
    discount = _require("discount", "добавьте декоратор discount(percent)")

    @discount(50)
    @takeaway
    def price(drink):
        return drink.cost()

    # сначала +20 за стакан, потом скидка 50%: (120 + 20) * 0.5
    assert price(Espresso()) == 70
