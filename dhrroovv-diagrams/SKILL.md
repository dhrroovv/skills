---
name: dhrroovv-diagrams
description: "Dhruv's rules for drawing any diagram (flowchart, system design, architecture, sequence, ER, network, state): always use the draw.io connector, never tldraw; Mermaid for standard types, XML for exact layout or cloud/network icons; official draw.io icons for named technologies; readability limits (title, short labels, 2-4 colors, error paths, about 12 nodes). Use whenever a diagram, chart of a flow, or architecture picture is requested or would clearly help."
---

# Diagrams

Goal: a diagram I can read in chat at a glance and open and edit in draw.io.

## Tool

- Use the draw.io connector (`create_diagram`, `search_shapes`, `get_drawio_reference`) for every diagram. Never use tldraw, and don't hand-draw SVG or ASCII art in its place.
- If the draw.io connector isn't enabled or fails, say so in one line and stop. Don't silently switch tools. I'll enable it or tell you what to use instead.
- Call `get_drawio_reference` once per format (`mermaid` or `xml`) before the first diagram in a conversation.

## Pick the format

| Situation                                                                                          | Format                                               |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Standard types: flowchart, sequence, ER, class, state, gantt                                       | Mermaid (via `create_diagram` with `mermaid`)        |
| I need exact layout, grouping or regions (VPC, subnets, clusters, swimlanes), or cloud/network icons | draw.io XML (via `create_diagram` with `xml`)        |

- Any diagram that names technologies (see Icons) goes to XML so the icons can be used.
- If I ask for XML or "no Mermaid", use XML for the rest of the conversation.
- Large Mermaid flowcharts (20+ nodes, 3+ decisions, or back-edges): ask for `postLayout: "elk"`. For XML placed by hand with right-angle edges that might cross boxes: `routing: "libavoid"`.

## Icons for named technologies

Applies when the diagram names AWS, Azure, GCP, Kubernetes, network gear, databases, queues, or similar products.

1. Look up the official draw.io icon before drawing. For AWS, Azure, GCP and Kubernetes, the style can be written as `icon=aws lambda`; for everything else (Cisco, databases, logos) run `search_shapes` first and use the returned style string as is.
2. Use one icon set per diagram. Don't mix, for example, AWS 2024 icons with generic ones. Pick the set that covers most of the nodes.
3. Put a short label under each icon (1-3 words, such as "Orders DB").
4. If no matching icon exists, use a plain labeled box for that node. Don't use a wrong icon or a lookalike.

## Readability rules

- Give every diagram a title.
- Short labels: 1-5 words per node. Put detail in the reply text, not in the diagram.
- 2-4 colors, chosen by role (for example: client, service, data store, external), and stay consistent. Red or orange is for error paths only.
- Include error and failure paths, not just the happy path (retries, dead-letter queue, timeout, fallback). Label failure edges.
- Label edges only where the meaning isn't obvious (decision branches, protocols, async vs sync).
- About 12 nodes at most. If it needs more, split it into two diagrams (for example overview and detail) and say how they connect.
- Layout reads left-to-right or top-to-bottom, with no crossing lines where it can be avoided.
- Use `adaptiveColors="auto"` on XML diagrams so they work in light and dark mode.

## Reply format

- Lead with the diagram, then at most a few lines: what it shows, the key assumption, and anything left out. Don't narrate each box.
- If a name in the request is ambiguous (two possible services or flows), pick the likeliest, state it in one line, and draw it.

## Before finishing

Check and fix any of these:

- A tool other than draw.io, or a diagram with no title.
- A named technology drawn as a plain box when an official icon exists, or icons from more than one set.
- Missing error path, more than 4 colors, or more than about 12 nodes.
- Labels longer than 5 words, or an icon with no label.

## Superseded patterns

<!-- Record old habits here: what, date dropped, why. -->
