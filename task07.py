# Task 7 - class design decides what happens on delete (paper task)

# 7.1 7.2 Relationships and multiplicity
#
#   Order -> Customer         association        Order *  ---  1 Customer
#       (customer lives without the order; each order has one customer)
#   Order <>-- OrderLine      composition        Order 1  ---  1..* OrderLine
#       (Order creates the lines in add() and owns them)
#   OrderLine -> Product      association        OrderLine *  ---  1 Product
#       (product lives without lines, one line = one product)


# 7.3 ON DELETE
#   order_lines.order_id    -> CASCADE. Composition: a line has no sense
#       without its order, part disappears with the whole (lifetime test).
#   order_lines.product_id  -> RESTRICT. Association: old orders must keep
#       what was sold. A product that was sold must not be deleted (better
#       mark it inactive).

# 7.4 unit_price is the price at the moment of the purchase and Product.price
#     is the price today. They are different facts and they change for
#     different reasons. If we only used Product.price, the total of old
#     orders would change when the price changes. So it is not a DRY problem.
