# Output Format

Use this exact top-level structure in the final Markdown output:

```md
# PDF Report Summary

## 1. 这个报告主要讲的什么
用 3-6 句话总结报告主题、目标、方法或核心结论。

## 2. 从第几页到第几页讲到什么
- 第 1 页到第 3 页：说明报告背景、问题定义和整体结构。
- 第 4 页到第 6 页：介绍数据来源、方法或分析框架。
- 第 7 页到第 10 页：展开主要发现、指标变化或案例分析。
- 第 11 页到第 12 页：总结结论、建议或后续行动。

## 3. 报告中的并列对象与共享字段整理
数据来源：第 X 页到第 Y 页

| 对象 | 字段/指标 1 | 字段/指标 2 | 字段/指标 3 |
|---|---|---|---|
| 对象 A | ... | ... | ... |
| 对象 B | ... | ... | ... |

字段/指标说明：
- 字段/指标 1：说明这个字段或指标表示什么。
- 字段/指标 2：说明这个字段或指标表示什么。
- 字段/指标 3：说明这个字段或指标表示什么。
```

Guidance:

- Use Arabic numerals for page numbers and keep them 1-based.
- Prefer `第 X 页` when a range contains one page, and `第 X 页到第 Y 页` when a range spans multiple pages.
- Keep each bullet to one sentence unless the PDF is unusually dense.
- Preserve clear section names from the report when they are visible in headings.
- If a page range is low-confidence because of weak extraction, say so briefly.
- In the default first pass, return only section 1 and section 2.
- Only include `## 3. 报告中的并列对象与共享字段整理` after the user has explicitly selected the objects and fields or metrics to extract.
- If section 3 is requested, first build a parsed draft and then visually verify it against rendered PDF pages before treating it as final.
- Only include `## 3. 报告中的并列对象与共享字段整理` when the PDF actually contains comparable parallel items with shared fields or metrics.
- In section 3, add a `数据来源：...` line immediately before the table, and make the page source explicit and 1-based.
- The table in section 3 must be exhaustive for the repeated parallel set covered by the report or section being summarized.
- Use rows for parallel items and columns for shared fields or metrics.
- Prefer numeric shared metrics when the report provides stable comparable numbers; otherwise use the fullest stable shared schema you can reliably read.
- Prefer the fullest stable schema you can reliably read; do not intentionally drop rows just to keep the table short.
- If the document contains many parallel items, continue the table in Markdown rather than switching to a selective summary.
- If some field or metric values are missing or unreadable for a given row, leave the cell blank or mark it as unavailable.
- In `字段/指标说明`, explain only the fields or metrics that are non-obvious or important for interpretation.
- The preferred final artifact is a Markdown document unless the user explicitly asks for another export format.
