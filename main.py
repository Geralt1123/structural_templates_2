"""Запуск демонстраций всех шаблонов: python main.py"""

from patterns.decorator.__main__ import main as decorator_demo
from patterns.proxy.__main__ import main as proxy_demo


def main() -> None:
    for demo in (decorator_demo, proxy_demo):
        demo()
        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
