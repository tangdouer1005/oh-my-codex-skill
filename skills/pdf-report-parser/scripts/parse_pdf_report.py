#!/usr/bin/env python3
"""Extract page text from a PDF report and generate a draft Markdown summary."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "Missing dependency: pypdf. Install it with `python -m pip install pypdf`."
    ) from exc


HEADING_PATTERNS = [
    re.compile(r"^\d+(\.\d+)*\s+\S+"),
    re.compile(r"^第[一二三四五六七八九十百0-9]+[章节部分篇]\s*\S*"),
    re.compile(r"^[A-Z][A-Z0-9 /:&-]{5,}$"),
]


@dataclass
class PageInfo:
    page: int
    heading: str | None
    preview: str
    char_count: int


@dataclass
class SectionRange:
    start_page: int
    end_page: int
    label: str
    preview: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract PDF pages and create a draft Markdown report summary."
    )
    parser.add_argument("pdf_path", type=Path, help="Path to the input PDF report.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to the output Markdown file. Defaults to <pdf-stem>-summary.md.",
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        type=Path,
        help="Optional path to write structured page extraction data as JSON.",
    )
    parser.add_argument(
        "--max-snippet-chars",
        type=int,
        default=240,
        help="Maximum characters to include in section previews.",
    )
    return parser.parse_args()


def normalize_whitespace(text: str) -> str:
    text = text.replace("\x00", " ")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def clean_inline(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def detect_heading(lines: list[str]) -> str | None:
    candidates = []
    for line in lines[:8]:
        stripped = line.strip()
        if len(stripped) < 4:
            continue
        if any(pattern.match(stripped) for pattern in HEADING_PATTERNS):
            candidates.append(stripped)
            continue
        if len(stripped) <= 80 and not stripped.endswith(("。", ".", ";", "；", ":", "：")):
            candidates.append(stripped)
    return candidates[0] if candidates else None


def extract_pages(pdf_path: Path, max_snippet_chars: int) -> list[PageInfo]:
    reader = PdfReader(str(pdf_path))
    pages: list[PageInfo] = []
    for index, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text() or ""
        normalized = normalize_whitespace(raw_text)
        lines = normalized.splitlines()
        heading = detect_heading(lines)
        preview_source = clean_inline(normalized)
        if not preview_source:
            preview_source = "[No extractable text found on this page]"
        pages.append(
            PageInfo(
                page=index,
                heading=heading,
                preview=truncate(preview_source, max_snippet_chars),
                char_count=len(preview_source)
                if preview_source != "[No extractable text found on this page]"
                else 0,
            )
        )
    return pages


def infer_report_topic(pages: list[PageInfo]) -> str:
    for page in pages[:3]:
        if page.heading:
            return page.heading
        if page.preview and not page.preview.startswith("[No extractable"):
            sentences = re.split(r"[。.!?]", page.preview)
            first = clean_inline(sentences[0])
            if len(first) >= 10:
                return truncate(first, 80)
    return "The report topic could not be inferred reliably from extracted text."


def make_label(page: PageInfo) -> str:
    if page.heading:
        return page.heading
    if page.char_count == 0:
        return "Text extraction failed or the page is image-based"
    return "Untitled section"


def build_ranges(pages: list[PageInfo]) -> list[SectionRange]:
    if not pages:
        return []

    ranges: list[SectionRange] = []
    current_label = make_label(pages[0])
    start_page = pages[0].page
    preview_parts = [pages[0].preview]

    for page in pages[1:]:
        page_label = make_label(page)
        same_group = page_label == current_label or (
            current_label == "Untitled section" and page_label == "Untitled section"
        )
        if same_group:
            preview_parts.append(page.preview)
            continue

        ranges.append(
            SectionRange(
                start_page=start_page,
                end_page=page.page - 1,
                label=current_label,
                preview=truncate(clean_inline(" ".join(preview_parts)), 240),
            )
        )
        current_label = page_label
        start_page = page.page
        preview_parts = [page.preview]

    ranges.append(
        SectionRange(
            start_page=start_page,
            end_page=pages[-1].page,
            label=current_label,
            preview=truncate(clean_inline(" ".join(preview_parts)), 240),
        )
    )
    return merge_adjacent_untitled_ranges(ranges)


def merge_adjacent_untitled_ranges(ranges: list[SectionRange]) -> list[SectionRange]:
    if not ranges:
        return []

    merged = [ranges[0]]
    for section in ranges[1:]:
        previous = merged[-1]
        can_merge = (
            previous.label == section.label == "Untitled section"
            or previous.label == section.label == "Text extraction failed or the page is image-based"
        )
        if can_merge and previous.end_page + 1 == section.start_page:
            previous.end_page = section.end_page
            previous.preview = truncate(
                clean_inline(f"{previous.preview} {section.preview}"), 240
            )
            continue
        merged.append(section)
    return merged


def build_markdown(topic: str, sections: list[SectionRange], pages: list[PageInfo]) -> str:
    low_text_pages = [page.page for page in pages if page.char_count < 40]
    bullet_lines = []
    for section in sections:
        if section.start_page == section.end_page:
            page_label = f"第 {section.start_page} 页"
        else:
            page_label = f"第 {section.start_page} 页到第 {section.end_page} 页"
        bullet_lines.append(
            f"- {page_label}：{section.label}。依据文本提取，初步内容为：{section.preview}"
        )

    notes = ""
    if low_text_pages:
        joined = ", ".join(str(page) for page in low_text_pages[:10])
        notes = (
            "\n## Notes\n"
            f"- 提取文本较少的页码：{joined}。这些页面可能需要人工复核或 OCR。\n"
        )

    heading_counter = Counter(page.heading for page in pages if page.heading)
    top_headings = [heading for heading, _ in heading_counter.most_common(3)]
    heading_hint = ""
    if top_headings:
        heading_hint = "可见标题线索包括：" + "；".join(top_headings) + "。"

    return (
        "# PDF Report Summary\n\n"
        "## 1. 这个报告主要讲的什么\n"
        f"初步判断，这份报告主要围绕“{topic}”展开。"
        f"{heading_hint}请结合全文对这段总结进行进一步润色，补充报告目标、方法、主要发现和结论。\n\n"
        "## 2. 从第几页到第几页讲到什么\n"
        + "\n".join(bullet_lines)
        + notes
        + "\n"
    )


def main() -> int:
    args = parse_args()
    pdf_path: Path = args.pdf_path.expanduser().resolve()
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    output_path = args.output or pdf_path.with_name(f"{pdf_path.stem}-summary.md")
    output_path = output_path.expanduser().resolve()

    pages = extract_pages(pdf_path, args.max_snippet_chars)
    sections = build_ranges(pages)
    topic = infer_report_topic(pages)
    markdown = build_markdown(topic, sections, pages)
    output_path.write_text(markdown, encoding="utf-8")

    if args.json_path:
        json_path = args.json_path.expanduser().resolve()
        payload = {
            "pdf_path": str(pdf_path),
            "topic_hint": topic,
            "pages": [asdict(page) for page in pages],
            "sections": [asdict(section) for section in sections],
        }
        json_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    print(f"Wrote Markdown summary draft to: {output_path}")
    if args.json_path:
        print(f"Wrote JSON extraction data to: {args.json_path.expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
