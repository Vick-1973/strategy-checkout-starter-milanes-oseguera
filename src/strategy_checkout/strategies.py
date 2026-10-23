from abc import ABC, abstractmethod
from .models import Order


class ShippingCostStrategy(ABC):
    """Abstract contract shared by all shipping methods."""

    @abstractmethod
    def calculate(self, order: Order) -> float:
        """Return the shipping charge for an order."""
        raise NotImplementedError


class StandardShipping(ShippingCostStrategy):
    def calculate(self, order: Order) -> float:
        return 0.0 if order.subtotal >= 1000.0 else 49.0


class ExpressShipping(ShippingCostStrategy):
    def calculate(self, order: Order) -> float:
        return 99.0 + 12.0 * order.weight_kg


class PickupShipping(ShippingCostStrategy):
    def calculate(self, order: Order) -> float:
        return 0.0


class SameDayShipping(ShippingCostStrategy):
    def calculate(self, order: Order) -> float:
        return 149.0 + 18.0 * order.weight_kg
