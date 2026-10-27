# Task 5 - validation without touching 40 call sites
#
# 5.2 The constructor does self.price = price (not self._price), so it goes
#     through the setter and wrong values are rejected there too.
# 5.3 final_price uses integer math and // so the result is int, rounded down.
# 5.4 If the final price is computed once in __init__ it gets old when the
#     price changes later (see BadProduct below and its test).
# 5.5 sku has only a getter (property without setter), so p.sku = 'X'
#     gives AttributeError.

import pytest


class Product:
    def __init__(self, sku, price, discount_percent=0):
        self._sku = sku
        self.price = price
        self.discount_percent = discount_percent

    @property
    def sku(self):
        return self._sku

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if type(value) is not int:
            raise TypeError("price must be int")
        if value <= 0:
            raise ValueError("price must be greater than 0")
        self._price = value

    @property
    def discount_percent(self):
        return self._discount_percent

    @discount_percent.setter
    def discount_percent(self, value):
        if type(value) is not int:
            raise TypeError("discount must be int")
        if not 0 <= value <= 90:
            raise ValueError("discount must be from 0 to 90")
        self._discount_percent = value

    def final_price(self):
        return self.price * (100 - self.discount_percent) // 100


# the idea from the teammate (5.4)
class BadProduct:
    def __init__(self, sku, price, discount_percent=0):
        self.price = price
        self.discount_percent = discount_percent
        self.final = price * (100 - discount_percent) // 100


def test_old_value_from_task():
    assert Product("A1", 99_990, 15).final_price() == 84_991


def test_final_price_is_int():
    assert type(Product("A1", 99_990, 15).final_price()) is int


def test_price_must_be_positive():
    p = Product("A1", 100_000)
    with pytest.raises(ValueError):
        p.price = 0
    with pytest.raises(ValueError):
        Product("A1", -5)
    assert p.price == 100_000


def test_discount_range():
    p = Product("A1", 100_000)
    with pytest.raises(ValueError):
        p.discount_percent = 150
    with pytest.raises(ValueError):
        p.discount_percent = -1
    with pytest.raises(ValueError):
        Product("A1", 100_000, 91)
    p.discount_percent = 90
    assert p.final_price() == 10_000


def test_wrong_types():
    with pytest.raises(TypeError):
        Product("A1", 99.5)
    with pytest.raises(TypeError):
        Product("A1", True)


def test_old_assignment_still_works():
    p = Product("A1", 100_000, 10)
    p.price = 120_000
    assert p.final_price() == 108_000


def test_sku_read_only():
    p = Product("A1", 100_000)
    with pytest.raises(AttributeError):
        p.sku = "X"
    assert p.sku == "A1"


def test_cached_price_goes_stale():
    p = BadProduct("A1", 100_000, 10)  # final = 90000
    p.price = 200_000
    assert p.final == 90_000  # should be 180000, so this is the bug
