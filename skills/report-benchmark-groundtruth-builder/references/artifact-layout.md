# Artifact Layout

Use this layout unless the user explicitly requests another structure.

If the summary input is:

`/path/to/report_summary.md`

create:

- Markdown record: `/path/to/report_groundtruth.md`
- Artifact root: `/path/to/report_groundtruth/`

Inside the artifact root, create one folder per query:

- `/path/to/report_groundtruth/query_01/`
- `/path/to/report_groundtruth/query_02/`
- and so on

Each query folder should contain:

- `direct_data.json`
- `final_chart_data.json`
- `chart.py`
- `chart.png`

Notes:

- `direct_data.json` stores only report-visible values required by the query
- `final_chart_data.json` stores the fully reasoned chart-ready data
- `chart.py` should render `chart.png`

If the query recommendation file already implies a numbering scheme such as `Query 1`, map it directly to `query_01`, `query_02`, and so on.

Overwrite existing artifacts when rerunning unless the user explicitly asks to preserve prior versions.
