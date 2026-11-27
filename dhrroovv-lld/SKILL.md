---
name: dhrroovv-lld
description: "Dhruv's low-level design and OOP rules for Python: when to use classes vs functions, how to split responsibilities, composition over inheritance, Protocols and dependency injection, which design patterns are approved (with their Python forms), and how to write a short LLD before coding. Use when designing or structuring classes and modules, choosing a design pattern, writing an LLD, or refactoring code structure. Builds on dhrroovv-python."
---

# Low-level design

Goal: code that is easy to read and safe to change. The simplest structure that solves today's requirement wins.

Follow `dhrroovv-python`, and in FastAPI projects `dhrroovv-fastapi`; their layout and naming rules win over this skill. Match the structure already in the codebase. Don't introduce a second style next to it.

## Default stance

- Functions first. Plain functions and modules are the default unit. Add a class only when it holds state shared by several operations, or when it sits at an external boundary and must be swappable or fakeable.
- Abstract on the third real use, not the first. Tolerate duplication twice; extract on the third.
- No speculative flexibility: no interface with one implementation (except at an external boundary), no factory around a single constructor, no config for things that never change, no hooks "for later".
- Prefer a few deep modules over many tiny ones. A module or class should hide real complexity behind a small interface. Avoid classes or methods that only forward calls.
- Never silently pick a pattern or structure for a non-trivial choice. Give me two options in 2-3 lines each with a recommendation, and I decide.

## OOP fundamentals (Python forms)

- Encapsulation: public attributes by default. A leading underscore marks internal methods and functions only (never variables or attributes). Use `@property` only for derived or validated values, never for trivial getters and setters. State changes go through the object's methods, not scattered across callers.
- Abstraction: expose the smallest interface callers need. Callers must not need to know internal steps or call order.
- Inheritance: only for a true is-a relationship that shares real behavior, at most one level deep, with `@override` on overrides. Subclasses must honor the parent's contract. Never inherit just to reuse code; compose instead. No mixins unless I ask.
- Polymorphism: use a `Protocol` or a callable, not `isinstance` chains. Use `ABC` only when the base class carries shared implementation or you need failure at instantiation.
- Composition: objects receive their collaborators as constructor arguments.

## Principles and how to apply them

- Single responsibility: describe the unit in one sentence without "and". Split a class that mixes I/O with business rules, or a function that needs section comments.
- Size: a function should read at a glance (roughly 40 lines at most, shallow nesting, early returns). A class with more than about 7 public methods or unrelated groups of fields probably needs splitting.
- Dependency inversion at boundaries only: external services (payments, email, storage, third-party APIs), the clock, randomness. Depend on a small `Protocol` (1-3 methods) or a callable passed in as an argument. Inside our own logic depend on concrete code. No DI containers; in FastAPI use `Depends`.
- Open/closed: replace an if/elif chain on type with a dict of callables only when there are 3+ branches and more are expected.
- Interface segregation: keep Protocols small. Don't force implementers to carry unused methods.
- Model data explicitly. Use Pydantic where data is parsed, validated, or crosses a boundary. Use `@dataclass(frozen=True, slots=True)` for small internal value objects. Never pass raw dicts or tuples between modules.
- Dependencies point one way (routers, then services, then models). No import cycles. Lower layers never import higher ones.

## Patterns

Use a pattern only when you can name the present problem it solves in one sentence. If you can't, don't use it. When you do use one, say which and why in your summary. Snippets: `references/patterns.md`.

| Need                                            | Python form                                                                  |
| ----------------------------------------------- | ---------------------------------------------------------------------------- |
| Swap an algorithm                               | Strategy: pass a function; a class with `__call__` only if it has state      |
| Create variants                                 | Factory: a function, `@classmethod from_x`, or a dict registry (3+ variants) |
| One shared object                               | Singleton: a module-level instance. Never a `__new__` singleton              |
| Wrap a foreign API                              | Adapter: small class implementing our Protocol                               |
| Cross-cutting behavior (retry, timing, caching) | Decorator: `@decorator` function                                             |
| Behavior varies by state (3+ states)            | State: one small class per state, or enum plus dict                          |
| Ordered checks or handlers                      | Chain: a list of callables run in order                                      |
| Notify other parts                              | Observer: list of callbacks, only when asked                                 |
| Fixed workflow, varying steps                   | Template Method: base class with named steps, one level only                 |
| Many optional settings                          | Builder: keyword arguments and dataclass defaults                            |
| Setup and cleanup                               | Context manager: `with` / `@contextmanager`                                  |

Ask me before using: Abstract Factory, Bridge, Composite, Flyweight, Mediator, Memento, Proxy, Visitor, Interpreter, any pattern not listed, a repository layer (our service layer owns queries), an event bus or plugin registry, metaclasses, descriptors, or a DI container.

## When I ask for an LLD

Use `references/lld-template.md`. In short:

1. Restate the requirement, constraints, and non-goals. List open questions. Ask them if the answer changes the design; otherwise state your assumptions.
2. Find entities (nouns) and responsibilities (verbs). Mark each as data model, behavior (function or service), or boundary (adapter).
3. Show relationships: has-a and uses over is-a, with dependency direction.
4. Write public signatures only, fully type-hinted, no bodies.
5. Walk through the main flow and one failure flow.
6. Pattern check: each pattern used needs its one-sentence problem. Drop the rest.
7. Stop and wait for my approval before implementing.

Keep it to one page. Use a Mermaid diagram of at most about 12 nodes so it renders in any tool. For ordinary coding tasks, apply the rules silently and don't write a design doc.

## FastAPI projects

Services stay as modules of plain async functions. Don't wrap them in classes, and don't add a repository layer. Keep the folder layout from `dhrroovv-fastapi`.

## Before finishing a task that adds or restructures classes

Check and remove any of these:

- A class that could be a function, such as one with `__init__` and a single public method.
- A class of only static methods (make it a module), or any `Manager`, `Helper`, or `Utils` class.
- An interface, factory, or layer that isn't at an external boundary and has one implementation.
- Inheritance more than one level deep, or inheritance used only for code reuse.
- `isinstance` chains, trivial getters and setters, import cycles, or mutable global state other than settings and the engine.

## Superseded patterns

<!-- Record old habits here: what, date dropped, why. -->
