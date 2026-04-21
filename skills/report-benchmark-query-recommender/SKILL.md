---
name: report-benchmark-query-recommender
description: Recommend benchmark chart queries from structured third sections of parsed report summaries. Use when Codex receives a Markdown summary extracted from a PDF report, especially one whose third section contains repeated comparable markets, companies, regions, products, or entities with shared metrics, and needs query recommendations for a multimodal chart benchmark where the PDF is the context and the query must require combining evidence from multiple places and deriving new values instead of directly plotting a visible table.
---

# Report Benchmark Query Recommender

## Overview

Use this skill to convert a report's structured third section into benchmark-worthy chart query recommendations.

The target benchmark is not "read one table and draw it." The target benchmark is "read a multimodal PDF, trace evidence across multiple places, derive missing values, and only then render a chart."

## Workflow

1. Read the report summary and isolate section 3 or the equivalent structured extraction block.
2. Identify the repeated entity level in that section, such as market, city, country, company, investor, category, or time period.
3. List the shared fields that appear across entities, then separate them into:
   - directly plottable fields
   - derivation ingredients
   - context fields that can support filtering, segmentation, ranking, or hierarchy
4. Prefer fields that come from different tables, subsections, or pages, because those are the best raw material for reasoning-heavy benchmark queries.
5. Generate candidate derived metrics before writing any query. Typical examples include growth, share, concentration, ratio, gap, acceleration, ranking change, and composite comparisons.
6. Reject candidate queries that can be answered by directly copying one visible series into a chart.
7. Keep only candidates that are answerable from the report context without external data.
8. Return the recommendations using `references/output-format.md`.
9. Save the full generated output to a Markdown file in addition to showing it to the user.

## Benchmark Fit Criteria

A strong benchmark query should satisfy most of these conditions:

- Require combining at least two evidence locations from the PDF or parsed summary
- Prefer a multi-step reasoning chain rather than a single derivation
- Require one or more derived values before charting
- Produce a chart with a clear analytic purpose instead of a decorative visualization
- Be specific enough that two competent annotators would derive roughly the same dataset
- Stay grounded in the report rather than relying on outside facts
- Expose likely failure modes for multimodal reasoning, such as cross-page joins, hierarchy resolution, time-window aggregation, unit normalization, or top-N concentration

Prefer queries whose derivation path looks like:

1. select or filter the relevant objects
2. gather direct values from multiple tables, blocks, or pages
3. compute one or more derived metrics
4. sort or rank the resulting entities
5. keep the top `N` or another explicit subset
6. render the final chart

This longer chain is usually better aligned with the benchmark than a query that only needs one join and one formula.

Treat the following as weak queries unless the user explicitly asks for simpler items:

- "Plot quarterly funding for each market"
- "Show the top 5 deals in Q4"
- "Make a bar chart of deal-stage percentages"

These are too close to direct transcription.

## Query Construction Rules

- Write the query as a user-facing chart request, not as an annotation instruction.
- Write the query as a complete natural-language instruction that is specific enough to be executed directly by a chart-generation system.
- State the chart type inside the query itself, not only in the surrounding metadata.
- State the target entities, the derived metric, the comparison window, and the aggregation rule inside the query itself.
- State the unit inside the query itself whenever the plotted value is monetary, percentage-based, ratio-based, or derived from multiple units.
- State sorting, filtering, inclusion, and exclusion rules inside the query itself when they matter.
- Prefer queries that explicitly require ranking, sorting, or top-`N` selection after the derived metric is computed.
- State whether values should be shown as absolute values, percentages, multiples, basis-point changes, or growth rates.
- Mention any necessary normalization rule inside the query itself, such as converting all money to `$B` or `$M`.
- Prefer charts that make the reasoning necessary. If the key value is a ratio or delta, recommend a chart type that foregrounds that value.
- If a recommendation depends on a mild inference rather than an explicit report metric, label that inference clearly in the rationale.
- If the report contains hierarchical geography, allow cross-level comparisons only when the denominator is well defined.
- If the report mixes annual and quarterly fields, ensure the query states how to align the time windows.
- Avoid vague prompts such as "compare", "show trends", or "visualize concentration" unless the query also defines exactly how that comparison should be computed and displayed.

Use this mental template when drafting the final query:

`Create a [chart type] showing [entity scope] by [derived metric], using [source periods / fields], with values expressed in [unit], sorted by [rule], and limited to [filters].`

For stronger benchmark candidates, prefer an expanded template:

`Create a [chart type] for the top [N] [entities] after filtering to [scope], where the plotted value is [derived metric], computed from [source fields / tables], expressed in [unit], sorted by [ranking rule], and restricted to [inclusion / exclusion rule].`

## Selection Heuristics

- Prefer "ingredient diversity": time series plus ranked deals, stage mix plus funding totals, region totals plus subregion totals.
- Prefer longer reasoning chains such as:
  - filter entities first
  - join multiple evidence blocks
  - compute derived metrics
  - rank the entities
  - keep top `N`
  - then chart
- Prefer datasets that force intermediate computation, such as:
  - average funding per deal
  - top-deal concentration share
  - year-over-year or period-over-period change
  - share captured by a submarket within a parent geography
  - funding momentum versus deal momentum
  - stage structure versus realized capital concentration
- Prefer candidates where the top `N` is not directly visible in the source and must be determined after derivation.
- Prefer queries with moderate complexity. Avoid queries that require too many speculative assumptions or overly deep reconstruction.
- When several candidates are similar, keep the one with the cleanest derivation path and strongest chart payoff.

## Diversity Requirement

Judge diversity at the query-set level, not only at the single-query level.

When recommending multiple queries, do not produce a list where every item is just a small variation of the same pattern. Aim for diversity across all of the following dimensions:

- entity scope: global markets, subregions, city ecosystems, parent-child geographies, or other distinct object sets
- reasoning pattern: filtering, cross-block joins, time aggregation, ratio construction, concentration analysis, ranking after derivation, parent-child share analysis, divergence analysis
- final selection rule: top `N`, bottom `N`, largest gap, highest concentration, biggest acceleration, strongest divergence, or other explicit subset logic
- chart type: bar, scatter, bubble, dumbbell, line, slope, heatmap, or other chart forms that fit the metric
- metric family: absolute derived value, share, concentration, growth, gap, rank difference, dispersion, or composite but well-defined derived value
- time scope: single quarter, quarter-over-quarter, year-over-year, full-year aggregation, or mixed annual-versus-quarterly alignment when justified

Use these set-level rules:

- Do not let more than two recommended queries share the same core reasoning template.
- Do not let most queries use the same chart type unless the data genuinely supports little else.
- Do not let all queries focus on the same entity level, such as only cities or only countries.
- Include a mix of ranking-based queries and relationship-based queries.
- Include at least one query where the final plotted subset is determined after deriving a new metric rather than copied from a visible ranking.
- Include at least one query that uses parent-child hierarchy or cross-block alignment if the source supports it.
- Include at least one query that compares two derived metrics in the same chart if the source supports it.

If two candidate queries differ only by swapping one metric, one geography, or one time window, treat them as near-duplicates and keep only the stronger one.

Before finalizing the recommendation list, scan it for redundancy and replace repetitive items with a different reasoning pattern, chart type, or entity scope.

## Output Standard

Always follow `references/output-format.md`.

In this skill, writing the result to Markdown is part of the task, not an optional extra.

Before listing recommendations, briefly summarize:

- what the repeated entities are
- which fields are available
- which field combinations create the best reasoning opportunities

Then provide a ranked list of recommended queries. Each recommendation must explain why it is benchmark-worthy and what derivation work is required.

Recommend at least 10 queries by default unless the user explicitly asks for a different number.

The `Query` line is the primary artifact. It should stand on its own even if the reader ignores the other bullets.

The final list should read like a balanced benchmark slice rather than a cluster of near-duplicate prompts.

## Markdown Output Requirement

Every time this skill is used to generate recommendations, do both of the following:

1. show the result in the assistant response
2. save the same result to a Markdown file

Treat the Markdown file as a required artifact.

Use these file rules unless the user explicitly requests a different path:

- If the input is a summary Markdown file, save the result in the same directory as the input file.
- Name the output file by appending `_queries` or `_query_recommendations` before the `.md` suffix.
- If a file with that name already exists and the user has not asked to preserve it, overwrite it with the latest full result.

The saved Markdown should contain the full recommendation package, not just the final query strings. Include:

- source file path
- section-3 assessment
- all recommended queries with all required fields
- excluded query types
- diversity check

If the user asks for only a subset later, you may create a second derived Markdown file, but the primary full-output Markdown artifact should still be written.

## Resources

- `references/output-format.md`: required response structure for recommendations
- `references/reasoning-patterns.md`: approved transformation patterns, anti-patterns, and examples tuned for report section 3
