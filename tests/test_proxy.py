import pytest

from patterns.proxy import machine
from patterns.proxy.machine import (
    CoffeeMachine,
    LazyCoffeeMachine,
    LoggingCoffeeMachine,
    Menu,
    RealCoffeeMachine,
    RemoteMenu,
    StaffOnlyCoffeeMachine,
)


@pytest.fixture(autouse=True)
def reset_counter():
    RealCoffeeMachine.warmups = 0
    yield


# ---------------------------------------------------------------------------
# Тесты примера
# ---------------------------------------------------------------------------

def test_proxies_share_interface():
    for proxy in (
        LazyCoffeeMachine(),
        StaffOnlyCoffeeMachine(LazyCoffeeMachine(), "бариста"),
        LoggingCoffeeMachine(LazyCoffeeMachine()),
    ):
        assert isinstance(proxy, CoffeeMachine)


def test_lazy_proxy_creates_machine_on_first_use():
    lazy = LazyCoffeeMachine()
    assert RealCoffeeMachine.warmups == 0
    assert lazy.brew("Эспрессо") == "Эспрессо готов"
    lazy.brew("Латте")
    assert RealCoffeeMachine.warmups == 1


def test_staff_only_proxy():
    guest = StaffOnlyCoffeeMachine(LazyCoffeeMachine(), "посетитель")
    with pytest.raises(PermissionError):
        guest.brew("Латте")
    assert RealCoffeeMachine.warmups == 0, "посетитель не должен даже включить машину"
    assert StaffOnlyCoffeeMachine(LazyCoffeeMachine(), "бариста").brew("Латте") == "Латте готов"


def test_logging_proxy():
    logged = LoggingCoffeeMachine(LazyCoffeeMachine())
    logged.brew("Латте")
    logged.brew("Раф")
    assert logged.log == ["Латте", "Раф"]


def test_remote_menu():
    menu = RemoteMenu(delay=0)
    assert menu.get_price("Латте") == 220
    menu.get_price("Латте")
    assert menu.requests == 2
    with pytest.raises(KeyError):
        menu.get_price("Чайный гриб")


# ---------------------------------------------------------------------------
# Тесты задания (SKIPPED, пока класс не добавлен)
# ---------------------------------------------------------------------------

def _require_proxy():
    cls = getattr(machine, "CachingMenuProxy", None)
    if cls is None:
        pytest.skip("ЗАДАНИЕ: добавьте класс CachingMenuProxy в patterns/proxy/machine.py")
    return cls


def test_task_caching_proxy_is_menu():
    CachingMenuProxy = _require_proxy()
    assert isinstance(CachingMenuProxy(RemoteMenu(delay=0)), Menu), "CachingMenuProxy должен наследовать Menu"


def test_task_caching_proxy_returns_real_prices():
    CachingMenuProxy = _require_proxy()
    proxy = CachingMenuProxy(RemoteMenu(delay=0))
    assert proxy.get_price("Латте") == 220
    assert proxy.get_price("Эспрессо") == 120


def test_task_caching_proxy_caches():
    CachingMenuProxy = _require_proxy()
    remote = RemoteMenu(delay=0)
    proxy = CachingMenuProxy(remote)
    for _ in range(5):
        proxy.get_price("Латте")
    proxy.get_price("Капучино")
    proxy.get_price("Капучино")
    assert remote.requests == 2, "каждый напиток должен запрашиваться у сервера только один раз"


def test_task_caching_proxy_clear_cache():
    CachingMenuProxy = _require_proxy()
    remote = RemoteMenu(delay=0)
    proxy = CachingMenuProxy(remote)
    proxy.get_price("Латте")
    remote.PRICES = {**RemoteMenu.PRICES, "Латте": 250}  # управляющий поднял цену
    assert proxy.get_price("Латте") == 220, "до сброса кэша цена старая"
    proxy.clear_cache()
    assert proxy.get_price("Латте") == 250
    assert remote.requests == 2


def test_task_caching_proxy_does_not_cache_errors():
    CachingMenuProxy = _require_proxy()
    proxy = CachingMenuProxy(RemoteMenu(delay=0))
    with pytest.raises(KeyError):
        proxy.get_price("Чайный гриб")
