# Task 1 - the cart that belongs to everybody
#
# 1.2 Both bugs have the same root cause: a mutable object ([]) is created
#     only once (in the class body / in the def line) and then every
#     Cart uses this one same list. So it is shared between all carts.
# 1.3 Fix = create new lists inside __init__ (None as default for coupons).
#     In a dataclass "coupons: list = []" gives ValueError (mutable default
#     is not allowed), so we write field(default_factory=list).
# 1.4 self.items.append(...) does not find "items" on the object, so python
#     takes the class attribute - it is one list for all carts and append
#     changes this list. self.count += 1 reads the class value, but the
#     "=" part creates a new attribute on this one object only.

from dataclasses import dataclass, field

import pytest


# the old code from the ticket, kept only to show the bug
class OldCart:
    items = []

    def __init__(self, user_id, coupons=[]):
        self.user_id = user_id
        self.coupons = coupons

    def add(self, sku, qty=1):
        self.items.append((sku, qty))

    def apply_coupon(self, code):
        self.coupons.append(code)


# fixed version
class Cart:
    def __init__(self, user_id, coupons=None):
        self.user_id = user_id
        self.items = []
        self.coupons = list(coupons) if coupons else []

    def add(self, sku, qty=1):
        self.items.append((sku, qty))

    def apply_coupon(self, code):
        self.coupons.append(code)


# same thing as dataclass
@dataclass
class CartDC:
    user_id: int
    items: list = field(default_factory=list)
    coupons: list = field(default_factory=list)

    def add(self, sku, qty=1):
        self.items.append((sku, qty))

    def apply_coupon(self, code):
        self.coupons.append(code)


# 1.1 test from the ticket
def check_two_carts(cart_class):
    first = cart_class(1)
    second = cart_class(2)
    first.add("A1", 2)
    first.apply_coupon("SALE10")
    assert second.items == []
    assert second.coupons == []


def test_old_cart_is_broken():
    # the same check fails for the old code
    with pytest.raises(AssertionError):
        check_two_carts(OldCart)


def test_cart_not_shared():
    check_two_carts(Cart)


def test_dataclass_cart_not_shared():
    check_two_carts(CartDC)


def test_cart_keeps_its_own_data():
    cart = Cart(1)
    cart.add("A1", 2)
    cart.apply_coupon("SALE10")
    assert cart.items == [("A1", 2)]
    assert cart.coupons == ["SALE10"]


def test_passed_coupons_are_copied():
    codes = ["X"]
    cart = Cart(1, codes)
    cart.apply_coupon("Y")
    assert codes == ["X"]


def test_dataclass_does_not_allow_list_default():
    with pytest.raises(ValueError):

        @dataclass
        class Bad:
            coupons: list = []
