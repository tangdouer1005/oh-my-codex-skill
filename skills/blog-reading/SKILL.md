---
name: blog-reading
description: Analyze technical blogs, engineering writeups, architecture posts, benchmark reports, and official technical explainers with a first-principles lens and produce a structured Chinese Markdown reading note. Use when Codex needs to read non-paper technical content and explain the core problem, practical difficulty, inspiration, insight, reusable patterns, limits, and motivation in the fixed outline required by the user.
---

# Blog Reading

Act as a first-principles thinker. Start from the real engineering problem, the system constraints, and the operational trade-offs, then reconstruct why the author's approach is reasonable.

Write in Chinese unless the user asks otherwise. Use Markdown only. Do not use LaTeX or any math rendering syntax. Express formulas in plain text such as `latency = compute + io + queue`.

Omit pleasantries, scene-setting, and generic praise. Be direct, organized, and concrete.

## Workflow

1. Identify the practical problem.
   - State what real issue the post is trying to solve.
   - Clarify the operational setting, constraints, and success criteria.
2. Reconstruct why the problem is hard.
   - Look for friction in scale, latency, reliability, cost, complexity, observability, developer workflow, or organizational process.
   - Explain why naive solutions fail in practice.
3. Infer the author's core insight.
   - Ask what observation makes the proposed approach feel natural.
   - Trace each pattern or recommendation back to a failure mode, recurring trade-off, or operational fact.
4. Separate `insight` from `pattern`.
   - `Insight` is the author's belief about what matters most in solving the problem.
   - `Practical Pattern` is the concrete mechanism, process, architecture, or habit that realizes that belief.
5. Stress-test the advice.
   - Identify the assumptions, hidden dependencies, and situations where the pattern may stop working.
   - Prefer realistic failure modes over generic criticism.
6. Reconstruct the motivation path.
   - Explain how one could naturally arrive at the article's approach from first principles.
   - Prefer question-driven reasoning.

## Reading Rules

- Do not summarize the blog mechanically section by section. Rebuild the author's actual argument.
- Distinguish between the author's explicit claim and your own `推断`.
- Treat benchmark reports, official docs, incident writeups, architecture blogs, and engineering retrospectives as valid blog-like inputs if they are not academic papers.
- When multiple ideas exist, number them and map each practical pattern to the corresponding insight.
- Prefer operational language such as latency, throughput, reliability, complexity, maintenance burden, rollout risk, or debugging cost when relevant.
- If the post contains prescriptions, explain the conditions under which they are likely to work.
- Always fill the note metadata block before the main sections.

## Output Contract

Always mirror the structure of `/Users/tangjiahui/Desktop/paper/templates/blog-note.md`.

Start with this metadata block:

```md
# {Title}

- Type: blog
- URL:
- Topic:
- Status: to-read
- Tags:
- Date:
- Author:
```

Metadata rules:
- `Type` must be `blog`.
- `URL` should be the original link.
- `Topic` should be filled with the best-fit topic path from the project tree when possible.
- `Status` defaults to `to-read` unless the user asks for another status.
- `Tags` should contain 3-8 concise tags.
- `Date` should use the article date when available.
- `Author` should be filled when available.

After the metadata block, always produce the following top-level sections and preserve the numbering:

### 1. Core Problem
- State the actual practical problem the article is solving or clarifying.
- Formalize when possible:
  - background
  - input / output
  - system boundary
  - success metric
  - operational constraints
- If the post really addresses multiple distinct problems, split them clearly.

### 2. Why It Is Hard
- Explain why the problem is difficult in practice.
- Focus on the structural reason, not just surface inconvenience.
- If useful, group by scale, latency, reliability, cost, developer workflow, debugging, or deployment.

### 3. Core Idea
Under this section, always include the following subsections:

#### 3.1 Inspiration
- For each insight, explain what inspired it.
- Inspirations may come from:
  - a recurring failure in practice
  - a hard system constraint
  - an organizational bottleneck
  - an observation from production behavior
  - a simplifying principle
  - a comparison against a naive baseline

#### 3.2 Insight
- State each insight in one sentence first.
- Then explain:
  - what essence it identifies
  - why that essence matters
  - which inspiration(s) led to it

#### 3.3 Practical Pattern
- Describe the concrete method, practice, architecture, rollout pattern, or operating rule.
- Distinguish pattern types when useful:
  - architecture-level
  - workflow-level
  - process-level
  - observability-level
  - debugging-level
  - evaluation-level
- Do not force academic novelty language onto ordinary blog content.

#### 3.4 Pattern Mapping
- For every concrete pattern, use exactly this format:
  - `【它要解决的实际问题】->【背后的 insight】->【采用了什么具体做法】`
- Keep one pattern per bullet.
- If a pattern supports multiple insights, name the primary one first and note the rest briefly.

### 4. Limits
- State what assumptions or prerequisites the article relies on.
- Explain where the advice may break down.
- If scale, constraints, team size, product shape, or infrastructure complexity grows, explain what new trouble appears.

### 5. Motivation
- Summarize how one could naturally think of the article's idea from first principles.
- Prefer question form.
- Follow first principles:
  - what is the true bottleneck?
  - why do simpler approaches fail?
  - what must a workable solution preserve?
  - what is the cheapest or most robust intervention that addresses the bottleneck?
- Present the motivation as a short sequence of questions that progressively tighten toward the final approach.

### 6. Actionable Takeaway
- State what can be reused directly.
- Identify what is worth turning into team norms, checklists, design rules, or implementation tasks.
- Connect the article back to the reader's current project when possible.
- Mirror the final section wording from the note template.

## Style Rules

- Use compact Markdown headings and bullets.
- Avoid tables unless the user explicitly asks for them.
- Avoid copying the blog's section order unless that order is itself part of the argument.
- Prefer operational precision over vague praise like "this is a good best practice".
- When the article is opinionated, separate observed facts from advocated practices.
- Do not invent production incidents, metrics, or implementation details not present in the source.

## Reference

If you need an exact scaffold, read [references/output-template.md](references/output-template.md) and follow it closely.
