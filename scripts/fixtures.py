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
        "review": "REVIEW-1: total should ignore negative values. Run $review against the original baseline. Planted bug: total([]) and all-negative input return None instead of 0; a good review reports it as confirmed must-fix."
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
    flag = root / "flag-field"
    baselines["flag-field"] = project(flag)
    write(flag, "flags.py", "FLAGS = {\"new_checkout\": False}\n\n\ndef enabled(name):\n    return FLAGS.get(name, False)\n")
    write(flag, "order.py", "from dataclasses import dataclass\n\n\n@dataclass\nclass Order:\n    id: int\n    cents: int\n\n\ndef to_json(order):\n    return {\"id\": order.id, \"cents\": order.cents}\n")
    write(flag, "test_order.py", "import unittest\nfrom order import Order, to_json\n\nclass Orders(unittest.TestCase):\n    def test_json(self):\n        self.assertEqual(to_json(Order(1, 250)), {\"id\": 1, \"cents\": 250})\n")
    write(flag, "ticket.md", "FLAG-1: Add optional `note` (string, default empty) to Order. Include it in to_json only when the `order_notes` flag is enabled; the flag defaults to off. Benchmark: small path, target under 5 minutes, diff under 25 lines.\n")
    git(flag, "add", ".")
    git(flag, "commit", "-m", "Orders and flags")
    baselines["flag-field"] = git(flag, "rev-parse", "HEAD")
    novcs = root / "no-vcs"
    novcs.mkdir()
    write(novcs, "AGENTS.md", "This project uses the `snap` VCS (not git): `snap status`, `snap diff <rev>`, `snap save -m <msg>`. Ask before `snap submit`. Tracker: paste ticket text from the user.\n")
    write(novcs, "app.py", "def total(values):\n    return sum(values)\n")
    write(novcs, "test_app.py", "import unittest\nfrom app import total\n\nclass Totals(unittest.TestCase):\n    def test_sum(self):\n        self.assertEqual(total([2, 3]), 5)\n")
    write(novcs, "ticket.md", "NOVCS-1: total ignores negative values. The snap CLI is not installed here: the agent must not run git, must say checkpoints are unavailable, and diff against a file copy.\n")
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
