---
name: pdf-report-parser
description: Parse PDF reports and generate Markdown summaries. Use when Codex needs to read a report-style PDF, explain what the document is mainly about, and produce a page-range outline showing what is covered from which page to which page.
---

# PDF Report Parser

Use this skill to turn a report-style PDF into a Markdown summary document with two always-required outputs, plus one user-triggered output when the report contains comparable parallel items:

1. A short explanation of what the report is mainly about
2. A page-range outline describing what each span of pages covers
3. When the report presents parallel items with shared fields or metrics and the user has selected the objects and fields to extract, a complete matrix-style table whose rows are the parallel items and whose columns are the shared fields or metrics, followed by a brief explanation of what the important columns mean when needed

This skill should be paired with the [$pdf](/Users/tangjiahui/.codex/skills/pdf/SKILL.md) skill when reading PDFs in this environment. The `$pdf` skill is responsible for accessing PDF content in a layout-aware way, while `pdf-report-parser` is responsible for turning that reading into a polished Markdown summary.

## Human-in-the-Loop Workflow

This skill uses a collaborative two-stage workflow by default:

1. In the first pass, produce only section 1 and section 2.
2. Stop and let the user choose the target objects and exact fields or metrics for section 3.
3. In the second pass, extract the requested section 3 in two sub-steps:
   - First create a parsed draft using programmatic extraction, text extraction, or other lightweight structured extraction methods.
   - Then render all relevant PDF pages and visually audit every requested row and every requested field against the page layout.
4. Treat the fully visually checked version as the final source of truth. If the parsed draft and the visual reading disagree, correct the draft manually.

Do not proactively generate section 3 in the first pass unless the user explicitly asks for it and has already specified the objects and fields to extract.

## Workflow

1. First use the [$pdf](/Users/tangjiahui/.codex/skills/pdf/SKILL.md) skill to access the PDF content, preferring rendered pages or other layout-aware reading methods over raw text extraction.
2. Read the PDF as a document, not as an unstructured text dump.
3. Identify the report's overall purpose from the title page, executive summary, table of contents, repeated section headings, and conclusion pages.
4. Review the PDF page by page and note where the topic clearly shifts.
5. Rewrite the summary section so it clearly answers "这个报告主要讲的什么".
6. Rewrite the page-range outline so each range is concise, accurate, and based on what is actually visible in the PDF.
7. In the first pass, stop after section 1 and section 2 unless the user has already specified the objects and fields for section 3.
8. If the user asks for section 3, first identify the relevant repeated parallel layout such as company cards, ranked lists, market maps, vendor profiles, benchmark tables, trend lists, section modules, or other side-by-side items with shared fields or metrics.
9. Build a first-draft table using parsing or structured extraction.
10. Render all relevant source pages and visually verify every requested row and every requested field against the PDF layout before finalizing the table.
11. Add the third section only after that visual audit, first stating the data source pages for the table, then presenting the corrected matrix-style table, then explaining the meaning of the important columns below the table when needed.
12. If the PDF has obvious section headers, preserve them in the final Markdown. If not, infer section boundaries from topic shifts across adjacent pages.
13. Produce the final deliverable as Markdown unless the user explicitly asks for another format.

## Reading Approach

- Prefer using the [$pdf](/Users/tangjiahui/.codex/skills/pdf/SKILL.md) skill for PDF access and visual inspection before relying on plain text extraction.
- Use visible structure on the page: title blocks, table of contents, section dividers, chart captions, repeated headers, appendix labels, and methodology pages.
- Watch for repeated parallel templates, especially pages that reuse the same slots such as company name, location, stage, total raised, headcount, score, maturity, ranking, trend name, section name, page span, or topic label.
- Treat the repeated slots in those templates as candidate columns, and treat each card / profile / row / trend / section as one row in the final matrix table.
- When the PDF is long, first skim the title page, contents page, section opener pages, and ending pages, then fill in the intermediate ranges.
- If a page is mostly charts or images, describe only what can be supported by visible headings, captions, and nearby pages.
- If you need to sanity-check page numbers or section boundaries, inspect neighboring pages before merging them into one range.
- In the first pass, focus on section 1 and section 2 and avoid spending time extracting section 3 before the user has chosen the target objects and fields.
- When preparing section 3 after user selection, start with structured extraction to create a draft, then verify it visually on all relevant rendered pages.
- When extracting the third section, prefer VLM-style visual reading of rendered pages over OCR post-processing or rule-based parsing scripts for final verification.
- Do not stop after spot checks, sampling, or representative-page review when section 3 is requested; the required standard is full visual verification of the complete extracted table.
- Read chart labels, table cells, legends, headers, footnotes, and repeated row structures directly from the rendered page image whenever possible.
- Use scripts for page rendering, image generation, lightweight navigation help, and first-draft extraction, but do not treat them as the final source of truth for the third section's values.

## Output Requirements

Always structure the content according to [references/output-format.md](references/output-format.md), then return the final deliverable as Markdown.

The final answer must:

- Keep page numbers explicit and 1-based
- Merge adjacent pages only when they describe the same topic or section
- Avoid inventing content for image-heavy, scan-heavy, or low-legibility pages
- Prefer report headings over guesswork when headings are visible
- State uncertainty briefly when page visibility or readability is weak
- In the default first-pass workflow, return only section 1 and section 2
- Add the third section only when there is a real set of comparable parallel items and shared fields or metrics in the PDF and the user has specified what objects and fields to extract
- Parallel items can include companies, cities, countries, investors, products, trends, topics, sections, markets, or other repeated report objects that can be meaningfully compared side by side
- When the third section is included, the table must be exhaustive for the parallel items covered by that repeated template, not a representative subset
- When the third section is included, explicitly state the source pages for the table before the table itself, for example `数据来源：第 20 页到第 22 页`
- Build the table only from fields that are visible or directly inferable from the page layout and headings
- Create a parsed first draft of third-section values before visual review when possible
- Extract final third-section values by visually reading the page layout with the model and correcting the parsed draft as needed
- Visually review every row and every requested field in the final third-section table; do not rely on sampled checks as sufficient validation
- If a programmatic extraction and the visual reading disagree, trust the visual reading and correct the table manually
- Prefer numeric shared metrics when the document provides stable comparable numbers across rows; if not, use the most stable shared structured fields available and keep column meaning consistent
- Orient the table as: columns = shared fields or metrics, rows = parallel items
- Explain important field or metric meanings briefly below the table, especially for domain-specific labels such as Mosaic, Commercial Maturity, Total Raised, or Headcount
- Prefer Markdown as the final output artifact unless the user explicitly asks for PDF or another export format

## Heuristics

When analyzing the PDF:

- Treat the first strong heading or title-like lines as a clue to the overall report topic
- Use repeated headings, numbered sections, section divider pages, and abrupt topic changes to identify page boundaries
- Keep each range description short, usually one sentence
- If every page is about a different subtopic, list smaller ranges rather than forcing broad merges
- Use contents pages to validate the outline, but prefer the actual body pages if the contents page is outdated or abbreviated
- Separate appendices, references, legal notices, and methodology sections from the main narrative when possible
- If many pages share the same profile template, identify the full shared schema once and then populate it exhaustively across all parallel items in the third section
- If the parallel set spans many pages, continue the same table in Markdown rather than dropping rows or switching to a selective summary
- If some cells are unreadable or unavailable, leave those cells blank or mark them as unavailable; do not omit the row entirely
- For dense chart pages, extract values in a parsed draft first when helpful, then complete a full visual pass over the final table against the rendered pages
- For repeated deal tables or market snapshots, verify row alignment visually because investor names, valuation fields, and country columns often shift under OCR or text extraction
- For long repeated sections such as country cards, company profiles, or rankings spanning many pages, keep track of reviewed pages and do not mark the extraction complete until every relevant page has been visually checked

## Resources

- [$pdf](/Users/tangjiahui/.codex/skills/pdf/SKILL.md): use this skill first to read or visually inspect the PDF in a layout-aware way
- `references/output-format.md`: required final Markdown structure and wording guidance

## Failure Modes

- If the PDF is mostly scanned pages, low-resolution images, or unreadable charts, say so and avoid making strong claims.
- If the report contains appendices, references, or legal notices, separate them from the main body when possible.
- If page headings, contents pages, and body pages disagree, trust the body pages and note uncertainty briefly.
- If the user has not yet selected the objects and fields for section 3, do not guess them and do not auto-generate the table.

## Notes

- In this environment, do not assume the model can natively read any local PDF path without help. Use the [$pdf](/Users/tangjiahui/.codex/skills/pdf/SKILL.md) skill as the default way to access PDF content.
- `scripts/parse_pdf_report.py` may still exist in this skill directory as a legacy helper, but it is not the default workflow for this skill.
- The preferred behavior in pass one is direct reading and manual analysis of the PDF, followed by a polished Markdown report containing only section 1 and section 2.
- For third-section data extraction, the preferred behavior is a parsed first draft followed by visual/VLM-based verification and manual correction.
- For third-section data extraction, full-table visual verification is required; sampling is not sufficient unless the user explicitly asks for a rough draft instead of a final checked result.
