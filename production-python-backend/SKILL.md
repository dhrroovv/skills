---
name: production-python-backend
description: Write production-grade Python backend code that prioritizes readability, maintainability, correctness, simplicity, and explicit design over cleverness or minimal lines of code. Use this when implementing, refactoring, reviewing, or designing Python backend code.
---

# Production Python Backend Engineering

## Core Philosophy

Write code for the human who will maintain it six months from now.

The primary goals, in order, are:

1. Correctness
2. Readability
3. Maintainability
4. Explicit behavior
5. Testability
6. Operational reliability
7. Performance where it matters

Do not optimize for:

- Minimum number of lines
- Cleverness
- Novel Python tricks
- Showing off language features
- Excessive abstraction
- Premature optimization
- "DRY" at the expense of readability
- Using obscure APIs when a common approach exists

Prefer boring, obvious, conventional code.

A good implementation should be understandable by a competent Python engineer who has never seen the codebase before.

# 1. Understand Before Implementing

Before changing code:

- Inspect the relevant code.
- Understand the existing data flow.
- Understand the surrounding abstractions.
- Identify the callers and consumers of the code being changed.
- Check existing tests.
- Check existing error-handling conventions.
- Check existing logging and observability.
- Understand external dependencies.

Do not immediately start writing code based only on the user's description.

Do not redesign unrelated parts of the system.

If the existing implementation is already reasonably structured, make the smallest clean change that solves the problem.

# 2. Prefer Explicit Code

Prefer code whose behavior is obvious from reading it.

Good:

```python
user = await user_service.get_user(user_id)

if user is None:
    raise UserNotFoundError(user_id)

orders = await order_service.get_orders(user.id)
```

Avoid unnecessarily clever code such as:

```python
orders = (
    await order_service.get_orders((user := await user_service.get_user(user_id)).id)
    if user
    else []
)
```

The second version may be shorter, but it makes the reader work harder.

Code should optimize for cognitive simplicity, not character count.

# 3. Avoid Clever Python

Use common Python constructs unless there is a strong reason not to.

Prefer:

- straightforward loops
- normal conditionals
- named variables
- explicit functions
- standard library functionality
- conventional comprehensions
- clear exception handling
- type hints

Avoid unnecessarily obscure:

- metaprogramming
- decorators with complicated behavior
- dynamic attribute manipulation
- clever one-liners
- deeply nested comprehensions
- overly clever generators
- monkey patching
- dynamic imports
- excessive use of `getattr` / `setattr`
- implicit behavior that requires knowledge of Python internals

If a less experienced engineer can understand the code immediately, that is usually preferable.

# 4. Functions

Functions should have one clear responsibility.

Prefer:

```python
async def create_order(
    user_id: UUID,
    items: list[OrderItem],
) -> Order:
    validate_order_items(items)

    order = build_order(user_id, items)

    await order_repository.save(order)

    return order
```

Avoid functions that:

- validate input
- perform database operations
- call external APIs
- transform data
- send notifications
- log unrelated information
- and contain business rules

all inside one large function.

Extract functions when doing so improves understanding.

Do not create tiny functions solely to reduce line count or satisfy an arbitrary rule.

# 5. Classes and OOP

Use classes when they represent a meaningful concept or provide useful encapsulation.

Good candidates include:

- domain concepts
- services with meaningful state/dependencies
- clients for external systems
- repositories where the architecture actually benefits from them
- strategies with interchangeable behavior
- components with a clear lifecycle

Do not create classes simply because "everything should be an object."

Avoid:

```python
class UserNameGetter:
    def get(self, user):
        return user.name
```

Prefer simple functions when a class provides no meaningful abstraction.

Follow normal OOP principles:

- Encapsulation
- Single Responsibility
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation
- Dependency Inversion

But do not force SOLID principles mechanically.

The goal is good design, not maximum abstraction.

# 6. Abstraction

Introduce an abstraction when it solves a real problem.

Good reasons:

- Multiple implementations exist.
- A dependency needs to be isolated.
- A boundary between components needs to be explicit.
- Testing genuinely benefits from the abstraction.
- Business logic should not depend directly on infrastructure.
- A concept has meaningful behavior of its own.

Bad reasons:

- "This might be useful someday."
- "Every service needs a repository."
- "We need an interface because SOLID says so."
- "This function is 10 lines, therefore it needs a class."
- "We may eventually support another database."

Avoid speculative abstractions.

Prefer:

simple code → real duplication/problem appears → extract abstraction

rather than:

possible future requirement → create interfaces/factories → add unnecessary indirection.

# 7. Design Patterns

Use established design patterns when they make the design clearer.

Common useful patterns include:

- Strategy
- Factory
- Adapter
- Facade
- Observer
- Repository
- Dependency Injection
- Command

Do not introduce a design pattern merely to demonstrate knowledge of it.

A simple `if/elif` chain can be better than a Strategy pattern when there are only two stable cases.

A function can be better than a Factory class when object creation is simple.

Use the simplest design that will remain maintainable.

# 8. DRY — Don't Repeat Yourself

Avoid unnecessary duplication of actual knowledge or business rules.

However, do not blindly eliminate similar-looking code.

Two pieces of code that look similar may represent different business concepts.

Prefer:

```python
calculate_shipping_price(...)
calculate_refund_amount(...)
```

over prematurely combining them into:

```python
calculate_amount(..., mode="shipping")
```

Duplication is sometimes preferable to a misleading abstraction.

Follow:

> Duplication is cheaper than the wrong abstraction.

# 9. Naming

Names should communicate intent.

Prefer:

```python
pending_orders
expired_sessions
failed_payment_attempts
calculate_discount
fetch_product_details
```

Avoid:

```python
data
obj
thing
result
tmp
process
handle
do_it
manager
helper
utils
```

unless the generic name genuinely describes the concept.

Avoid meaningless suffixes such as:

```text
UserManager
DataHelper
CommonUtils
GenericService
BaseProcessor
```

unless they represent a real concept.

Prefer domain-specific names.

# 10. Type Hints

Use type hints consistently in production backend code.

Prefer:

```python
async def get_user(user_id: UUID) -> User | None: ...
```

over:

```python
async def get_user(user_id): ...
```

Use modern Python typing appropriate for the project's Python version.

Types should improve understanding.

Do not create unnecessarily complicated types just to make the type checker happy.

# 11. Error Handling

Handle errors intentionally.

Do not use:

```python
try:
    ...
except Exception:
    pass
```

Do not catch broad exceptions unless there is a clear reason.

Catch exceptions where you can meaningfully handle them.

Prefer domain-specific exceptions when they improve clarity:

```python
raise UserNotFoundError(user_id)
```

instead of:

```python
raise Exception("user not found")
```

Preserve useful error context.

Do not hide failures merely to make the application appear successful.

# 12. Async Code

Use asynchronous programming when the workload is I/O-bound and the surrounding application supports it.

Use async for things such as:

- database I/O
- HTTP requests
- network operations
- async message brokers

Do not use async merely because it looks modern.

Avoid blocking operations inside async code.

# 13. Database Code

Treat database operations as production-critical code.

Consider:

- indexes
- query complexity
- N+1 queries
- transactions
- isolation
- locking
- connection pools
- pagination
- constraints
- migrations
- race conditions

Do not fetch an entire table just to filter it in Python when the database can perform the filtering efficiently.

Prefer database-side filtering:

```python
query = select(User).where(User.email == email)
```

over:

```python
users = await get_all_users()

for user in users:
    if user.email == email:
        return user
```

Do not introduce unnecessary database queries.

When modifying schemas, consider existing production data and migration safety.

# 14. API Design

Backend APIs should be predictable and explicit.

Consider:

- request validation
- response schemas
- HTTP semantics
- status codes
- authentication
- authorization
- idempotency
- backwards compatibility
- pagination
- error responses
- timeouts
- rate limits where relevant

Do not leak internal implementation details through API contracts.

Avoid breaking existing consumers unless the change is explicitly intended and coordinated.

# 15. External Services

Treat every external dependency as unreliable.

For external APIs, consider:

- timeouts
- retries
- exponential backoff
- rate limits
- idempotency
- partial failures
- malformed responses
- authentication failures
- service unavailability
- observability

Never assume an external service will always respond successfully.

Do not blindly retry every failure.

Retries should be intentional and should consider whether the operation is safe to repeat.

# 16. Logging and Observability

Production code should be observable.

Logs should answer:

- What happened?
- Where did it happen?
- Which request/entity was involved?
- Why did it fail?
- What useful context is available?

Do not log:

- passwords
- API keys
- tokens
- secrets
- sensitive user data

Avoid excessive logging inside hot paths.

Use structured logging where the existing application supports it.

# 17. Configuration and Secrets

Do not hardcode:

- API keys
- passwords
- tokens
- database credentials
- environment-specific configuration

Use the project's established configuration mechanism.

Do not introduce a new configuration system when one already exists.

# 18. Testing

Write tests around behavior rather than implementation details.

Prioritize tests for:

- business rules
- edge cases
- failure scenarios
- external integration boundaries
- database behavior where appropriate
- critical API contracts

A test should clearly communicate what behavior it protects.

Avoid tests that simply mirror the implementation.

When changing existing code, inspect existing tests before deciding how to modify the code.

# 19. Performance

Correctness and maintainability come before micro-optimization.

Do not optimize without evidence.

Before optimizing, identify the actual bottleneck using:

- profiling
- metrics
- tracing
- query analysis
- benchmarks

Prefer algorithmic improvements and eliminating unnecessary work over micro-optimizations.

Do not make code significantly harder to understand for a negligible performance improvement.

# 20. Security

Treat security as part of correctness.

Consider:

- authentication
- authorization
- input validation
- injection vulnerabilities
- secrets
- sensitive data exposure
- insecure deserialization
- SSRF
- path traversal
- rate limiting
- privilege boundaries

Never disable a security mechanism simply to make development easier without explicitly understanding the consequences.

# 21. Dependencies

Prefer the standard library or existing project dependencies when they are sufficient.

Do not add a dependency for a trivial problem.

Before adding a dependency, consider:

- Does the project already have something that solves this?
- Is the dependency actively maintained?
- Does it significantly reduce complexity?
- Is its security/reliability acceptable?
- Will it become long-term maintenance overhead?

A new dependency should solve a meaningful problem.

# 22. Refactoring

Refactor when it improves the code.

Good refactoring:

complex code → clearer structure → same behavior

Avoid mixing large unrelated refactors with feature work.

Do not rewrite working code simply because you would personally structure it differently.

Preserve behavior unless changing behavior is part of the task.

# 23. Comments

Comments should explain WHY, not WHAT.

Bad:

```python
# Increment counter
counter += 1
```

Good:

```python
# We intentionally keep this counter in memory because it is only
# used for request-local batching and must not be shared between workers.
counter += 1
```

Do not use comments to compensate for confusing code.

If code requires a large comment to explain what it does, first consider whether the code itself can be made clearer.

# 24. Backward Compatibility

Before changing an existing interface, consider:

- callers
- API consumers
- database records
- background jobs
- message schemas
- cached data
- external integrations

Prefer additive changes when possible.

Do not silently change behavior that existing consumers may rely on.

# 25. Production Readiness Checklist

Before considering a backend implementation complete, verify:

- Is the behavior correct?
- Is the code easy to understand?
- Are names meaningful?
- Is the abstraction justified?
- Is error handling intentional?
- Are failure modes considered?
- Are external calls protected with appropriate timeouts?
- Are database queries efficient?
- Are transactions correct?
- Is the code observable?
- Are secrets protected?
- Are important edge cases tested?
- Is the API backward compatible?
- Did we avoid unnecessary dependencies?
- Did we avoid unnecessary abstractions?
- Did we modify only what was necessary?

If the implementation is technically correct but unnecessarily complicated, simplify it.

If the implementation is short but difficult to understand, make it clearer.

The best production code is not the cleverest code.

It is code that another engineer can confidently understand, debug, modify, and extend.
