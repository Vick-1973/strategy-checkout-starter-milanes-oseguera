import pytest

from strategy_checkout.checkout import Checkout
from strategy_checkout.models import Order
from strategy_checkout.strategies import (
    ShippingCostStrategy,
    StandardShipping,
    ExpressShipping,
    PickupShipping,
    SameDayShipping,
)


class FixedShipping(ShippingCostStrategy):
    """Test double proving Checkout accepts any valid Strategy object."""

    def calculate(self, order: Order) -> float:
        return 10.0


def test_strategy_contract_cannot_be_instantiated():
    with pytest.raises(TypeError):
        ShippingCostStrategy()


def test_all_shipping_methods_implement_the_contract():
    for strategy_type in (
        StandardShipping,
        ExpressShipping,
        PickupShipping,
        SameDayShipping,
    ):
        assert issubclass(strategy_type, ShippingCostStrategy)


def test_standard_shipping_costs_49_below_threshold():
    order = Order(subtotal=750.0, weight_kg=2.0)
    assert Checkout(StandardShipping()).shipping_cost(order) == 49.0


def test_standard_shipping_is_free_at_exact_threshold():
    order = Order(subtotal=1000.0, weight_kg=2.0)
    assert Checkout(StandardShipping()).shipping_cost(order) == 0.0


def test_standard_shipping_is_free_above_threshold():
    order = Order(subtotal=1250.0, weight_kg=3.5)
    assert Checkout(StandardShipping()).shipping_cost(order) == 0.0


def test_express_shipping_uses_base_plus_weight():
    order = Order(subtotal=500.0, weight_kg=3.5)
    assert Checkout(ExpressShipping()).shipping_cost(order) == pytest.approx(141.0)


def test_express_shipping_with_zero_weight():
    order = Order(subtotal=500.0, weight_kg=0.0)
    assert Checkout(ExpressShipping()).shipping_cost(order) == 99.0


def test_pickup_shipping_is_free():
    order = Order(subtotal=500.0, weight_kg=3.5)
    assert Checkout(PickupShipping()).shipping_cost(order) == 0.0


def test_same_day_shipping_uses_base_plus_weight():
    order = Order(subtotal=500.0, weight_kg=3.5)
    assert Checkout(SameDayShipping()).shipping_cost(order) == pytest.approx(212.0)


def test_same_day_shipping_with_zero_weight():
    order = Order(subtotal=500.0, weight_kg=0.0)
    assert Checkout(SameDayShipping()).shipping_cost(order) == 149.0


def test_total_adds_standard_shipping_cost():
    order = Order(subtotal=500.0, weight_kg=2.0)
    assert Checkout(StandardShipping()).total(order) == 549.0


def test_total_adds_same_day_shipping_cost():
    order = Order(subtotal=500.0, weight_kg=3.5)
    assert Checkout(SameDayShipping()).total(order) == pytest.approx(712.0)


def test_checkout_delegates_to_any_strategy_without_changes():
    order = Order(subtotal=100.0, weight_kg=2.0)
    checkout = Checkout(FixedShipping())
    assert checkout.shipping_cost(order) == 10.0
    assert checkout.total(order) == 110.0
