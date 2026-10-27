# Task 2 - three different delivery fees
#
# 2.1 By hand (Checkout / Receipt / Courier), correct answer from the rule in brackets
#     150 000 sum, 4.2 km -> 0 / 15 000 / 0        (correct: 0)      Checkout and Courier are right
#     I ran the old code and got the same numbers.
#     Problems: Receipt uses ">" instead of ">=", int() and round() are not
#     "every started km", and Courier has no rounding at all (float money).
# 2.2 Order has food_total and distance_km, so Order is the expert and
#     it has delivery_fee(). The 3 services just call it.
# 2.3 math.ceil gives the started kilometres.

import math


class Order:
    FREE_FROM = 150_000
    BASE_FEE = 12_000
    BASE_KM = 3
    PER_KM = 3_000  # change to 3_500 here, one line

    def __init__(self, food_total, distance_km):
        self.food_total = food_total
        self.distance_km = distance_km

    def delivery_fee(self):
        if self.food_total >= self.FREE_FROM:
            return 0
        extra_km = max(0, self.distance_km - self.BASE_KM)
        return self.BASE_FEE + math.ceil(extra_km) * self.PER_KM


class CheckoutService:
    def delivery_fee(self, order):
        return order.delivery_fee()


class ReceiptService:
    def delivery_fee(self, order):
        return order.delivery_fee()


class CourierPayoutService:
    def delivery_fee(self, order):
        return order.delivery_fee()


# 2.4 tests
def test_the_three_orders_from_2_1():
    assert Order(150_000, 4.2).delivery_fee() == 0
    assert Order(90_000, 4.2).delivery_fee() == 18_000
    assert Order(90_000, 3.6).delivery_fee() == 15_000


def test_free_delivery_border():
    assert Order(149_999, 3.0).delivery_fee() == 12_000
    assert Order(150_000, 3.0).delivery_fee() == 0


def test_distance_border():
    assert Order(100_000, 3.0).delivery_fee() == 12_000
    assert Order(100_000, 3.01).delivery_fee() == 15_000
    assert Order(100_000, 4.0).delivery_fee() == 15_000


def test_short_distance():
    assert Order(100_000, 1.5).delivery_fee() == 12_000


def test_fee_is_int():
    assert type(Order(90_000, 4.2).delivery_fee()) is int


def test_all_services_give_same_fee():
    order = Order(90_000, 4.2)
    fees = {
        CheckoutService().delivery_fee(order),
        ReceiptService().delivery_fee(order),
        CourierPayoutService().delivery_fee(order),
    }
    assert fees == {18_000}
