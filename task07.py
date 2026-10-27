# Task 7 - class design decides what happens on delete (paper task)
#
# 7.1 + 7.2 Relationships and multiplicity
#
#   Order -> Customer         association        Order *  ---  1 Customer
#       (customer lives without the order; each order has one customer)
#   Order <>-- OrderLine      composition        Order 1  ---  1..* OrderLine
#       (Order creates the lines in add() and owns them)
#   OrderLine -> Product      association        OrderLine *  ---  1 Product
#       (product lives without lines, one line = one product)
#   Order -> Courier          association        Order *  ---  0..1 Courier
#       (courier is None until assign(), one courier has many orders)
#   Catalog <>-- Product      aggregation        Catalog 1  ---  0..* Product
#       (catalog has a list of products, but products exist without it)
#   Order ..> Product         dependency         (add() gets a product only as
#       a parameter to read its price, Order does not keep it)
#   SmsGateway ..> Order      dependency         (order_shipped(order) only
#       uses the order, does not store it)
#
#   Not enforced by the code: Order 1..* OrderLine. Now an order with zero
#   lines is allowed. Also the customer can be None, nothing checks it.
#
# 7.3 ON DELETE
#   order_lines.order_id    -> CASCADE. Composition: a line has no sense
#       without its order, part disappears with the whole (lifetime test).
#   order_lines.product_id  -> RESTRICT. Association: old orders must keep
#       what was sold. A product that was sold must not be deleted (better
#       mark it inactive).
#   orders.customer_id      -> RESTRICT. Customer is required (1), so SET NULL
#       is not possible, and the order is a money record, it should not
#       disappear when the customer does.
#   orders.courier_id       -> SET NULL. Multiplicity is 0..1, the order lives
#       without the courier (the courier just becomes not assigned).
#
# 7.4 unit_price is the price at the moment of the purchase and Product.price
#     is the price today. They are different facts and they change for
#     different reasons. If we only used Product.price, the total of old
#     orders would change when the price changes. So it is not a DRY problem.
