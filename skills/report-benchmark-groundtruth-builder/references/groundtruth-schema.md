# Groundtruth Schema

Use these schemas for machine-readable artifacts.

## direct_data.json

```json
{
  "query_id": "query_01",
  "query_text": "exact query text",
  "source_summary_file": "/absolute/path/to/summary.md",
  "source_query_file": "/absolute/path/to/query_recommendations.md",
  "records": [
    {
      "entity": "Silicon Valley",
      "field_group": "Quarterly funding & deals",
      "field": "2025 Q4 Funding",
      "value": 59.2,
      "value_unit": "USD billions",
      "value_type": "currency",
      "source_section": "### Silicon Valley",
      "source_note": "directly visible in summary"
    }
  ]
}
```

Rules:

- store quantitative values as JSON numbers
- store the unit separately in `value_unit`
- if you need to mention the original display form, put it in metadata or notes, not in the numeric value field
- one record per direct value used in reasoning
- do not store derived values here

## final_chart_data.json

```json
{
  "query_id": "query_01",
  "query_text": "exact query text",
  "chart_type": "horizontal bar chart",
  "value_unit": "USD millions per deal",
  "sort_rule": "descending by avg_deal_size",
  "selection_rule": "top 5",
  "records": [
    {
      "entity": "Silicon Valley",
      "avg_deal_size": 188.54
    }
  ]
}
```

Rules:

- store only the final plotted rows after filtering, sorting, and top-`N` selection
- numeric values should be normalized and chart-ready
- quantitative fields inside `records` must be JSON numbers
- field names should match the plotted semantics
