# LLD template (one page)

````markdown
# LLD: <feature name>

## Goal and scope

<2-4 lines>
Non-goals: <what this design deliberately leaves out>

## Assumptions and open questions

- <assumption or question>

## Components

| Name | Kind (data / behavior / boundary) | Responsibility (one sentence) | Collaborators |
| ---- | --------------------------------- | ----------------------------- | ------------- |

## Structure

```mermaid
classDiagram
  %% at most ~12 nodes; show dependency direction
```

## Public interfaces

```python
# signatures only, fully type-hinted, no bodies
```

## Main flow

```mermaid
sequenceDiagram
  %% happy path
```

## Failure flows

- <what fails> -> <what happens>

## Patterns used

- <pattern>: <the present problem it solves> (or "None")

## Decisions for review

- Option A vs Option B, with a recommendation
````
