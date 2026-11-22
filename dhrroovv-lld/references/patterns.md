# Approved patterns, Python forms

Use a pattern only when you can name the present problem it solves. Snippets show shape only.

## Strategy: pass a callable

```python
from collections.abc import Callable

type Discount = Callable[[float], float]


def final_price(price: float, discount: Discount) -> float:
    return price - discount(price)


final_price(100.0, lambda amount: amount * 0.1)
```

Use a small class with `__call__` only if the strategy keeps state.

## Factory: classmethod or registry

```python
from typing import Self


class Order:
    def __init__(self, items: list[str]) -> None:
        self.items = items

    @classmethod
    def from_cart(cls, cart: Cart) -> Self:
        return cls(cart.items)
```

```python
HANDLERS: dict[str, Callable[[Event], None]] = {"created": on_created, "paid": on_paid}


def handle(event: Event) -> None:
    HANDLERS[event.kind](event)
```

Use a registry only with 3+ variants and more expected.

## Singleton: module-level object

`settings = Settings()` in `app/core/config.py`, imported where needed. Never a class with `__new__` tricks.

## Adapter plus dependency injection at an external boundary

```python
from typing import Protocol


class PaymentGateway(Protocol):
    async def charge(self, cents: int, customer: str) -> str: ...


class StripeGateway:
    def __init__(self, client: StripeClient) -> None:
        self.client = client

    async def charge(self, cents: int, customer: str) -> str:
        intent = await self.client.create_payment_intent(cents, customer)
        return intent.id


async def checkout(order: Order, gateway: PaymentGateway) -> str:
    return await gateway.charge(order.total_cents, order.customer_id)
```

This is the one place a Protocol with a single real implementation is justified: tests pass a fake gateway.

## Decorator: cross-cutting behavior

```python
import functools
import logging
import time
from collections.abc import Callable

logger = logging.getLogger(__name__)


def timed[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(fn)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            logger.info("%s took %.3fs", fn.__name__, time.perf_counter() - start)

    return inner
```

## Chain: ordered list of callables

```python
type Check = Callable[[Order], None]  # each raises on failure


def validate(order: Order, checks: list[Check]) -> None:
    for check in checks:
        check(order)
```

## Value object

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Money:
    cents: int
    currency: str
```

Use Pydantic instead when the data is parsed, validated, or crosses a boundary.
