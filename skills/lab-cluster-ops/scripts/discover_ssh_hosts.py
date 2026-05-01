#!/usr/bin/env python3
"""Summarize concrete SSH aliases from local SSH config files."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


HOME = Path.home()


@dataclass
class HostEntry:
    aliases: list[str]
    source: Path
    options: dict[str, str] = field(default_factory=dict)


def expand_include(base: Path, raw: str) -> list[Path]:
    pattern = raw.strip().strip('"').strip("'")
    pattern_path = Path(pattern).expanduser()
    if not pattern_path.is_absolute():
        pattern_path = (base.parent / pattern_path).resolve()
    return sorted(Path(p) for p in pattern_path.parent.glob(pattern_path.name))


def parse_file(path: Path, seen: set[Path]) -> list[HostEntry]:
    path = path.expanduser().resolve()
    if path in seen or not path.exists():
        return []
    seen.add(path)

    entries: list[HostEntry] = []
    current: HostEntry | None = None

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        lowered = line.lower()
        if lowered.startswith("include "):
            include_target = line.split(None, 1)[1]
            for include_path in expand_include(path, include_target):
                entries.extend(parse_file(include_path, seen))
            continue

        if lowered.startswith("host "):
            aliases = line.split()[1:]
            if aliases:
                current = HostEntry(aliases=aliases, source=path)
                entries.append(current)
            continue

        if current is None:
            continue

        if " " not in line and "\t" not in line:
            continue

        key, value = line.split(None, 1)
        current.options[key.lower()] = value.strip()

    return entries


def is_concrete_alias(alias: str) -> bool:
    return not any(ch in alias for ch in "*?!")


def format_value(entry: HostEntry, key: str, default: str = "-") -> str:
    return entry.options.get(key, default)


def main() -> int:
    config = HOME / ".ssh" / "config"
    entries = parse_file(config, seen=set())

    concrete_entries = [
        HostEntry(
            aliases=[alias],
            source=entry.source,
            options=entry.options,
        )
        for entry in entries
        for alias in entry.aliases
        if is_concrete_alias(alias)
    ]

    if not concrete_entries:
        print(f"No concrete SSH aliases found in {config}.")
        return 0

    header = [
        "ALIAS",
        "HOSTNAME",
        "USER",
        "PORT",
        "PROXYJUMP",
        "IDENTITYFILE",
        "SOURCE",
    ]
    rows: list[list[str]] = []

    for entry in concrete_entries:
        rows.append(
            [
                entry.aliases[0],
                format_value(entry, "hostname"),
                format_value(entry, "user"),
                format_value(entry, "port"),
                format_value(entry, "proxyjump"),
                format_value(entry, "identityfile"),
                str(entry.source),
            ]
        )

    widths = [len(col) for col in header]
    for row in rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len(value))

    def render(parts: Iterable[str]) -> str:
        return "  ".join(part.ljust(widths[idx]) for idx, part in enumerate(parts))

    print(render(header))
    print(render(["-" * width for width in widths]))
    for row in rows:
        print(render(row))

    return 0


if __name__ == "__main__":
    sys.exit(main())
