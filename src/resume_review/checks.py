"""Deterministic checks that run on the resume text before and after the AI review.

The AI review is good at judgement but can miss simple factual errors. These
checks catch the mistakes a recruiter would spot instantly, so the AI's output
never goes out unchecked.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

BUZZWORDS = [
    "results-driven", "results driven", "team player", "hard-working", "hardworking",
    "detail-oriented", "detail oriented", "analytical", "synergy", "dynamic",
    "go-getter", "passionate", "self-starter", "self starter", "think outside the box",
    "strong interest", "skilled in", "data-driven", "responsible for",
]

# "60% of 4 users", "90% of 12 participants"
PERCENT_OF_N = re.compile(r"(\d{1,3}(?:\.\d+)?)\s*%\s+of\s+(?:the\s+)?(\d{1,4})\b", re.IGNORECASE)
BULLET = re.compile(r"^\s*[•\-\*▪●]\s+(.*)$")


@dataclass
class Finding:
    check: str
    detail: str


def impossible_percentages(text: str) -> list[Finding]:
    """Flag 'X% of N' where X% of N is not a whole number of people/items."""
    findings = []
    for match in PERCENT_OF_N.finditer(text):
        pct, n = float(match.group(1)), int(match.group(2))
        count = pct / 100 * n
        if n > 0 and abs(count - round(count)) > 0.01:
            findings.append(Finding(
                "Impossible percentage",
                f'"{match.group(0)}" works out to {count:g} people/items. '
                "Check where the percentage really came from.",
            ))
    return findings


def buzzwords(text: str) -> list[Finding]:
    lowered = text.lower()
    found = []
    for word in BUZZWORDS:
        hits = len(re.findall(r"\b" + re.escape(word) + r"\b", lowered))
        if hits:
            found.append(Finding("Buzzword", f'"{word}" appears {hits}x. Replace it with evidence.'))
    return found


def bullets_without_numbers(text: str) -> list[Finding]:
    """Join wrapped bullet lines, then flag bullets that contain no digits."""
    bullets: list[str] = []
    for line in text.splitlines():
        m = BULLET.match(line)
        if m:
            bullets.append(m.group(1).strip())
        elif bullets and line.startswith(("  ", "\t")) and line.strip():
            bullets[-1] += " " + line.strip()
    return [
        Finding("No metric", f'"{b[:90]}{"…" if len(b) > 90 else ""}"')
        for b in bullets
        if not re.search(r"\d", b)
    ]


def inconsistent_figures(resume: str, master: str) -> list[Finding]:
    """Flag percentages that appear near the same words in both versions but differ.

    Simple heuristic: for each percentage in the resume, take the two words before it
    and look for the same two words followed by a different percentage in the master.
    """
    pattern = re.compile(r"(\b\w+\W+\w+)\W+(\d{1,3}(?:\.\d+)?)\s*%")
    master_map: dict[str, set[str]] = {}
    for ctx, val in pattern.findall(master):
        master_map.setdefault(ctx.lower(), set()).add(val)
    findings = []
    for ctx, val in pattern.findall(resume):
        others = master_map.get(ctx.lower())
        if others and val not in others:
            findings.append(Finding(
                "Figure differs from master",
                f'"…{ctx} {val}%" here vs {", ".join(sorted(others))}% in the master resume.',
            ))
    return findings


def run_all(resume: str, master: str | None = None) -> list[Finding]:
    findings = impossible_percentages(resume) + buzzwords(resume) + bullets_without_numbers(resume)
    if master:
        findings += [Finding(f.check + " (master)", f.detail) for f in impossible_percentages(master)]
        findings += inconsistent_figures(resume, master)
    return findings


def to_markdown(findings: list[Finding]) -> str:
    if not findings:
        return "## Automated checks\n\nNo issues found.\n"
    lines = ["## Automated checks", "", "| Check | Detail |", "|---|---|"]
    lines += [f"| {f.check} | {f.detail.replace('|', '/')} |" for f in findings]
    return "\n".join(lines) + "\n"
