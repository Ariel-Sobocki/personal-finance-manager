# Reflection — Design Choices

This document explains the design decisions behind the Personal Finance Manager, why each pattern was chosen, and the trade-offs I found while building it with Test-Driven Development (TDD).

## Development approach: TDD

Every feature was built with a red → green → refactor cycle. The provided tests acted as the specification, and I added my own tests whenever I found a gap (10 own tests, 23 in total).

The first problem was that `python -m unittest discover` reported `Ran 0 tests ... OK`. The `balance/` and `transaction/` folders were missing `__init__.py`, so unittest never found the tests. A green result with zero tests is a false sense of safety. From then on I always checked *how many* tests ran, not only whether they passed.

## 1. Singleton — `Balance`

**Why:** the whole application must share one balance. If the main program and the observers each created their own `Balance`, there would be several unsynchronized balances.

**How:** a class attribute `_instance` plus a `get_instance()` class method that creates the object only once. Calling `Balance()` directly when an instance already exists raises `RuntimeError`, so the single access point is enforced.

**Trade-off:** I first tried overriding `__new__`. I discarded it because the tests require `get_instance()`, and because Python always runs `__init__` after `__new__`, which would reset the balance on every call.

## 2. Adapter — `TransactionAdapter`

**Why:** income from the freelance platform (`ExternalFreelanceIncome`) has a different interface: a string type (`"income"`), an invoice id and a description. The rest of the system only understands `Transaction` (an amount plus a `TransactionCategory` enum). The adapter translates one into the other without modifying either class. In a real system the external class would usually come from a third party that I do not control.

**Decision:** instead of always hard-coding `INCOME`, the adapter maps `"income"` to `TransactionCategory.INCOME` and raises `ValueError` for any unknown type. If the platform ever sends something unexpected, it fails loudly instead of silently adding money to the balance. Fields the system does not need (`invoice_id`, `description`) are dropped.

## 3. Observer — `LowBalanceAlertObserver` and `PrintObserver`

**Why:** several parts of the app need to react when the balance changes (printing, alerts), but `Balance` should not know about any of them. With Observer, `Balance` (the subject) keeps a list of observers and calls `update(balance, transaction)` on each one. New behaviour can be added without touching `Balance` (loose coupling).

**Decisions:**
- Observers are notified **after** the balance is updated, so they see the new value. If the category is invalid, the `ValueError` stops execution and nobody is notified.
- The whole `Balance` object is passed to `update()`, so each observer asks for what it needs (`get_balance()`, `summary()`).
- `PrintObserver` reuses `Transaction.__str__` and `Balance.summary()`, which were already tested.

**Problem found: Singleton + Observer.** Because `Balance` is a Singleton, observers registered in one test stayed attached for the following tests. `reset()` only clears the balance. I considered two fixes:
1. Making `reset()` also clear the observers.
2. Adding `unregister_observer()` and having each test remove what it registered (`addCleanup`).

I chose the second. It keeps `reset()` with a single responsibility, avoids silently disabling alerts if `reset()` is ever called in the main program, and completes the Observer pattern with its "detach" operation.

## 4. Fourth pattern: Strategy — platform fees

**Problem:** freelance platforms charge a fee, and the rule changes (10%, 5%, no fee, maybe a fixed amount). Hard-coding it with `if` statements inside the adapter would mean modifying the adapter for every new rule.

**Solution:** a `FeeStrategy` interface with `apply_fee(amount)`, and two concrete strategies: `NoFeeStrategy` and `PercentageFeeStrategy(percentage)`. `TransactionAdapter` receives a strategy and calls `apply_fee()` without knowing which one it got. A new rule only requires a new class (open/closed principle).

**Why Strategy over Command or Decorator:** it solves a realistic need, it was low-risk (the strategy is an optional parameter that defaults to `NoFeeStrategy`, so existing code and tests kept working), and it fits naturally into the existing Adapter. In `main.py` the freelance income of 1200 is now registered net of a 10% fee (1080), and the final balance is 1255.00.

## Testing decisions

- **Own unit tests** cover gaps in the provided ones. Examples: `summary()` (a broken format string, `{:2.f}`, went undetected because no test called it), equality with a different category or another type, unknown external types, unregistered observers, the printed output (captured with `redirect_stdout`) and both fee strategies.
- **Proving tests work:** for new tests I temporarily broke the code to see them fail (for example, removing the category comparison in `__eq__`). A test you have never seen fail may be passing by accident.
- **Acceptance test** (`test_main.py`) runs the full `main()` and checks the final balance. Since `main()` registers observers inside the Singleton, the test resets `Balance._instance` before and after, so it starts clean and leaves nothing behind.
- **When a requirement changes, the test changes first.** Adding the 10% fee meant updating the expected balance in `test_main.py` (red) before changing `main.py` (green).

## Limitations and possible improvements

- `LowBalanceAlertObserver` only stores the **latest** state. In `main.py` the balance dropped to 50 (below the threshold of 100) after the second transaction, but the final output shows `False` because it recovered later. A real app should notify at the moment the alert fires, or keep an alert history.
- Amounts are plain numbers. The `/` in the percentage fee produces floats (`1080.0`); a production version should use `Decimal` to avoid rounding issues with money.
- `Transaction` has no `__repr__`, so failed assertions show `<Transaction object at 0x...>` instead of readable values. Adding it would make debugging easier.
- `add_income()` and `add_expense()` do not notify observers; only `apply_transaction()` does. That matches the observer interface (which needs a transaction), but it is a rule callers must know.
