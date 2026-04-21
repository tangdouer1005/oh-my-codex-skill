# Reasoning Patterns

Use these patterns to transform section-3 extractions into benchmark-worthy chart queries.

## Good Patterns

### 0. Long-Chain Benchmark Pattern

Prefer candidates that require a pipeline like:

1. filter or select a subset of entities
2. retrieve direct values from multiple blocks
3. compute one or more derived metrics
4. rank or sort entities by the derived metric
5. keep the top `N` or otherwise prune to a final subset
6. render the chart

Why it is good:

- It creates a longer and more realistic reasoning chain.
- It avoids benchmark items that are solved by one join and one arithmetic operation.
- It makes errors easier to diagnose because failures can occur at filtering, joining, derivation, ranking, or subset selection.

## Diversity Axes

When assembling a set of recommended queries, vary along these axes instead of repeating one successful pattern:

### A. Entity-Scope Diversity

Alternate among:

- all markets
- only US city ecosystems
- region and subregion comparisons
- parent-child hierarchies
- other coherent subsets supported by the source

### B. Metric-Family Diversity

Alternate among:

- efficiency metrics such as `Funding / Deals`
- concentration metrics such as `top-deal sum / Funding`
- growth metrics
- rank-gap metrics
- share-of-parent metrics
- divergence metrics between two derived values

### C. Chart Diversity

Alternate among:

- ranked bars for ordered comparisons
- scatter plots for two-derived-metric relationships
- bubble charts when a third quantitative channel adds value
- dumbbell or slope charts for before-versus-after comparisons
- heatmaps only when a matrix structure is genuinely present

### D. Selection Diversity

Alternate among:

- top `N`
- bottom `N`
- largest positive gap
- largest negative gap
- highest concentration
- strongest acceleration

Do not default to `top 10` ranked bars for everything.

### 1. Ratio From Two Visible Measures

Combine two fields that appear separately to form a new metric.

Examples:

- `Funding / Deals` to estimate average capital per deal
- `Top 5 deal sum / quarterly funding` to estimate concentration
- `Submarket funding / parent-market funding` to estimate share capture

Why it is good:

- It forces intermediate calculation before rendering.
- The chart can target the derived metric rather than a copied series.

### 2. Time-Window Aggregation

Aggregate multiple visible periods into a new comparison window.

Examples:

- compare `2025 Q1-Q4` against `2024 Q1-Q4`
- compare `Q4'25` against the `2024 quarterly average`
- compare pre-spike and post-spike averages

Why it is good:

- It requires window selection, aggregation, and then comparison.

### 3. Cross-Block Comparison

Join metrics from different blocks that describe the same entity.

Examples:

- quarterly funding trend plus annual deal-stage mix
- annual stage mix plus top-equity-deal concentration
- region totals plus child-market totals

Why it is good:

- The model must resolve entity identity across pages and field groups.

### 4. Concentration And Dispersion

Measure how capital is distributed instead of plotting raw totals.

Examples:

- top-1 or top-5 deal share within quarterly funding
- gap between first and fifth largest deals
- dispersion of average deal size across markets

Why it is good:

- The query depends on reconstructing a mini dataset from ranked rows.

### 5. Divergence Queries

Compare two kinds of momentum that do not necessarily move together.

Examples:

- funding growth versus deal-count growth
- stage skew versus average deal size
- parent-market share versus local concentration

Why it is good:

- These queries create more diagnostic charts and surface reasoning failures clearly.

### 6. Derived-Ranking Queries

Rank entities only after computing a derived metric that is not explicitly listed in the source.

Examples:

- compute average funding per deal for every market, then keep the top 10
- compute top-deal concentration for every city, then keep the top 5
- compute funding-growth-minus-deal-growth for every region, then rank descending

Why it is good:

- It forces the model to derive the sortable field first.
- It prevents "top N" from being copied from a visible ranking table.

## Anti-Patterns

Reject or downgrade these unless the user explicitly wants easy items.

### Direct Plot

- plot one visible time series
- rank markets by one already visible total
- show stage percentages exactly as listed
- take the visible top 5 rows from one table and chart them without any new ranking step
- generate five queries that all use the same ranking-and-bar-chart pattern with only cosmetic metric changes

Why reject:

- No derivation step
- Minimal reasoning burden

### Over-Speculative Composite Score

- build a custom index from loosely related fields without a clear formula

Why reject:

- Annotation becomes unstable
- Different annotators may invent different formulas

### Unsupported Join

- compare entities across hierarchy levels without a clear denominator
- combine annual and quarterly fields without stating the alignment rule

Why reject:

- The resulting dataset is ambiguous

## Example Ideas For State of AI 2025 Geographic Trends

These are examples of the style to recommend, not mandatory outputs.

1. Create a ranked horizontal bar chart comparing `2025 Q4` average funding per deal across the major US ecosystems, where average funding per deal is defined as `Funding / Deals`, values are expressed in `USD millions per deal`, and bars are sorted from highest to lowest.
2. Create a ranked horizontal bar chart showing the top 10 markets by `2025 Q4` funding concentration, after computing for every market the ratio `sum of visible Top equity deals in Q4'25 Round Amounts / 2025 Q4 Funding`, expressing the result as a percentage, and sorting from highest to lowest.
3. Create a ranked horizontal bar chart showing the top 8 markets by `2025` capital-intensity acceleration, where the metric is `(2025 total Funding / 2025 total Deals) - (2024 total Funding / 2024 total Deals)`, values are expressed in `USD millions per deal`, and markets are sorted from highest to lowest.
4. Create a bubble chart for the top 6 submarkets by `2025 Q4` share of parent-region funding, where the x-axis is `child Q4 Funding / parent-region Q4 Funding`, the y-axis is `sum of visible child Top equity deals / child Q4 Funding`, both are percentages, and bubble size represents `child Q4 Funding`.
5. Create a ranked horizontal bar chart showing the top 10 markets by the gap between `2025 Q4` average funding per deal and `2025 Early-stage deal share`, after converting average funding per deal to `USD millions` and sorting descending by the derived gap.

## Calibration Rule

If a candidate query can be solved by reading one row group and plotting it directly, it is usually below the benchmark bar.

If a candidate query requires:

- filtering or selecting the relevant entities
- selecting entities
- joining fields across blocks
- computing intermediate values
- ranking the entities by a derived metric
- selecting the top `N` after the ranking step
- and only then charting

it is usually in scope.

If a recommended batch repeats that same chain in almost identical form across all items, the batch is not diverse enough even if each item is individually valid.
