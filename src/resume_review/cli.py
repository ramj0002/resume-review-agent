"""Review a resume against a job ad with Claude, plus deterministic checks.

Usage:
    python -m resume_review --resume cv.pdf --job job_ad.txt [--master master.pdf] [--out report.md]
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .checks import run_all, to_markdown

ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = ROOT / "skill" / "SKILL.md"
DEFAULT_MODEL = "claude-sonnet-5-5"

CLI_NOTE = """
You are running inside a command-line tool, not a chat. All inputs are provided below.
Do not ask questions or offer follow-ups: produce the full review as a Markdown report.
If the master resume is missing, skip that section.
"""


def read_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        sys.exit(f"File not found: {path}")
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader
        return "\n".join(page.extract_text() or "" for page in PdfReader(p).pages)
    if suffix == ".docx":
        import docx
        return "\n".join(par.text for par in docx.Document(p).paragraphs)
    return p.read_text(encoding="utf-8")


def load_skill() -> str:
    text = SKILL_PATH.read_text(encoding="utf-8")
    # Drop the YAML front matter; keep the instructions.
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    return text.strip() + "\n" + CLI_NOTE


def build_message(resume: str, job: str, master: str | None, checks_md: str) -> str:
    parts = [f"<job_ad>\n{job}\n</job_ad>", f"<resume>\n{resume}\n</resume>"]
    if master:
        parts.append(f"<master_resume>\n{master}\n</master_resume>")
    parts.append(
        "<automated_checks>\nThese deterministic checks already ran on the resume. "
        "Confirm or dismiss each one in your review; do not ignore them.\n"
        f"{checks_md}\n</automated_checks>"
    )
    return "\n\n".join(parts)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Recruiter-style resume review against a job ad.")
    ap.add_argument("--resume", required=True, help="Tailored resume (.pdf, .docx, .md, .txt)")
    ap.add_argument("--job", required=True, help="Job ad text file (.txt, .md)")
    ap.add_argument("--master", help="Optional master resume")
    ap.add_argument("--out", default="review.md", help="Where to write the report")
    ap.add_argument("--model", default=os.environ.get("RESUME_REVIEW_MODEL", DEFAULT_MODEL))
    ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--checks-only", action="store_true", help="Run the deterministic checks only (no API call)")
    ap.add_argument("--dry-run", action="store_true", help="Print the prompt instead of calling the API")
    args = ap.parse_args(argv)

    resume = read_text(args.resume)
    job = read_text(args.job)
    master = read_text(args.master) if args.master else None
    checks_md = to_markdown(run_all(resume, master))

    if args.checks_only:
        Path(args.out).write_text(checks_md, encoding="utf-8")
        print(checks_md)
        return

    system, message = load_skill(), build_message(resume, job, master, checks_md)
    if args.dry_run:
        print("=== SYSTEM ===\n" + system + "\n\n=== USER ===\n" + message)
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Set ANTHROPIC_API_KEY first (or use --checks-only / --dry-run).")

    import anthropic
    client = anthropic.Anthropic()
    print(f"Reviewing with {args.model}…", file=sys.stderr)
    response = client.messages.create(
        model=args.model,
        max_tokens=args.max_tokens,
        system=system,
        messages=[{"role": "user", "content": message}],
    )
    review = "".join(block.text for block in response.content if block.type == "text")
    report = review.rstrip() + "\n\n---\n\n" + checks_md
    Path(args.out).write_text(report, encoding="utf-8")
    print(f"Saved {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
