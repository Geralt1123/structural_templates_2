"""Демо: python -m patterns.decorator"""

from patterns.decorator import beverage as module
from patterns.decorator.beverage import (
    Americano,
    Espresso,
    Milk,
    Syrup,
    Tea,
    WhippedCream,
    checkout,
    checkout_takeaway,
)


def main() -> None:
    print("=== Декоратор ===")

    print("\n[Базовые напитки]")
    for drink in (Espresso(), Americano(), Tea()):
        print(drink)

    print("\n[Оборачиваем добавками]")
    latte = Milk(Espresso())
    print(latte)

    # Обёртки можно вкладывать друг в друга в любом количестве.
    fancy = WhippedCream(Syrup(Syrup(Milk(Americano(), "овсяное"), "карамель"), "ваниль"))
    print(fancy)

    # Декоратору всё равно, что внутри: он работает и с чаем.
    print(Milk(Syrup(Tea(), "мёд")))

    print("\n[Каждая обёртка добавляет своё и передаёт вызов дальше]")
    layer = fancy
    while True:
        print(f"  {type(layer).__name__:<13} cost() = {layer.cost()}")
        if not hasattr(layer, "_beverage"):
            break
        layer = layer._beverage

    # Когда студент добавит ExtraShot, он автоматически появится в демо.
    if hasattr(module, "ExtraShot"):
        print("\n[ExtraShot]")
        print(module.ExtraShot(module.ExtraShot(Milk(Espresso()))))

    print("\n[Декораторы функций Python]")
    print("В зале:  ", checkout(latte), "₽")
    print("Навынос: ", checkout_takeaway(latte), "₽")
    print("Имя функции сохранилось благодаря functools.wraps:", checkout_takeaway.__name__)

    if hasattr(module, "discount"):
        @module.discount(10)
        def checkout_happy_hour(beverage):
            return beverage.cost()

        print("Счастливый час (-10%):", checkout_happy_hour(latte), "₽")


if __name__ == "__main__":
    main()
