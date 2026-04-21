---
name: paper-reading
description: Analyze research papers with a first-principles lens and produce a structured Chinese Markdown reading note. Use when Codex needs to read a paper, preprint, technical report, or method section and explain the task, challenges, inspirations, insights, novelty, flaws, and motivation in the fixed outline required by the user.
---

# Paper Reading

Act as a first-principles thinker. Start from the problem's objective, constraints, and available primitives, then reconstruct why the method exists and what its design is trying to buy.

Write in Chinese unless the user asks otherwise. Use Markdown only. Do not use LaTeX or any math rendering syntax. Express formulas in plain text such as `score = a * b + c`.

Omit pleasantries, scene-setting, and generic praise. Be direct, organized, and concrete.

## Workflow

1. Identify the paper's primitive problem.
   - State the input, output, optimization target, constraints, and evaluation setting as formally as the paper allows.
   - Distinguish the actual scientific task from the benchmark wrapper.
2. Reconstruct why prior methods struggle.
   - Look for bottlenecks in representation, optimization, generalization, efficiency, data assumptions, supervision, and deployment conditions.
   - Explain challenges causally, not rhetorically.
3. Infer the authors' core insight.
   - Ask what observation would make the proposed design feel obvious.
   - Trace each design choice back to an inspiration, empirical fact, or failure mode of old methods.
4. Separate `insight` from `novelty`.
   - `Insight` is the paper's key belief about how the problem should be attacked.
   - `Novelty` is the concrete architectural, algorithmic, objective, training, inference, or data-design change used to realize that belief.
5. Stress-test the method.
   - Identify hidden assumptions, brittle data conditions, scaling limits, and scenario mismatch.
   - Prefer realistic failure modes over generic criticism.
6. Reconstruct the motivation path.
   - Explain how someone could naturally arrive at the paper's idea from first principles.
   - Prefer question-driven reasoning.

## Reading Rules

- Do not merely paraphrase the abstract. Use the method, experiments, and ablations to validate what the real contribution is.
- If the paper does not state something explicitly, mark it as `推断` and explain the evidence behind the inference.
- When multiple insights exist, number them and map each novelty to the corresponding insight.
- When the paper is underspecified, say exactly what is missing.
- Prefer precise nouns over vague claims like "improves performance significantly".
- If metrics or setups matter for understanding the task, include them briefly inside the relevant section instead of creating a detached experiment summary.
- Always fill the note metadata block before the main sections.
- Always assign `Topic` automatically using the project taxonomy in [references/topic-taxonomy.md](references/topic-taxonomy.md).
- Choose exactly one primary topic path for `Topic`.
- If a paper spans multiple areas, put the best single path in `Topic` and list the rest inside `Tags`.

## Output Contract

Always mirror the structure of `/Users/tangjiahui/Desktop/paper/templates/paper-note.md`.

Start with this metadata block:

```md
# {Title}

- Type: paper
- URL:
- Topic:
- Status: to-read
- Tags:
- Date:
- Authors:
```

Metadata rules:
- `Type` must be `paper`.
- `URL` should be the canonical paper link when available.
- `Topic` must be auto-classified to exactly one path from [references/topic-taxonomy.md](references/topic-taxonomy.md).
- `Status` defaults to `to-read` unless the user asks for another status.
- `Tags` should contain 3-8 concise tags.
- `Date` should prefer the paper year or note date when available.
- `Authors` should list the authors briefly.

After the metadata block, always produce the following top-level sections and preserve the numbering:

### 1. Task
- State the exact problem the paper solves.
- Formalize when possible:
  - input
  - output
  - objective
  - constraints
  - assumptions
  - evaluation protocol
- If the paper actually solves multiple coupled tasks, split them clearly.

### 2. Challenge
- Explain what traditional or prior methods struggle with.
- Focus on the structural reason the problem is hard.
- If useful, group challenges by data, model, optimization, inference, or deployment.

### 3. Insight & Novelty
Under this section, always include the following subsections:

#### 3.1 Inspiration
- For each insight, explain what inspired it.
- Inspirations may come from:
  - a failure mode of previous methods
  - a property of the data or task
  - an analogy to another field
  - an empirical observation from experiments
  - a constraint such as latency, cost, or supervision

#### 3.2 Insight
- State each insight in one sentence first.
- Then explain:
  - what aspect it is an insight about
  - why that aspect matters
  - which inspiration(s) led to it

#### 3.3 Novelty
- Distinguish architecture-level, method-level, objective-level, data-level, training-level, or inference-level novelty.
- Do not label a component as novel unless the paper actually claims or demonstrates it as a contribution.

#### 3.4 Novelty Mapping
- For every novelty, use exactly this format:
  - `【创新点解决的问题是什么】->【受哪个 insight 启发】->【设计了什么创新点，尽可能具体描述】`
- Keep one novelty per bullet.
- If a novelty supports multiple insights, name the primary one first and note the rest briefly.

### 4. Potential Flaw
Under this section, always answer:

#### 4.1 Scenario limits
- Is the paper's setting narrow?
- Could the architecture or method be extended to harder settings with more dimensions, conditions, constraints, agents, modalities, or objectives?

#### 4.2 Bad data properties
- What problematic data properties would break or weaken the method?
- Examples: noise, sparsity, long-tail imbalance, distribution shift, missing labels, non-stationarity, confounding, adversarial artifacts, compositional explosion.

#### 4.3 Paper-worthy difficulty
- Among the above limitations, which one is most worth deep study as a new paper topic?
- Explain why it is both important and technically nontrivial.

### 5. Motivation
- Summarize how one could naturally think of the paper's general idea.
- Prefer question form.
- Follow first principles:
  - what is the essence of the problem?
  - what must a valid solution preserve or exploit?
  - why are simpler alternatives insufficient?
- what is the easiest plausible idea that addresses the real bottleneck?
- Present the motivation as a short sequence of questions that progressively tighten toward the paper's final method.

### 6. Takeaway
- End with the same `Takeaway` block as the note template.
- Include:
  - `一句话总结`
  - `我最认同的点`
  - `我最怀疑的点`
  - `可迁移到我项目里的启发`

## Style Rules

- Use compact Markdown headings and bullets.
- Avoid tables unless the user explicitly asks for them.
- Avoid dumping all experiment details; include only evidence needed to support the reasoning.
- When unsure between two interpretations, present both briefly and say which one is more plausible.
- Do not invent citations, datasets, baselines, or formulas.

## Reference

If you need an exact scaffold, read [references/output-template.md](references/output-template.md) and follow it closely.
Use [references/topic-taxonomy.md](references/topic-taxonomy.md) whenever you need to classify a paper into the project's topic tree.
