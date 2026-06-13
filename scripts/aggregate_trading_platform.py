#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/hanilbert/Networks_Rules"
AUTHOR = "hanilbert"

PREFERRED_ORDER = [
    "exness",
    "icmarkets",
    "thinkmarkets",
    "easymarkets",
    "metatrader",
    "ibkr",
    "futu",
    "tiger",
    "longbridge",
]

COUNT_ORDER = ["DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR"]
COUNT_HEADER_PATTERN = re.compile(r"^# [A-Z0-9-]+: \d+$")


@dataclass(frozen=True)
class Entry:
    kind: str
    value: str


@dataclass(frozen=True)
class RuleFile:
    path: Path
    name: str
    entries: list[Entry]


def sort_key(path: Path) -> tuple[int, str]:
    stem = path.stem.lower()
    try:
        return (PREFERRED_ORDER.index(stem), stem)
    except ValueError:
        return (len(PREFERRED_ORDER), stem)


def read_name(lines: list[str], fallback: str) -> str:
    for line in lines:
        if line.startswith("# NAME:"):
            return line.split(":", 1)[1].strip()
    return fallback


def trim_blank_edges(entries: list[Entry]) -> list[Entry]:
    start = 0
    end = len(entries)
    while start < end and entries[start].kind == "blank":
        start += 1
    while end > start and entries[end - 1].kind == "blank":
        end -= 1
    return entries[start:end]


def read_clash_rule(path: Path) -> RuleFile:
    lines = path.read_text(encoding="utf-8").splitlines()
    name = read_name(lines, path.stem)
    entries: list[Entry] = []
    in_payload = False

    for line in lines:
        stripped = line.strip()
        if stripped == "payload:":
            in_payload = True
            continue
        if not in_payload:
            continue
        if not stripped:
            entries.append(Entry("blank", ""))
        elif stripped.startswith("#"):
            entries.append(Entry("comment", stripped))
        elif stripped.startswith("- "):
            entries.append(Entry("rule", stripped[2:].strip()))

    return RuleFile(path, name, trim_blank_edges(entries))


def read_surge_rule(path: Path) -> RuleFile:
    lines = path.read_text(encoding="utf-8").splitlines()
    name = read_name(lines, path.stem)
    entries: list[Entry] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            entries.append(Entry("blank", ""))
        elif stripped.startswith("#"):
            if stripped.startswith("# NAME:") or stripped.startswith("# AUTHOR:"):
                continue
            if stripped.startswith("# REPO:") or stripped.startswith("# UPDATED:"):
                continue
            if stripped.startswith("# TOTAL:") or COUNT_HEADER_PATTERN.match(stripped):
                continue
            entries.append(Entry("comment", stripped))
        else:
            entries.append(Entry("rule", stripped))

    return RuleFile(path, name, trim_blank_edges(entries))


def build_sections(rule_files: list[RuleFile]) -> tuple[list[list[Entry]], Counter[str]]:
    seen_rules: set[str] = set()
    counts: Counter[str] = Counter()
    sections: list[list[Entry]] = []

    for rule_file in rule_files:
        section: list[Entry] = []
        has_rule = False
        first_nonblank = next((entry for entry in rule_file.entries if entry.kind != "blank"), None)
        if first_nonblank is None or first_nonblank.kind != "comment":
            section.append(Entry("comment", f"# {rule_file.name}"))

        for entry in rule_file.entries:
            if entry.kind != "rule":
                section.append(entry)
                continue
            normalized = entry.value.strip()
            if normalized in seen_rules:
                continue
            seen_rules.add(normalized)
            counts[normalized.split(",", 1)[0]] += 1
            section.append(Entry("rule", normalized))
            has_rule = True

        if has_rule:
            sections.append(trim_blank_edges(section))

    return sections, counts


def count_lines(counts: Counter[str]) -> list[str]:
    known = [rule_type for rule_type in COUNT_ORDER if counts[rule_type]]
    extra = sorted(rule_type for rule_type in counts if rule_type not in COUNT_ORDER)
    return [f"# {rule_type}: {counts[rule_type]}" for rule_type in known + extra]


def header(total_name: str, counts: Counter[str]) -> list[str]:
    total = sum(counts.values())
    return [
        f"# NAME: {total_name}",
        f"# AUTHOR: {AUTHOR}",
        f"# REPO: {REPO_URL}",
        f"# UPDATED: {date.today().isoformat()}",
        *count_lines(counts),
        f"# TOTAL: {total}",
        "",
    ]


def render_clash(sections: list[list[Entry]], counts: Counter[str]) -> str:
    lines = header("Trading Platform", counts)
    lines.append("payload:")
    for index, section in enumerate(sections):
        if index:
            lines.append("")
        for entry in section:
            if entry.kind == "blank":
                lines.append("")
            elif entry.kind == "comment":
                lines.append(f"  {entry.value}")
            elif entry.kind == "rule":
                lines.append(f"  - {entry.value}")
    return "\n".join(lines).rstrip() + "\n"


def render_surge(sections: list[list[Entry]], counts: Counter[str]) -> str:
    lines = header("Trading Platform", counts)
    for index, section in enumerate(sections):
        if index:
            lines.append("")
        for entry in section:
            lines.append(entry.value)
    return "\n".join(lines).rstrip() + "\n"


def source_files(directory: Path, suffix: str) -> list[Path]:
    return sorted(
        (
            path
            for path in directory.glob(f"*{suffix}")
            if path.stem != "trading_platform"
        ),
        key=sort_key,
    )


def main() -> None:
    clash_sources = [read_clash_rule(path) for path in source_files(ROOT / "rules/clash", ".yaml")]
    surge_sources = [read_surge_rule(path) for path in source_files(ROOT / "rules/surge", ".list")]

    clash_sections, clash_counts = build_sections(clash_sources)
    surge_sections, surge_counts = build_sections(surge_sources)

    (ROOT / "rules/clash/trading_platform.yaml").write_text(
        render_clash(clash_sections, clash_counts),
        encoding="utf-8",
    )
    (ROOT / "rules/surge/trading_platform.list").write_text(
        render_surge(surge_sections, surge_counts),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
