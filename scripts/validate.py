#!/usr/bin/env python3
"""Validate sources.json, this kit's skills and roles without downloading anything."""

import json
from pathlib import Path
import re

from install import NAME, parse_role


def main():
    root = Path(__file__).resolve().parents[1]
    sources = json.loads((root / "sources.json").read_text())
    names = []
    for source in sources["upstream"]:
        if not re.fullmatch(r"[0-9a-f]{40}", source["revision"]):
            raise ValueError(f"pin a full commit SHA for {source['repository']}")
        names += source["skills"]
    for path in sorted((root / "kit/skills").iterdir()):
        frontmatter = (path / "SKILL.md").read_text().split("---", 2)[1]
        if not re.search(rf"^name: {re.escape(path.name)}$", frontmatter, re.M) or "\ndescription: " not in frontmatter:
            raise ValueError(f"invalid skill metadata: {path}")
        names.append(path.name)
    if len(names) != len(set(names)) or not all(NAME.fullmatch(name) for name in names):
        raise ValueError(f"invalid or duplicate skill names: {sorted(names)}")
    roles = [parse_role(path) for path in sorted((root / "kit/agents").glob("*.md"))]
    for role in roles:
        if set(role["skills"]) - set(names):
            raise ValueError(f"{role['name']} requires unknown skills")
    print(f"Validated {len(names)} skills and {len(roles)} roles.")


if __name__ == "__main__":
    main()
