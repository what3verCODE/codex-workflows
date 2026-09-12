#!/usr/bin/env python3
"""Create disposable acceptance projects. Existing destinations are never replaced."""

import json
from pathlib import Path
import subprocess
import sys


def write(root, path, content):
    file = root / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()


def project(root, code="def total(values):\n    return sum(values)\n"):
    root.mkdir(parents=True)
    write(root, "AGENTS.md", "Use the existing unittest boundary. Base branch is main; task branches use task/<ticket>. Checkpoint only task files. Keep memory.md accurate.\n")
    write(root, "app.py", code)
    write(root, "test_app.py", "import unittest\nfrom app import total\n\nclass Totals(unittest.TestCase):\n    def test_sum(self):\n        self.assertEqual(total([2, 3]), 5)\n")
    write(root, "memory.md", "total adds all supplied values.\n")
    write(root, "Makefile", "test:\n\t@python3 -m unittest -v\n")
    git(root, "init", "-b", "main")
    git(root, "config", "user.name", "Workflow fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "add", ".")
    git(root, "commit", "-m", "Fixture baseline")
    return git(root, "rev-parse", "HEAD")


def main():
    root = Path(sys.argv[1]).resolve()
    root.mkdir(parents=True, exist_ok=False)
    baselines = {}
    for name in ("prepared", "clarification", "prepared-bug", "uncertain-bug", "documentation", "existing-edits", "review", "multi/service", "multi/client"):
        code = "def total(values):\n    return sum(values) if values else None\n" if "bug" in name else "def total(values):\n    return sum(values)\n"
        baselines[name] = project(root / name, code)
    tickets = {
        "prepared": "PREP-1: total ignores negative values, keeps zero and positives. Existing unittest is the agreed boundary. Update memory.md.",
        "clarification": "ASK-1: Change total to handle discounts correctly. Discount meaning has not been decided. Ask before implementation.",
        "prepared-bug": "BUG-1: Empty totals must be zero. Investigation established that the truthiness conditional in app.py returns None for []. Comment: total([]) was observed returning None. Use the existing unittest boundary for regression.",
        "uncertain-bug": "BUG-2: Empty basket totals display None instead of zero. Determine the cause and return evidence before implementation. Use the existing unittest boundary if implementation is subsequently requested.",
        "documentation": "DOC-1: Expand memory.md with examples for [2, 3] and []. Inspect app.py as the authority. Documentation only.",
        "existing-edits": "EDIT-1: Complete the relevant edit to ignore negative values. Reuse task/EDIT-1, preserve notes.txt and keep it out of checkpoints. Add regression tests and update memory.md.",
        "multi": "MULTI-1: total in both service and client must ignore negative values. Each uses its existing unittest boundary. Update both memory files. The two projects form one ticket.",
        "review": "REVIEW-1: total should ignore negative values. Review against the original baseline, with independent standards/specification and technical analysis. Both code and memory must describe that behavior."
    }
    for name, ticket in tickets.items():
        write(root, name + "/ticket.md", ticket + "\n")
    git(root / "existing-edits", "switch", "-c", "task/EDIT-1")
    write(root, "existing-edits/app.py", "def total(values):\n    return sum(value for value in values if value >= 0)\n")
    write(root, "existing-edits/notes.txt", "Unrelated personal draft, preserve exactly.\n")
    write(root, "review/app.py", "def total(values):\n    return sum(value for value in values if value > 0) or None\n")
    write(root, "review/memory.md", "total ignores negative values and returns zero for an empty list.\n")
    git(root / "review", "switch", "-c", "task/REVIEW-1")
    git(root / "review", "add", "app.py", "memory.md")
    git(root / "review", "commit", "-m", "Implement positive totals")
    write(root, "baselines.json", json.dumps(baselines, indent=2) + "\n")
    write(root, "multi/AGENTS.md", "| Project | Path |\n| --- | --- |\n| Totals service | ./service |\n| Totals client | ./client |\nOnly these projects participate in MULTI-1. Read each project's instructions.\n")
    for i in range(1500):
        write(root, f"discovery/archive/{i:04d}.txt", f"Unrelated archived event {i}.\n")
    write(root, "discovery/services/billing/AGENTS.md", "Read rules.md before changing billing.\n")
    write(root, "discovery/services/billing/rules.md", "Amounts are integer cents.\n")
    write(root, "discovery/services/billing/invoice.py", "def invoice_total(items):\n    return sum(item['cents'] for item in items)\n")
    write(root, "discovery/AGENTS.md", "| Project | Path |\n| --- | --- |\n| Billing | services/billing |\n")
    write(root, "tracker.json", json.dumps({"issues": {"17": {"title": "Totals spec", "body": "## Operations\nKeep the migration window.\n\n## Specification\nOld spec.\n", "comments": ["Keep this discussion."], "labels": ["customer"]}}, "relationships": []}, indent=2) + "\n")
    print(root)


if __name__ == "__main__":
    main()
