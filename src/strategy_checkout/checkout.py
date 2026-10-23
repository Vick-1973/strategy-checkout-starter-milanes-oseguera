from .models import Order
from .strategies import ShippingCostStrategy


class Checkout:
    def __init__(self, shipping_strategy: ShippingCostStrategy) -> None:
        self.shipping_strategy = shipping_strategy

    def shipping_cost(self, order: Order) -> float:
        return self.shipping_strategy.calculate(order)

    def total(self, order: Order) -> float:
        return order.subtotal + self.shipping_cost(order)
