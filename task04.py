# Task 4 - the negative balance in production
#
# 4.1 Wrong type (10.5, "5", True) -> TypeError, because the type is wrong.
#     Right type but bad value (-10, 0) -> ValueError.
#     deposit(True) is NOT accepted: I check type(amount) is int, and
#     type(True) is bool, so it gives TypeError.
# 4.3 Refund is a third kind of entry. The balance goes up like in a deposit,
#     but the reason is different (money returned for a payment, not new money
#     from outside). History must know the difference for reports and audit.
# 4.4 0.1 + 0.2 == 0.30000000000000004 (floats are binary and can not keep
#     0.1 exactly). Int tiyin is exact: 10 + 20 == 30, no fractions at all.

import pytest


class InsufficientFundsError(ValueError):
    pass


class Wallet:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self._balance = 0  # in tiyin
        self._history = []

    @property
    def balance(self):
        return self._balance

    @property
    def history(self):
        # tuple, so nobody can change it from outside
        return tuple(self._history)

    def deposit(self, amount):
        self._check_amount(amount)
        self._change("deposit", amount, amount)

    def withdraw(self, amount):
        self._check_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError("not enough money")
        self._change("withdraw", amount, -amount)

    def refund(self, amount):
        self._check_amount(amount)
        self._change("refund", amount, amount)

    def _check_amount(self, amount):
        if type(amount) is not int:  # also rejects True/False
            raise TypeError("amount must be int")
        if amount <= 0:
            raise ValueError("amount must be positive")

    def _change(self, kind, amount, delta):
        self._balance += delta
        self._history.append((kind, amount, self._balance))


def test_deposit_and_withdraw():
    w = Wallet(1)
    w.deposit(1000)
    w.withdraw(300)
    assert w.balance == 700


def test_history_entries():
    w = Wallet(1)
    w.deposit(1000)
    w.withdraw(300)
    w.refund(50)
    assert w.history == (
        ("deposit", 1000, 1000),
        ("withdraw", 300, 700),
        ("refund", 50, 750),
    )


def test_admin_script_line_fails():
    w = Wallet(1)
    w.deposit(1000)
    with pytest.raises(AttributeError):
        w.balance -= 500
    assert w.balance == 1000


def test_cannot_go_below_zero():
    w = Wallet(1)
    w.deposit(100)
    with pytest.raises(InsufficientFundsError):
        w.withdraw(101)
    assert w.balance == 100
    assert len(w.history) == 1  # failed call is not in history


def test_wrong_types():
    w = Wallet(1)
    for bad in (10.5, "10", None, True):
        with pytest.raises(TypeError):
            w.deposit(bad)


def test_wrong_values():
    w = Wallet(1)
    for bad in (-10, 0):
        with pytest.raises(ValueError):
            w.deposit(bad)
        with pytest.raises(ValueError):
            w.withdraw(bad)


def test_history_is_read_only():
    w = Wallet(1)
    w.deposit(100)
    with pytest.raises(AttributeError):
        w.history.append(("x", 1, 1))
    with pytest.raises(TypeError):
        w.history[0] = ("x", 1, 1)
    with pytest.raises(AttributeError):
        w.history = []
    assert len(w.history) == 1


def test_balance_never_negative_in_random_calls():
    import random

    random.seed(1)
    w = Wallet(1)
    for _ in range(500):
        action = random.choice([w.deposit, w.withdraw, w.refund])
        try:
            action(random.randint(-50, 200))
        except ValueError:
            pass
        assert w.balance >= 0


def test_float_problem():
    assert 0.1 + 0.2 != 0.3
    assert 10 + 20 == 30
