---
name: report-benchmark-groundtruth-builder
description: Build benchmark groundtruth bundles from a parsed report summary and its query recommendations. Use when Codex receives a report summary Markdown file plus a query-recommendations Markdown file, and needs to produce per-query groundtruth containing the direct source data visible in the report, the fully reasoned final chart-ready data, runnable Python chart code, rendered chart images, and a Markdown record of the full output.
---

# Report Benchmark Groundtruth Builder

## Overview

Use this skill to turn one or more recommended chart queries into benchmark-ready groundtruth artifacts.

The required output is not only the final answer. It is a reproducible bundle: direct source data in JSON, reasoned chart data in JSON, code, image, and Markdown documentation.

## Inputs

Expect two primary inputs:

- a parsed report summary Markdown file
- a query recommendations Markdown file derived from that summary

If the user gives only the query file, recover the summary path from its `Source file` line when possible.

## Per-Query Deliverables

For each selected query, produce all of the following:

1. direct source data needed to answer the query, restricted to values that appear explicitly in the report summary
2. runnable Python reasoning code named `reasoning.py` that transforms the direct source data into the final chart-ready data
3. final chart-ready data after all reasoning and derivation steps
4. runnable Python code that renders the requested chart
5. a rendered chart image
6. a Markdown explanation that records the query, source fields, derivation steps, and artifact paths

Do not stop at analysis. Finish the full bundle unless the user explicitly asks for a draft only.

## Workflow

1. Read the summary Markdown and the query recommendations Markdown together.
2. Choose the target query or queries.
3. Parse the query carefully to recover:
   - entity scope
   - filters
   - direct source fields
   - derived metric definitions
   - sorting or ranking rules
   - top `N` or final subset rule
   - chart type
   - display unit
4. Extract only the direct values that are explicitly visible in the summary and needed for that query.
5. Preserve those direct values in a machine-readable JSON artifact before any transformation.
6. Validate the direct source JSON before any reasoning:
   - confirm every required visible field for the query is present or explicitly marked unavailable
   - confirm numeric values are stored as JSON numbers and units are separated from values
   - confirm the saved direct source rows are sufficient to reproduce the planned derivation
7. Write a runnable Python script named `reasoning.py` that reads or defines the direct source data and applies the full reasoning chain step by step until it produces the final chart-ready dataset.
8. Execute `reasoning.py` and save the final chart-ready dataset in a machine-readable JSON artifact.
9. Validate the final chart-ready JSON immediately after it is produced:
   - confirm every row and field required by the query is present
   - confirm filters, ranking, sorting, top `N`, and unit normalization were applied correctly
   - confirm every derived value can be traced back to saved direct source data
   - confirm the final dataset matches the exact chart specification rather than a nearby interpretation
10. Write Python chart code that reads or defines the final chart-ready data and renders the requested chart.
11. Execute the chart code and save the image.
12. Validate the rendered chart artifact:
   - confirm the chart file exists and is readable
   - confirm the plotted entities, order, labels, units, and chart type match the query
   - confirm the chart reflects the validated final chart-ready JSON rather than stale or edited-by-hand data
13. Write a Markdown record covering the full groundtruth for the query, including validation notes and any residual ambiguity.

## Groundtruth Rules

- Treat `direct source data` and `final chart-ready data` as different layers and save both as JSON.
- Treat `reasoning.py` as the explicit transformation layer between those two JSON artifacts.
- Direct source data must remain as close as possible to the report-visible values.
- Final chart-ready data must be the exact data needed to render the requested chart.
- All quantitative values in both JSON artifacts must be stored as JSON numbers, not numeric-looking strings.
- Do not store values such as `"$59.2B"` or `"41.49%"` in the value field. Store the numeric value separately from its unit.
- Every derived value in the final dataset must be traceable back to saved direct source data.
- The derivation path from direct source JSON to final chart-ready JSON must be executable from `reasoning.py`, not only described in prose.
- Validate each artifact at the point it is created rather than waiting until the end of the run.
- If validation fails at any stage, fix the artifact and rerun the relevant downstream steps before marking the query complete.
- If the query requires filtering, ranking, or top `N` selection, show that logic explicitly in the Markdown record.
- If units are normalized during reasoning, record both the original visible unit and the normalized unit.
- If a query is ambiguous, resolve it conservatively and document the choice.
- Do not invent missing source values. If an input value is unavailable, document the gap and stop that query or mark it incomplete.

## Chart Code Rules

- Prefer Python with `seaborn` and `pandas` unless the user requests a different plotting stack.
- Make the script runnable offline from the local workspace.
- Save the chart to disk instead of only displaying it interactively.
- Use deterministic ordering, labels, and axis formatting.
- Keep the chart faithful to the query specification rather than aesthetically elaborate.
- Keep the code self-contained enough that another agent can rerun it without hidden state.

## Markdown Output Requirement

In this skill, the Markdown report is a required artifact.

For every run:

1. show the result to the user
2. save the same result to a Markdown file

Use the directory and naming rules in `references/artifact-layout.md`.

The saved Markdown must include:

- source summary path
- source query-recommendations path
- selected query ids or titles
- artifact paths
- direct source data summary
- reasoning code path
- reasoning steps
- validation checks and outcomes for direct source data, reasoning output, and chart output
- final chart-ready data summary
- chart code path
- chart image path

## Validation Standard

Before considering a query complete, verify all of the following:

- the direct source data is sufficient to reproduce the reasoning
- `reasoning.py` reproduces the transformation from direct source data to final chart-ready data
- the final chart-ready data matches the query specification
- the final chart-ready data has the correct filtered subset, ordering, units, and derived values
- the Python code runs successfully
- the chart image is actually created
- the chart content matches the validated final chart-ready data
- the Markdown record points to the correct artifact paths

At minimum, the validation record should explicitly answer:

- Was the direct source JSON checked against the visible source values?
- Was the final chart-ready JSON checked against the query specification?
- Was the transformation logic in `reasoning.py` rerun after fixes, if any?
- Was the rendered chart checked against the final chart-ready JSON?

## Resources

- `references/output-format.md`: required Markdown structure for the saved groundtruth record
- `references/artifact-layout.md`: required folder and file naming layout
- `references/groundtruth-schema.md`: required content for direct data and final chart-ready data artifacts
