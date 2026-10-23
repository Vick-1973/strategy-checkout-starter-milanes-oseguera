
# Strategy Pattern — Checkout Shipping

**Class activity:** Software Design — Fall 2026  
**Team:** Oswaldo Oseguera Sandoval and Braulio Milanés Loza

## Objective

Refactor the original conditional shipping logic into the object-oriented **Strategy Pattern**.

`Checkout` is the context and receives a `ShippingCostStrategy` object at construction time. Each concrete shipping class implements the same `calculate(order)` contract.

## Shipping Strategies

| Strategy | Shipping rule |
| --- | --- |
| StandardShipping | $0 when subtotal >= $1,000; otherwise $49 |
| ExpressShipping | $99 + $12 per kilogram |
| PickupShipping | $0 |
| SameDayShipping | $149 + $18 per kilogram |

## Strategy Pattern Implementation

The implementation uses:

- ShippingCostStrategy: Abstract Strategy contract.
- StandardShipping: Concrete Strategy.
- ExpressShipping: Concrete Strategy.
- PickupShipping: Concrete Strategy.
- SameDayShipping: Concrete Strategy.
- Checkout: Context that delegates shipping calculations.

SameDayShipping was implemented without adding shipping-specific conditions or modifying the behavior of Checkout.

## Repository Structure

```text
src/
    strategy_checkout/
        __init__.py
        models.py
        strategies.py
        checkout.py

tests/
    test_checkout.py

.github/
    workflows/
        tests.yml

requirements.txt
pyproject.toml
README.md
```

## Running Tests

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run all tests:

```bash
python -m pytest -q
```

Expected output:

```text
13 passed
```

GitHub Actions also runs the automated tests after every push or pull request.

## Example Usage

```python
from strategy_checkout.checkout import Checkout
from strategy_checkout.models import Order
from strategy_checkout.strategies import SameDayShipping

order = Order(subtotal=500.0, weight_kg=3.5)

checkout = Checkout(SameDayShipping())

print(checkout.shipping_cost(order))  # 212.0
print(checkout.total(order))          # 712.0
```

The example assumes src is on the Python import path, as configured for pytest in pyproject.toml.

## Design Explanation

### 1. What varies?

The shipping cost calculation varies depending on the selected delivery method. Each shipping strategy has its own pricing rules, such as fixed fees, weight-based charges, or free shipping thresholds.

### 2. What stays stable?

The Checkout class remains stable because it delegates shipping calculations to a ShippingCostStrategy object. New shipping methods can be introduced without modifying Checkout.

### 3. What complexity cost does Strategy introduce?

The Strategy Pattern introduces additional classes and objects. Each shipping method requires its own class, and the application must create and provide the correct strategy object to Checkout.
